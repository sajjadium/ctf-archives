<?php
  include_once('php_head.php');
  
  $_SESSION['csrf'] = bin2hex(random_bytes(16));
?>
<head>
  <meta charset="utf-8">
  <title>YummyGIFs</title>
  <link rel="stylesheet" href="/static/pico.min.css">
  <link rel="stylesheet" href="/static/styles.css">
</head>