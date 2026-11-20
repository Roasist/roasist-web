<?php
/**
 * Roasist Corporate Website (www.roasist.com) — Hardened Automated Deployment Webhook
 * Security controls:
 *   - POST-only enforcement (405 on GET/HEAD)
 *   - HTTP header-only authentication (`X-Roasist-Deploy-Secret` -> SHA-256 `hash_equals`), zero URL/query secrets
 *   - Per-IP failed-authentication rate limiting (429 after 5 failed attempts / 15 min)
 *   - Zip-Slip & symlink archive entry validation prior to extraction
 *   - Locked production branch (`veridyen-production`) and zero hardcoded server account names
 */

@ini_set('display_errors', '0');
@header_remove('X-Powered-By');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store, no-cache, must-revalidate');
@set_time_limit(180);

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

$SECRET_SHA256 = 'f6b0ff71638ffbd8e6bc9ad15e9d04d9e0bf59acf53cb25cc2307c56421c2d33';

// Failed-auth IP rate limiter (stored in private leads dir or system temp)
$rateDir = is_dir(__DIR__ . '/api/_leads_private') ? (__DIR__ . '/api/_leads_private') : sys_get_temp_dir();
$ip      = (string)($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$authKey = substr(hash('sha256', 'deploy_auth|' . $ip . '|' . gmdate('Y-m-d')), 0, 16);
$authFile = $rateDir . '/deploy_fail_' . $authKey . '.json';
$now = time();

$fails = [];
if (is_file($authFile)) {
    $dec = json_decode((string)@file_get_contents($authFile), true);
    if (is_array($dec)) {
        foreach ($dec as $ts) {
            if (is_int($ts) && ($now - $ts) < 900) {
                $fails[] = $ts;
            }
        }
    }
}
if (count($fails) >= 5) {
    http_response_code(429);
    echo json_encode(['status' => 'error', 'message' => 'Too many unauthorized attempts']);
    exit;
}

// Accept secret strictly from HTTP header (never from URL query string)
$providedSecret = $_SERVER['HTTP_X_ROASIST_DEPLOY_SECRET'] ?? '';

if (!is_string($providedSecret) || $providedSecret === '' || !hash_equals($SECRET_SHA256, hash('sha256', trim($providedSecret)))) {
    $fails[] = $now;
    @file_put_contents($authFile, json_encode($fails), LOCK_EX);
    http_response_code(403);
    echo json_encode([
        'status'  => 'error',
        'message' => 'Unauthorized: Invalid deploy secret token'
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

$targetDir  = __DIR__;
$homeDir    = dirname(__DIR__);
$repoDir    = $homeDir . '/repositories/roasist-web';
$mode       = $_GET['mode'] ?? $_POST['mode'] ?? 'auto';
$uid        = bin2hex(random_bytes(8));
$tempZip    = sys_get_temp_dir() . '/rw_' . $uid . '.zip';
$extractDir = sys_get_temp_dir() . '/rw_' . $uid . '_ext';

$debug        = [];
$filesCopied  = 0;
$deployMethod = 'NONE';

// Remove legacy exposed .cpanel.yml & retired route directories so .htaccess 301 redirects take effect
if (file_exists($targetDir . '/.cpanel.yml')) {
    @unlink($targetDir . '/.cpanel.yml');
}
foreach (['/hizmetler/yapay-zeka-seo', '/en/ai-search-aeo-geo'] as $retiredRel) {
    $retiredAbs = $targetDir . $retiredRel;
    if (is_dir($retiredAbs)) {
        @unlink($retiredAbs . '/index.html');
        @rmdir($retiredAbs);
    }
}

/**
 * Validate every entry in a ZipArchive against Zip-Slip (`..`, absolute paths, null bytes) and Unix symlinks.
 */
function is_safe_zip(ZipArchive $zip): bool {
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $stat = $zip->statIndex($i);
        if (!is_array($stat) || !isset($stat['name'])) {
            return false;
        }
        $name = (string)$stat['name'];
        if (
            $name === ''
            || strpos($name, "\0") !== false
            || strpos($name, '\\') !== false
            || $name[0] === '/'
            || preg_match('#(?:^|/)\.\.(?:/|$)#', $name)
        ) {
            return false;
        }
        // Reject Unix symlinks (S_IFLNK = 0120000)
        if (isset($stat['opsys'], $stat['external_attr']) && $stat['opsys'] === ZipArchive::OPSYS_UNIX) {
            $mode = ($stat['external_attr'] >> 16) & 0170000;
            if ($mode === 0120000) {
                return false;
            }
        }
    }
    return true;
}

/**
 * Protected relative paths in public_html that must NEVER be overwritten by deployments.
 */
function is_protected_dest(string $subPath, string $destPath): bool {
    $norm = ltrim(str_replace('\\', '/', $subPath), '/');
    if ($norm === 'deploy_config.php' && file_exists($destPath)) {
        return true;
    }
    if ($norm === '.cpanel.yml') {
        return true;
    }
    if (strpos($norm, '.well-known/') === 0 || $norm === '.well-known') {
        return true;
    }
    if (strpos($norm, 'cgi-bin/') === 0 || $norm === 'cgi-bin') {
        return true;
    }
    if (strpos($norm, 'api/_leads_private/') === 0) {
        $base = basename($norm);
        if (
            $base === 'leads.jsonl'
            || $base === 'leads.1.jsonl'
            || $base === '.ip_salt'
            || strpos($base, 'rate_') === 0
            || strpos($base, 'deploy_fail_') === 0
        ) {
            return true;
        }
        if (file_exists($destPath)) {
            return true;
        }
    }
    return false;
}

/**
 * Recursively copy extracted directory into public_html, preserving protected runtime data.
 */
function sync_directory(string $sourceDir, string $targetDir): int {
    $copied = 0;
    $iterator = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($sourceDir, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::SELF_FIRST
    );

    foreach ($iterator as $item) {
        if ($item->isLink()) {
            continue;
        }
        $subPath = str_replace('\\', '/', $iterator->getSubPathName());
        if (strpos($subPath, '.git/') === 0 || $subPath === '.git') {
            continue;
        }
        $dest = $targetDir . '/' . $subPath;
        if (is_protected_dest($subPath, $dest)) {
            continue;
        }
        if ($item->isDir()) {
            if (!is_dir($dest)) {
                @mkdir($dest, 0755, true);
            }
        } else {
            $parent = dirname($dest);
            if (!is_dir($parent)) {
                @mkdir($parent, 0755, true);
            }
            if (@copy($item->getPathname(), $dest)) {
                $copied++;
            }
        }
    }

    if (file_exists($sourceDir . '/.htaccess')) {
        @copy($sourceDir . '/.htaccess', $targetDir . '/.htaccess');
    }

    // Prune deleted orphan media files in target/images when full images directory is synced
    if (is_dir($sourceDir . '/images') && is_dir($targetDir . '/images')) {
        $imgIter = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($targetDir . '/images', RecursiveDirectoryIterator::SKIP_DOTS),
            RecursiveIteratorIterator::CHILD_FIRST
        );
        foreach ($imgIter as $tItem) {
            $relImg = str_replace('\\', '/', $imgIter->getSubPathName());
            $srcImg = $sourceDir . '/images/' . $relImg;
            if (!file_exists($srcImg)) {
                if ($tItem->isDir() && !$tItem->isLink()) {
                    @rmdir($tItem->getRealPath());
                } else {
                    @unlink($tItem->getPathname());
                }
            }
        }
    }

    return $copied;
}

/**
 * Recursively remove temporary directory.
 */
function cleanup_dir(string $dir): void {
    if (!is_dir($dir)) {
        return;
    }
    $cleaner = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::CHILD_FIRST
    );
    foreach ($cleaner as $f) {
        if ($f->isDir() && !$f->isLink()) {
            @rmdir($f->getRealPath());
        } else {
            @unlink($f->getPathname());
        }
    }
    @rmdir($dir);
}

// =========================================================================
// ENGINE 1: Direct HTTPS ZIP Payload Upload
// =========================================================================
if (
    $mode !== 'github_pull'
    && isset($_FILES['payload'])
    && $_FILES['payload']['error'] === UPLOAD_ERR_OK
    && class_exists('ZipArchive')
) {
    $zip = new ZipArchive();
    if ($zip->open($_FILES['payload']['tmp_name']) === true) {
        if (is_safe_zip($zip)) {
            @mkdir($extractDir, 0750, true);
            $zip->extractTo($extractDir);
            $zip->close();

            $filesCopied = sync_directory($extractDir, $targetDir);
            cleanup_dir($extractDir);
            $deployMethod = 'DIRECT_PAYLOAD_UPLOAD';
        } else {
            $zip->close();
            $debug['zip_validation'] = 'rejected_unsafe_entries';
        }
    }
}

// =========================================================================
// ENGINE 2: Direct GitHub `veridyen-production` Branch Sync (Locked Branch)
// =========================================================================
if ($filesCopied === 0 && class_exists('ZipArchive')) {
    $branch = 'veridyen-production';
    $zipUrl = 'https://codeload.github.com/Roasist/roasist-web/zip/refs/heads/' . $branch . '?t=' . time();

    $fp = @fopen($tempZip, 'w+');
    if ($fp) {
        $ch = curl_init($zipUrl);
        curl_setopt($ch, CURLOPT_TIMEOUT, 150);
        curl_setopt($ch, CURLOPT_FILE, $fp);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_MAXREDIRS, 5);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Roasist-Veridyen-AutoDeployer/1.1');
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
        curl_exec($ch);
        $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        fclose($fp);

        $debug['github_http_code'] = $httpCode;
        $debug['download_bytes']   = @filesize($tempZip);

        if ($httpCode === 200 && file_exists($tempZip) && filesize($tempZip) > 1024) {
            $zip = new ZipArchive();
            if ($zip->open($tempZip) === true) {
                if (is_safe_zip($zip)) {
                    @mkdir($extractDir, 0750, true);
                    $zip->extractTo($extractDir);
                    $zip->close();

                    $topDirs = glob($extractDir . '/*', GLOB_ONLYDIR);
                    $sourceDir = (!empty($topDirs) && count($topDirs) === 1) ? $topDirs[0] : $extractDir;

                    $filesCopied = sync_directory($sourceDir, $targetDir);
                    cleanup_dir($extractDir);
                    $deployMethod = 'GITHUB_PRODUCTION_BRANCH_SYNC';
                } else {
                    $zip->close();
                    $debug['zip_validation'] = 'rejected_unsafe_entries';
                }
            }
        }
        @unlink($tempZip);
    }
}

