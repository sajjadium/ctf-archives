<?php

include 'config.php';


if (isset($_POST['token']) && is_string($_POST['token'])) {
    $token = json_decode($_POST['token'], true);
    if (isset($token['nonce']) && isset($token['username']) && isset($token['hash'])) {
        if (hash('sha3-256', $token['nonce'] . $token['username'] . getenv('SHARED_SECRET')) === $token['hash']) {
            $_SESSION['user'] = db::get_user($token['username']) ?? die('User not found.');
            die('Logged in.');
        }
    }
}
die('Invalid token.');