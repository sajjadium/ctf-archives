<?php

if (!isset($_GET['message'])) {
    highlight_file(__FILE__);
    die();
}

header('Content-Type: text/plain; charset="utf-8"');

$message = $_GET['message'];

$ip = $_SERVER['REMOTE_ADDR'];
if ($ip === "172.16.0.10" || $ip === '172.16.0.11') {
    $message = str_replace('flag', getenv('FLAG'), $message);
} else {
    $message = str_replace('flag', 'buckeye{not_the_flag}', $message);
}

echo $message;
