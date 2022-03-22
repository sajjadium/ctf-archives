<?php
ob_start();
include('config.php');
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>EzCMS</title>
</head>

<body>
<h2>Login platform</h2>
<div>
    <p>Admire love from Dm</p>
    <p>But maybe you need Login first</p>
</div>
<form action="index.php" method="post" enctype="multipart/form-data">
    <label for="file">username：</label>
    <input type="text" name="username" id="username"><br>
    <label for="file">password：</label>
    <input type="password" name="password" id="password"><br>
    <input type="submit" name="login" value="submit">
</form>
</body>
</html>

<?php
error_reporting(0);
if (isset($_POST['username']) && isset($_POST['password'])){
    $username = $_POST['username'];
    $password = $_POST['password'];
    $username = urldecode($username);
    $password = urldecode($password);
    if ($password === "admin"){
        die("u r not admin !!!");
    }

    $_SESSION['username'] = $username;
    $_SESSION['password'] = $password;

    if (login()){
        echo '<script>location.href="upload.php";</script>';
    }
}

ob_end_flush();
?>
