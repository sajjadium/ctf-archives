<?php
include_once("functions.php");
include_once("config.php");
$_SESSION['CSRFToken'] = md5(random_bytes(32));
if (isset($_SESSION['is_auth']) && $_SESSION['is_auth']){
    $_SESSION['is_auth'] = false;
    success('Success!');
    redirect('index.php',2);
}
