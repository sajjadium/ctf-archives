<?php

if (!isset($_SESSION['userid'])) {
    header("Location: login.php");
    exit();
} else {
	header("Location: home.php");
}

?>