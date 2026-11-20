<?php
/**
 * Roasist Corporate Website (www.roasist.com) — Automated Deployment Webhook
 * Mirrors Roasist Marketing Suite architecture, hardened with SHA-256 token verification
 * so the repository can safely remain public without exposing the deploy secret.
 *
 * Supported Engines:
 *   1. Direct HTTPS Payload Upload (`POST` multipart `payload=@bundle.zip`)
 *   2. Direct GitHub `veridyen-production` Branch Zip Sync (`mode=github_pull` / default POST)
 *   3. cPanel Local Git Repository Sync Fallback (`/home/roasistc/repositories/roasist-web`)
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
@set_time_limit(180);

$SECRET_SHA256 = 'f6b0ff71638ffbd8e6bc9ad15e9d04d9e0bf59acf53cb25cc2307c56421c2d33';

$providedSecret = $_SERVER['HTTP_X_ROASIST_DEPLOY_SECRET']
    ?? $_POST['secret']
    ?? $_GET['secret']
    ?? '';

if (!is_string($providedSecret) || $providedSecret === '' || !hash_equals($SECRET_SHA256, hash('sha256', trim($providedSecret)))) {
    http_response_code(403);
    echo json_encode([
        'status' => 'error',
        'message' => 'Unauthorized: Invalid deploy secret token'
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

$targetDir  = __DIR__;
$repoDir    = '/home/roasistc/repositories/roasist-web';
$mode       = $_GET['mode'] ?? $_POST['mode'] ?? 'auto';
$uid        = uniqid('rw_', true);
$tempZip    = sys_get_temp_dir() . '/' . $uid . '.zip';
$extractDir = sys_get_temp_dir() . '/' . $uid . '_ext';

$debug        = [];
$filesCopied  = 0;
$deployMethod = 'NONE';

/**
 * Protected relative paths in public_html that must NEVER be overwritten by deployments.
 */
function is_protected_dest(string $subPath, string $destPath): bool {
    $norm = ltrim(str_replace('\\', '/', $subPath), '/');
    if ($norm === 'deploy_config.php' && file_exists($destPath)) {
        return true;
    }
    if (strpos($norm, '.well-known/') === 0 || $norm === '.well-known') {
        return true;
    }
    if (strpos($norm, 'cgi-bin/') === 0 || $norm === 'cgi-bin') {
        return true;
    }
    // Preserve live lead logs & rate-limit files while allowing .htaccess / index.html setup if missing
    if (strpos($norm, 'api/_leads_private/') === 0) {
        $base = basename($norm);
        if ($base === 'leads.jsonl' || strpos($base, 'rate_') === 0) {
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
        if ($f->isDir()) {
            @rmdir($f->getRealPath());
        } else {
            @unlink($f->getRealPath());
        }
    }
    @rmdir($dir);
}

// =========================================================================
// ENGINE 1: Direct HTTPS ZIP Payload Upload (Fastest for delta/code updates)
// =========================================================================
if (
    $mode !== 'github_pull'
    && $_SERVER['REQUEST_METHOD'] === 'POST'
    && isset($_FILES['payload'])
    && $_FILES['payload']['error'] === UPLOAD_ERR_OK
    && class_exists('ZipArchive')
) {
    $zip = new ZipArchive();
    if ($zip->open($_FILES['payload']['tmp_name']) === true) {
        @mkdir($extractDir, 0755, true);
        $zip->extractTo($extractDir);
        $zip->close();

        $filesCopied = sync_directory($extractDir, $targetDir);
        cleanup_dir($extractDir);
        $deployMethod = 'DIRECT_PAYLOAD_UPLOAD';
    }
}

// =========================================================================
// ENGINE 2: Direct GitHub `veridyen-production` Branch Sync (Zero upload limit)
// =========================================================================
if ($filesCopied === 0 && class_exists('ZipArchive')) {
    $branch = preg_replace('/[^a-zA-Z0-9._-]/', '', $_GET['branch'] ?? 'veridyen-production');
    $zipUrl = 'https://codeload.github.com/Roasist/roasist-web/zip/refs/heads/' . $branch . '?t=' . time();

    $fp = @fopen($tempZip, 'w+');
    if ($fp) {
        $ch = curl_init($zipUrl);
        curl_setopt($ch, CURLOPT_TIMEOUT, 150);
        curl_setopt($ch, CURLOPT_FILE, $fp);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_MAXREDIRS, 5);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Roasist-Veridyen-AutoDeployer/1.0');
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        curl_exec($ch);
        $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlErr  = curl_error($ch);
        curl_close($ch);
        fclose($fp);

        $debug['github_http_code'] = $httpCode;
        $debug['download_bytes']   = @filesize($tempZip);
        if ($curlErr) {
            $debug['curl_error'] = $curlErr;
        }

        if ($httpCode === 200 && file_exists($tempZip) && filesize($tempZip) > 1024) {
            $zip = new ZipArchive();
            if ($zip->open($tempZip) === true) {
                @mkdir($extractDir, 0755, true);
                $zip->extractTo($extractDir);
                $zip->close();

                $topDirs = glob($extractDir . '/*', GLOB_ONLYDIR);
                $sourceDir = (!empty($topDirs) && count($topDirs) === 1) ? $topDirs[0] : $extractDir;

                $filesCopied = sync_directory($sourceDir, $targetDir);
                cleanup_dir($extractDir);
                $deployMethod = 'GITHUB_PRODUCTION_BRANCH_SYNC';
            }
        }
        @unlink($tempZip);
    }
}

// =========================================================================
// ENGINE 3: cPanel Local Git CLI Sync Fallback
// =========================================================================
if ($filesCopied === 0 && is_dir($repoDir) && function_exists('exec')) {
    $cmd = "cd " . escapeshellarg($repoDir) . " && export HOME=/home/roasistc && export PATH=\$PATH:/usr/local/cpanel/3rdparty/bin:/usr/bin:/bin && git fetch origin veridyen-production 2>&1 && git reset --hard origin/veridyen-production 2>&1";
    @exec($cmd, $gitOut, $gitStatus);
    $debug['cpanel_git'] = $gitOut;
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
header('Cache-Control: no-cache, no-store, must-revalidate');

if ($filesCopied === 0) {
    http_response_code(500);
    echo json_encode([
        'status'  => 'error',
        'message' => 'Dağıtım sırasında hiçbir dosya kopyalanamadı.',
        'debug'   => $debug
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
