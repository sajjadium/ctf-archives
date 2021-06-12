<?php

header('Content-Type: image/png');

if (isset($_COOKIE['token']) && $_COOKIE['token'] === getenv('TOKEN')) {
    $filepath = '/opt/flag.png';
} else {
    $filepath = '/opt/no_flag.png';
}

echo file_get_contents($filepath);
