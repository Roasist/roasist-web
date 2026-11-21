<?php
/**
 * Roasist Corporate Website — Hardened Native cPanel / Veridyen Lead Endpoint
 * Security controls:
 *   1. POST-only + JSON Content-Type + X-Requested-With custom header + Origin/Referer validation
 *   2. Honeypot + strict field & Reply-To sanitization (blocks SMTP header injection)
 *   3. KVKK-safe HMAC-SHA256 IP hashing with auto-generated private server salt + stale rate-file cleanup
 *   4. Protected backup lead storage (api/_leads_private/leads.jsonl) with 5 MB log rotation
 */

@ini_set('display_errors', '0');
@header_remove('X-Powered-By');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store, no-cache, must-revalidate');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method Not Allowed']);
    exit;
}

// Require custom AJAX header + JSON Content-Type (blocks cross-site form CSRF & simple bots)
$contentType   = strtolower((string)($_SERVER['CONTENT_TYPE'] ?? $_SERVER['HTTP_CONTENT_TYPE'] ?? ''));
$requestedWith = (string)($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '');
if (strpos($contentType, 'application/json') === false || $requestedWith !== 'RoasistWebForm') {
    http_response_code(403);
    echo json_encode(['ok' => false, 'error' => 'Forbidden request context']);
    exit;
}

// Validate Origin / Referer against allowed hosts
$allowedHosts = ['www.roasist.com', 'roasist.com', '127.0.0.1', 'localhost'];
$originHeader = (string)($_SERVER['HTTP_ORIGIN'] ?? '');
$refererHeader = (string)($_SERVER['HTTP_REFERER'] ?? '');
$sourceUrl = $originHeader !== '' ? $originHeader : $refererHeader;
if ($sourceUrl !== '') {
    $parsedHost = strtolower((string)(parse_url($sourceUrl, PHP_URL_HOST) ?? ''));
    if ($parsedHost === '' || !in_array($parsedHost, $allowedHosts, true)) {
        http_response_code(403);
        echo json_encode(['ok' => false, 'error' => 'Origin not permitted']);
        exit;
    }
}

$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > 32768) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Invalid payload']);
    exit;
}

$data = json_decode($raw, true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Invalid JSON']);
    exit;
}

// Honeypot check
if (!empty($data['honeypot'])) {
    echo json_encode(['ok' => true]);
    exit;
}

function clean_line($val, int $max = 300): string {
    $s = trim((string)$val);
    $s = str_replace(["\r", "\n", "\0"], ' ', $s);
    return mb_substr($s, 0, $max, 'UTF-8');
}

$name     = clean_line($data['name'] ?? ($data['Ad_Soyad'] ?? ''), 160);
$rawEmail = clean_line($data['email'] ?? ($data['Eposta'] ?? ''), 160);
$email    = str_replace([' ', '<', '>', ',', ';', '"', "'"], '', $rawEmail);
$phone    = clean_line($data['phone'] ?? ($data['contactPhone'] ?? ($data['Telefon'] ?? '-')), 60);
if ($phone === '') {
    $phone = '-';
}
$services = clean_line($data['services'] ?? ($data['Hizmetler'] ?? '-'), 500);
$budget   = clean_line($data['budget'] ?? ($data['Butce'] ?? '-'), 160);
$page     = clean_line($data['page'] ?? ($data['Sayfa'] ?? '-'), 300);
$subject  = clean_line($data['subject'] ?? 'Yeni Proje & Teklif Talebi — Roasist Web', 200);
$message  = trim((string)($data['message'] ?? ($data['Mesaj'] ?? '-')));
$message  = str_replace("\0", '', mb_substr($message, 0, 4000, 'UTF-8'));

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Invalid email']);
    exit;
}

if ($name === '') {
    $name = 'Web Ziyaretçisi';
}

// Private backup directory + server-local secret salt for KVKK-compliant IP hashing
$privateDir = __DIR__ . '/_leads_private';
if (!is_dir($privateDir)) {
    @mkdir($privateDir, 0750, true);
}

$saltFile = $privateDir . '/.ip_salt';
$salt = @file_get_contents($saltFile);
if (!is_string($salt) || strlen($salt) < 32) {
    try {
        $salt = bin2hex(random_bytes(32));
    } catch (Throwable $e) {
        $salt = hash('sha256', __FILE__ . '|' . php_uname() . '|' . microtime(true));
    }
    @file_put_contents($saltFile, $salt, LOCK_EX);
}

