<?php

include 'config.php';

session_unset();
session_destroy();

if(isset($_GET['next']) && is_string($_GET['next'])){
    header('Location: ' . $_GET['next']);
    die();
}
header('Location: /login.php');