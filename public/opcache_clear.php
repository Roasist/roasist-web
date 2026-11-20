<?php
/**
 * Roasist Corporate Website (www.roasist.com) — OPcache & LiteSpeed Cache Purge Endpoint
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

$SECRET_SHA256 = 'f6b0ff71638ffbd8e6bc9ad15e9d04d9e0bf59acf53cb25cc2307c56421c2d33';

$providedSecret = $_SERVER['HTTP_X_ROASIST_DEPLOY_SECRET']
    ?? $_POST['secret']
    ?? $_GET['secret']
    ?? '';

if (!is_string($providedSecret) || $providedSecret === '' || !hash_equals($SECRET_SHA256, hash('sha256', trim($providedSecret)))) {
    http_response_code(403);
    echo json_encode([
        'status' => 'error',
        'message' => 'Unauthorized: Invalid secret token'
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

$opcacheReset = false;
if (function_exists('opcache_reset')) {
    $opcacheReset = @opcache_reset();
}

header('X-LiteSpeed-Purge: *');
header('Cache-Control: no-cache, no-store, must-revalidate');

echo json_encode([
    'status'           => 'success',
    'message'          => 'OPcache ve LiteSpeed önbelleği başarıyla temizlendi!',
    'opcache_reset'    => $opcacheReset,
    'litespeed_purged' => true,
    'timestamp'        => date('Y-m-d H:i:s')
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
