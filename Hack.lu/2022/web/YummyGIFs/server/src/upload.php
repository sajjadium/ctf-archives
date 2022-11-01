<?php
include_once('include/php_head.php');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  header('HTTP/1.1 405 Method not allowed');
  echo ('405 Method not allowed');
  exit();
}
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true || $_SESSION['user_id'] === 1) { // admin has uploaded enough :)
  header('HTTP/1.1 401 Unauthorized');
  echo ('401 Unauthorized');
  exit();
}
if (!$_POST) {
  header('HTTP/1.1 400 Bad Request');
  echo ('File size exceeded');
  exit();
}
if ($_POST['csrf'] !== $_SESSION['csrf']) {
  header('HTTP/1.1 400 Bad Request');
  echo ($csrf_error);
  exit();
}
if (!is_string($_POST['title']) || !is_string($_POST['description'])) {
  header('HTTP/1.1 400 Bad Request');
  echo ('Bad Request');
  exit();
}

if (
  !isset($_FILES['file']) ||
  $_FILES['file']['error'] !== UPLOAD_ERR_OK ||                           // has upload succeeded?
  !is_string($_FILES['file']['name'])
) {
  header('HTTP/1.1 400 Bad Request');
  echo ('Bad file upload 🤨');
  exit();
}

$_FILES['file']['name'] = trim($_FILES['file']['name']);                  // remove leading whitespace in filename
if (
  !preg_match('/^[[:print:]]{1,200}\.gif$/', $_FILES['file']['name']) ||  // no weird chars in filename
  e($_FILES['file']['name']) !== $_FILES['file']['name'] ||               // no html chars in filename
  str_contains($_FILES['file']['name'], '/') ||                           // path traversal
  pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION) !== "gif" ||      // check if file extension is gif
  $_FILES['file']['type'] !== 'image/gif' ||                              // check if file type is gif
  !is_array(getimagesize($_FILES['file']['tmp_name'])) ||                 // check if file truly is a gif
  !imagecreatefromgif($_FILES['file']['tmp_name'])                        // check if file really truly is a gif
) {
  header('HTTP/1.1 400 Bad Request');
  echo ('Bad file upload 🤨');
  exit();
}

try {
  // move file to unguessable folder
  $random_id = bin2hex(random_bytes(16));
  $upload_dir = __DIR__ . "/uploads/$random_id/";
  if (!is_dir($upload_dir)) {
    mkdir($upload_dir, 0700, true);
  }

  DB::saveGIF($random_id, $_FILES['file']['name'], $_POST['title'], $_POST['description'], $_SESSION['user_id']);
  move_uploaded_file($_FILES['file']['tmp_name'], $upload_dir . $_FILES['file']['name']);
  
  echo ($random_id);
} catch (Exception $e) {
  header('HTTP/1.1 500 Server Error');
  echo ('Server Error: Unsuccessful file upload');
}
