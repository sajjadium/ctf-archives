<?php

if (isset($_POST["submit"])) {
    $uid = $_POST["uid"];
    $pwd = $_POST["pwd"];
    $wh = $_POST["wh"];

    include "../classes/dbh.php";
    include "../classes/signup.class.php";
    include "../classes/login.class.php";

    $signup = new SignupController($uid, $pwd, $wh);

    $signup->signupUser();

    $login = new LoginController($uid, $pwd);

    $login->loginUser();

    header("location: ../home.php");
}

?>