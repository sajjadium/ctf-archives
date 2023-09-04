<?php

require_once './inc/ecc/curve.php';
require_once './inc/license.php';

use Ecc\CurveP256;

function die_err_json(string $message, int $status_code = 400)
{
    http_response_code($status_code);

    echo json_encode([
        'message' => $message
    ]);

    exit();
}

header('Content-type: application/json');

$user = $_GET['user'] ?? null;
if ($user === null) {
    die_err_json('Missing user field');
}
$user_len = strlen($user);
if ($user_len < 4 || $user_len > 16) {
    die_err_json('Username must be between 4 and 16 characters');
}
$user = strtolower($user);

$privkey = gmp_init($_ENV['LPLZ_PRIVKEY'], 62);
$curve = CurveP256::getInstance();

echo json_encode(License::new($user, '+30 second', true, $privkey, $curve));
