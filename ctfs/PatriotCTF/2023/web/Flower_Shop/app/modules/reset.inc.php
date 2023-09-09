<?php

if (isset($_POST["submit"])) {
    $uid = $_POST["uid"];
    $token = $_POST["token"];


    include "../classes/dbh.php";
    include "../classes/reset.class.php";

    session_start();
    if (!$token || $token !== $_SESSION['token']) {
        header("location: ../login.php?error=invalidcsrf");
        exit();
    }

    $reset = new ResetController($uid);

    $tmpPwd = $reset->resetPassword();

    header("location: ../login.php?msg=PasswordResetSent");
}

?>