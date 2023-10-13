<?php


header('Content-Type: application/json;');
if ($_SERVER['HTTP_SEC_FETCH_DEST'] !== 'webidentity') {
    die();
}

session_start();

// not logged in
if(!isset($_SESSION['identity'])){
    die('Not logged in.');
}

// check account_id
if (!isset($_POST['account_id']) || $_POST['account_id'] !== $_SESSION['identity']['id']) {
    die('Account ID mismatch.');
}

// check origin
if (!isset($_SERVER['HTTP_ORIGIN']) || $_SERVER['HTTP_ORIGIN'] !== 'https://' . getenv('APP_DOMAIN')){
    die('Wrong origin.');
}



$token = [
    'iss' => getenv('IDENTITY_DOMAIN'),
    'aud' => $_POST['client_id'] ?? 'N/A',
    'sub' => $_POST['account_id']  ?? 'N/A',
    'nonce' => $_POST['nonce']  ?? 'N/A',
    'disclosure_text_shown' => $_POST['disclosure_text_shown'] ?? 'N/A',
    'username' => $_SESSION['identity']['given_name'],
    'hash' => hash('sha3-256', $_POST['nonce'] . $_SESSION['identity']['given_name'] . getenv('SHARED_SECRET'))
];

$data = [
    'token' => json_encode($token)
];

echo json_encode($data, JSON_PRETTY_PRINT);