$now    = time();
$ip     = (string)($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$ipHash = substr(hash_hmac('sha256', $ip . '|' . gmdate('Y-m-d'), $salt), 0, 16);

// Opportunistic cleanup of expired rate_*.json files (> 15 min old) to protect cPanel inode quota
$staleFiles = @glob($privateDir . '/rate_*.json');
if (is_array($staleFiles)) {
    $checked = 0;
    foreach ($staleFiles as $sf) {
        if (++$checked > 40) {
            break;
        }
        $mtime = @filemtime($sf);
        if ($mtime !== false && ($now - $mtime) > 900) {
            @unlink($sf);
        }
    }
}

// Per-IP rate limiting: max 6 submissions per 10 minutes
$rateFile = $privateDir . '/rate_' . $ipHash . '.json';
$hits = [];
if (is_file($rateFile)) {
    $decodedHits = json_decode((string)@file_get_contents($rateFile), true);
    if (is_array($decodedHits)) {
        foreach ($decodedHits as $ts) {
            if (is_int($ts) && ($now - $ts) < 600) {
                $hits[] = $ts;
            }
        }
    }
}
if (count($hits) >= 6) {
    http_response_code(429);
    echo json_encode(['ok' => false, 'error' => 'Too many requests']);
    exit;
}
$hits[] = $now;
@file_put_contents($rateFile, json_encode($hits), LOCK_EX);

// 1. Save private backup record with 5 MB rotation cap
$leadsFile = $privateDir . '/leads.jsonl';
if (is_file($leadsFile) && @filesize($leadsFile) > 5242880) {
    @rename($leadsFile, $privateDir . '/leads.1.jsonl');
}

$record = [
    'timestamp' => gmdate('c'),
    'name'      => $name,
    'email'     => $email,
    'phone'     => $phone,
    'services'  => $services,
    'budget'    => $budget,
    'message'   => $message,
    'page'      => $page,
    'ip_hash'   => $ipHash,
];
@file_put_contents(
    $leadsFile,
    json_encode($record, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n",
    FILE_APPEND | LOCK_EX
);

// 2. Send formatted UTF-8 HTML email to info@roasist.com
$to = 'info@roasist.com';
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject . ' (' . $name . ')') . '?=';

$safeName     = htmlspecialchars($name, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeEmail    = htmlspecialchars($email, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safePhone    = htmlspecialchars($phone, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$telHref      = preg_replace('/[^0-9+]/', '', $phone);
$safeServices = htmlspecialchars($services, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeBudget   = htmlspecialchars($budget, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safePage     = htmlspecialchars($page, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeMessage  = nl2br(htmlspecialchars($message, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
$dateStr      = date('d.m.Y H:i');

$phoneCell = ($telHref !== '')
    ? "<a href=\"tel:{$telHref}\" style=\"color:#0f172a;\">{$safePhone}</a>"
    : $safePhone;

$htmlBody = <<<HTML
<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#f8fafc;padding:24px;color:#0f172a;">
  <div style="max-width:600px;margin:0 auto;background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:28px;">
    <h2 style="margin:0 0 16px;font-size:18px;color:#0f172a;">Yeni Web Formu Talebi — Roasist</h2>
    <table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.6;">
      <tr><td style="padding:8px 0;color:#64748b;width:160px;"><strong>Ad Soyad:</strong></td><td style="padding:8px 0;color:#0f172a;">{$safeName}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>Telefon / WhatsApp:</strong></td><td style="padding:8px 0;color:#0f172a;">{$phoneCell}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>E-posta:</strong></td><td style="padding:8px 0;"><a href="mailto:{$safeEmail}" style="color:#0f172a;">{$safeEmail}</a></td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>Hizmetler:</strong></td><td style="padding:8px 0;color:#0f172a;">{$safeServices}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>Aylık Bütçe:</strong></td><td style="padding:8px 0;color:#0f172a;">{$safeBudget}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;vertical-align:top;"><strong>Mesaj / Hedefler:</strong></td><td style="padding:8px 0;color:#0f172a;">{$safeMessage}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>Kaynak Sayfa:</strong></td><td style="padding:8px 0;color:#475569;">{$safePage}</td></tr>
      <tr><td style="padding:8px 0;color:#64748b;"><strong>Tarih:</strong></td><td style="padding:8px 0;color:#475569;">{$dateStr}</td></tr>
    </table>
  </div>
</body>
</html>
HTML;

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    'From: Roasist Web <noreply@roasist.com>',
    'Reply-To: ' . $email,
    'X-Mailer: Roasist-Web/1.0',
];

$mailSent = @mail($to, $encodedSubject, chunk_split(base64_encode($htmlBody)), implode("\r\n", $headers));

echo json_encode([
    'ok' => true,
    'mailed' => (bool)$mailSent,
]);
