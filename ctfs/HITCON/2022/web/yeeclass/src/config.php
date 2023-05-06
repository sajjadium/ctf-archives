<?php

ini_set('display_errors', 0);
ini_set('display_startup_errors', 0);
error_reporting(E_ERROR);

define("PERM_STUDENT", -1);
define("PERM_TA", 0);
define("PERM_TEACHER", 1);

if (!session_id()) {
    session_start();
}

$pdo = new PDO("mysql:host=database;dbname=yeeclass;charset=utf8mb4", "yeeclass", "yeeclass");

?>