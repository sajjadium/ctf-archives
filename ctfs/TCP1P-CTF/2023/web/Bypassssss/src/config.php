<?php
    $host = "mysql-db";
    $username = "ctf";
    $password = "VeryRandomPassword";
    $databasename = "bypassssss";

    // Create connection
    $conn = mysqli_connect($host, $username, $password, $databasename);

    // Check connection
    if (!$conn) {
        die("Connection failed");
    }
?>