<?php
include_once('include/php_head.php');

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true && $_POST['csrf'] === $_SESSION['csrf']) {
  session_unset();
}
header('Location: /');
exit();
