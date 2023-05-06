<?php
require_once('config.php');
if(!isset($_SESSION["username"])){
    header("Location: login.php");
}
unset($_SESSION["username"]);
session_destroy();
header("Location: login.php");
?>