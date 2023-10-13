<?php
require("vendor/autoload.php");

if (isset($_COOKIE['cookie'])) {
    $cookie = base64_decode($_COOKIE['cookie']);
    unserialize($cookie);
}

echo "Welcome to my web app!";
