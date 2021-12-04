<?php
  session_start();

  if (isset($_GET['theme'])) {
    $_SESSION['theme'] = $_GET['theme'];
  }

  header('Location: /');
  die();
?>
