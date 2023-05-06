<?php
include_once("functions.php");
include_once("config.php");


$_SESSION['CSRFToken'] = md5(random_bytes(32));

if (!isset($_SESSION['is_auth']) or !$_SESSION['is_auth']){
    redirect('login.php');
    die();
}

if(!isset($_GET['file_name']) or !is_string($_GET['file_name'])){
    redirect('vault.php');
    die();
}

if(!isset($_GET['h']) or !is_string($_GET['h'])){
    redirect('vault.php');
    die();
}

// check the hash
if(!check_url()){
    redirect('vault.php');
    die();
}


$file = '/var/www/files/'. $_GET['file_name'];
if (!file_exists($file)) {
    redirect('vault.php');
    die();
}
else{
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.basename($file).'"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize($file));
    readfile($file);
    exit;
}

?>