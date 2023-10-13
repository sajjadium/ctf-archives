<?php
if ($_SESSION['loggedin'] === true && $_POST['csrf'] === $_SESSION['csrf']) {
  session_unset();
}
header('Location: /', true, 303);
