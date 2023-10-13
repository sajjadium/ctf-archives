<?php

header('Content-Type: application/json;');
if ($_SERVER['HTTP_SEC_FETCH_DEST'] !== 'webidentity') {
    die();
}

session_start();

if(!isset($_SESSION['identity'])){
    http_response_code(401);
    die();
}

$data = [
    'accounts' => [$_SESSION['identity']]
];

echo json_encode($data, JSON_PRETTY_PRINT);