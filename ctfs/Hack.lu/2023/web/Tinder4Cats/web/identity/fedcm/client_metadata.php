<?php

header('Content-Type: application/json;');
if ($_SERVER['HTTP_SEC_FETCH_DEST'] !== 'webidentity') {
    die();
}

$data = [
    'privacy_policy_url' => 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'terms_of_service_url' => 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
];

echo json_encode($data, JSON_PRETTY_PRINT);
