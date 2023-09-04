<?php

require_once './inc/ecc/point.php';
require_once './inc/ecc/curve.php';
require_once './inc/license.php';

use Ecc\Point;
use Ecc\CurveP256;

function die_err_json(string $message, int $status_code = 400)
{
    http_response_code($status_code);

    echo json_encode([
        'status' => 'error',
        'message' => $message
    ]);

    exit();
}

function die_json(string $message)
{
    echo json_encode([
        'status' => 'success',
        'message' => $message
    ]);

    exit();
}

header('Content-type: application/json');

$input = file_get_contents('php://input');

$pubkey = new Point(
    gmp_init($_ENV['LPLZ_PUBKEY_X'], 62),
    gmp_init($_ENV['LPLZ_PUBKEY_Y'], 62)
);
$curve = CurveP256::getInstance();

try {
    $license = License::import($input, $pubkey, $curve);

    if ($license->demo) {
        die_json("Welcome, {$license->user}.\nWant the flag? Sorry but it's not something I can reveal to demo users...");
    } else {
        die_json("Well done!\n" . $_ENV['LPLZ_FLAG']);
    }
} catch (LicenseInvalidFormatException $e) {
    die_err_json($e->getMessage());
} catch (LicenseInvalidSignatureException | LicenseExpiredException $e) {
    die_err_json($e->getMessage(), 403);
} catch (Exception $e) {
    die_err_json('Unknown error', 500);
}
