<?php
$rmf = function($file){
    system('rm -f -- '.escapeshellarg($file));
};

$page = $_GET['page'] ?? 'default';
chdir('./data');

if(isset($_GET['reset']) && preg_match('/^[a-zA-Z0-9]+$/', $page) === 1) {
    $rmf($page);
}

file_put_contents($page, file_get_contents($page) + 1);
include_once($page);
