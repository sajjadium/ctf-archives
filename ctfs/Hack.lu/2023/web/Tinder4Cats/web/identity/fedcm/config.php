<?php


header('Content-Type: application/json;');
header('Access-Control-Allow-Origin: *');

$data = [
    'accounts_endpoint' => '/fedcm/accounts.php',
    'client_metadata_endpoint' => '/fedcm/client_metadata.php',
    'id_assertion_endpoint' => '/fedcm/assertion.php',
    'signin_url' => '/login.php',
    'branding' => [
        'background_color' => 'green',
        'color' => '0xFFEEAA',
        'icons' => [
            [
                'url' => 'https://' . getenv('IDENTITY_DOMAIN') . '/static/img/idp.png',
                'size' => 25
            ]
        ]
    ]
];


echo json_encode($data, JSON_PRETTY_PRINT);
