<?php
    error_reporting(0);
    session_start();
    session_destroy();
    header('Location: index.php');
    exit;
?>