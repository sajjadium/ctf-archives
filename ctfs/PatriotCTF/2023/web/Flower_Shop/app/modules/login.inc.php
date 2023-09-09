<?php

if (isset($_POST["submit"])) {
    $uid = $_POST["uid"];
    $pwd = $_POST["pwd"];

    
    include "../classes/dbh.php";
    include "../classes/login.class.php";

    $login = new LoginController($uid, $pwd);

    $login->loginUser();

    header("location: ../home.php");
}

?>