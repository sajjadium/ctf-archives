<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Challenge Submissions</title>
  <style type="text/css">
    html {
      background: linear-gradient(to right, #E0E7FF, #F3E8FF, #FCE7F3)
    }
    body {
      max-width: 56rem;
      margin: auto;
      text-align: center;
      color: #111827;
      font-family: ui-sans-serif, system-ui, sans-serif;
      font-size: 18px;
    }
    h1 {
      font-weight: 800;
      margin-bottom: 3rem;
      font-size: 48px;
    }
    h2 {
      font-size: 30px;
      color: #1F2937;
      font-weight: 600;
      margin-top: 0;
    }
    p {
      margin: 0;
    }
    div {
      border-radius: 0.5rem;
      margin: 2rem;
      background: #FFF;
      text-align: left;
      padding: 32px;
      box-shadow: #0000001A 0px 10px 15px -3px, #0000001A 0px 4px 6px -4px;
    }
    input {
      background: #FFFFFF;
      border-radius: 8px;
      border: 1px solid #D1D5DB;
      padding: 12px 16px;
      margin-top: 2px;
    }
    input[type=submit] {
      background: #4F46E5;
      color: #FFF;
      cursor: pointer;
    }
  </style>
</head>
<body>
<h1>MVM CTF</h1>
<div>
  <h2>Info</h2>
  <p>We here at x3CTF still don't have enough MVM challs so we need you to submit even more. We have already come up with and uploaded a flag for the chall but we still need some other parts such as the challenge itself and a solution for it.</p>
</div>
<div>
  <h2>Submit a Challenge</h2>
  <p>Upload your challenge file, after upload the file will only be accessible to the admin.</p>
  <form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="file" id="file"><br>
    <input type="submit" value="Submit Challenge" name="submit">
  </form>
<?php

if (isset($_FILES['file'])) {
$uploadOk = 1;
$target_dir = "/var/www/html/uploads/";
$target_file = $target_dir . basename($_FILES["file"]["name"]);

if (file_exists($target_file)) {
  echo "Sorry, file already exists.";
  $uploadOk = 0;
}
if ($_FILES["file"]["size"] > 50000) {
  echo "Sorry, your file is too large you need to buy Nitro.";
  $uploadOk = 0;
}
if (!str_ends_with($target_file, '.txt')) {
  echo "Due to exploit you can only upload files with .txt extensions sorry about this but we got hacked last time so we have to check this from now on.";
  $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
  if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {
    echo "The file ". htmlspecialchars( basename( $_FILES["file"]["name"])). " has been uploaded.";
  } else {
    echo "Sorry, there was an error uploading your file.";
  }
}

$old_path = getcwd();
chdir($target_dir);
// make unreadable
shell_exec('chmod 000 *');
chdir($old_path);

}
?>
</div>
</body>
</html>