<?php
/**
 * Roasist Corporate Website — Native cPanel / Veridyen Lead Endpoint
 * Receives JSON POST from /iletisim/, /start-your-project/, /en/contact-us/, /en/start-your-project/
 * 1. Validates fields & blocks honeypot / header-injection / rapid spam
 * 2. Stores a private backup record in api/_leads_private/leads.jsonl
 * 3. Sends a UTF-8 HTML email to info@roasist.com with Reply-To set to the visitor
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method Not Allowed']);
    exit;
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

function clean_line($val, $max = 300) {
    $s = trim((string)$val);
    $s = str_replace(["\r", "\n", "\0"], ' ', $s);
    return mb_substr($s, 0, $max, 'UTF-8');
}

$name     = clean_line($data['name'] ?? ($data['Ad_Soyad'] ?? ''), 160);
$email    = clean_line($data['email'] ?? ($data['Eposta'] ?? ''), 160);
$services = clean_line($data['services'] ?? ($data['Hizmetler'] ?? '-'), 500);
$budget   = clean_line($data['budget'] ?? ($data['Butce'] ?? '-'), 160);
$page     = clean_line($data['page'] ?? ($data['Sayfa'] ?? '-'), 300);
$subject  = clean_line($data['subject'] ?? 'Yeni Proje & Teklif Talebi — Roasist Web', 200);
$message  = trim((string)($data['message'] ?? ($data['Mesaj'] ?? '-')));
$message  = mb_substr($message, 0, 4000, 'UTF-8');

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Invalid email']);
    exit;
}

if ($name === '') {
    $name = 'Web Ziyaretçisi';
}

// Private backup directory + lightweight IP rate limiting (max 6 req / 10 min)
$privateDir = __DIR__ . '/_leads_private';
if (!is_dir($privateDir)) {
    @mkdir($privateDir, 0750, true);
}

$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$ipHash = substr(hash('sha256', $ip . date('Y-m-d')), 0, 16);
$rateFile = $privateDir . '/rate_' . $ipHash . '.json';
$now = time();
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

// 1. Save private backup record so zero leads are ever lost
$record = [
    'timestamp' => gmdate('c'),
    'name'      => $name,
    'email'     => $email,
    'services'  => $services,
    'budget'    => $budget,
    'message'   => $message,
    'page'      => $page,
    'ip_hash'   => $ipHash,
];
@file_put_contents(
    $privateDir . '/leads.jsonl',
    json_encode($record, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n",
    FILE_APPEND | LOCK_EX
);

// 2. Send formatted UTF-8 HTML email to info@roasist.com
$to = 'info@roasist.com';
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject . ' (' . $name . ')') . '?=';

$safeName     = htmlspecialchars($name, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeEmail    = htmlspecialchars($email, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeServices = htmlspecialchars($services, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeBudget   = htmlspecialchars($budget, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safePage     = htmlspecialchars($page, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$safeMessage  = nl2br(htmlspecialchars($message, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
$dateStr      = date('d.m.Y H:i');

$htmlBody = <<<HTML
<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#f8fafc;padding:24px;color:#0f172a;">
  <div style="max-width:600px;margin:0 auto;background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:28px;">
    <h2 style="margin:0 0 16px;font-size:18px;color:#0f172a;">Yeni Web Formu Talebi — Roasist</h2>
    <table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.6;">
      <tr><td style="padding:8px 0;color:#64748b;width:160px;"><strong>Ad Soyad:</strong></td><td style="padding:8px 0;color:#0f172a;">{$safeName}</td></tr>
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
