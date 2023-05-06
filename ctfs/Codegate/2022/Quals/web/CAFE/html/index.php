<?php session_start(); ?>
<?php require_once __DIR__ . '/libs/db.php'; ?>
<?php require_once __DIR__ . '/libs/util.php'; ?>
<?php require_once __DIR__ . '/libs/htmlParser.php'; ?>

<?php define('__MAIN__', 1); ?>
<?php date_default_timezone_set("Asia/Seoul"); ?>
<?php error_reporting(E_ALL); ?>
<?php ini_set('error_reporting', E_ALL); ?>

<?php
  $data = json_decode(file_get_contents('php://input'), true);
  $routes = ['login', 'logout', 'register', 'write', 'read', 'report', 'search'];
  if(empty($_GET['url'])){
    require_once __DIR__ . '/routes/main.php';
  }else if(in_array($_GET['url'], $routes)){
    require_once __DIR__ . '/routes/' . $_GET['url'] . '.php';
  }else{
    require_once __DIR__ . '/routes/404.php';
  }
?> 