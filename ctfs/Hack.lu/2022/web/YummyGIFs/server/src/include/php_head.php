<?php
include_once('DB.php');
function e($str)
{
  return htmlspecialchars($str, ENT_QUOTES | ENT_HTML5);
}
function s($input_str)
{
  $allowed_tags = ['<b>', '</b>', '<i>', '</i>', '<u>', '</u>', '<s>', '</s>', '<br>'];
  $current_str = $input_str;
  while (true) {
    $new_str = preg_replace_callback('/<.*?>/', function ($matches) use ($allowed_tags) {
      return in_array($matches[0], $allowed_tags) ? $matches[0] : '';
    }, $current_str);
    if ($new_str === $current_str) {
      return $new_str;
    }
    $current_str = $new_str;
  }
}

@session_start();

$csrf_error = 'Wrong CSRF token 🤨';
$success = isset($_GET['success']) ? $_GET['success'] : "";
$error = isset($_GET['error']) ? $_GET['error'] : "";
