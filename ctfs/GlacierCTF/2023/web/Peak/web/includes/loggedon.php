<?php

include_once "session.php";

if(!isset($_SESSION['user']))
{
    $_SESSION['error'] = htmlentities("You need to login to access this resource!");
    header("Location: /login.php");
}