<?php
    $server = 'mysql8';
    $username = 'root';
    $password = '[CENSORED]';
    $db = 'main';
    $conn = new mysqli($server, $username, $password, $db);
    if($conn->connect_error){
        die("connect_error: " . $conn->connect_error);
    }
?>