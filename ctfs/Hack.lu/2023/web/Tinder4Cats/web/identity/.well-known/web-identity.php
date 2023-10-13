<?php

header('Content-Type: application/json;');
header('Access-Control-Allow-Origin: *'); // required by firefox

$data = [
    'provider_urls' => [
        'https://' . getenv('IDENTITY_DOMAIN') . '/fedcm/config.php'
    ]
];

echo json_encode($data, JSON_PRETTY_PRINT);