// =========================================================================
// ENGINE 3: cPanel Local Git CLI Sync Fallback (Dynamic Home Path)
// =========================================================================
if ($filesCopied === 0 && is_dir($repoDir) && function_exists('exec')) {
    $cmd = "cd " . escapeshellarg($repoDir) . " && export HOME=" . escapeshellarg($homeDir) . " && export PATH=\$PATH:/usr/local/cpanel/3rdparty/bin:/usr/bin:/bin && git fetch origin veridyen-production 2>&1 && git reset --hard origin/veridyen-production 2>&1";
    @exec($cmd, $gitOut, $gitStatus);
    if ($gitStatus === 0) {
        $filesCopied = sync_directory($repoDir, $targetDir);
        $deployMethod = 'CPANEL_GIT_CLI';
    }
}

// Reset PHP OPcache & Purge LiteSpeed Web Cache
$opcacheReset = false;
if (function_exists('opcache_reset')) {
    $opcacheReset = @opcache_reset();
}
header('X-LiteSpeed-Purge: *');

if ($filesCopied === 0) {
    http_response_code(500);
    echo json_encode([
        'status'  => 'error',
        'message' => 'Dağıtım sırasında hiçbir dosya kopyalanamadı.'
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

echo json_encode([
    'status'           => 'success',
    'message'          => 'www.roasist.com canlı sunucuya başarıyla dağıtıldı!',
    'method'           => $deployMethod,
    'files_updated'    => $filesCopied,
    'opcache_reset'    => $opcacheReset,
    'litespeed_purged' => true,
    'timestamp'        => date('Y-m-d H:i:s'),
    'debug'            => $debug
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
