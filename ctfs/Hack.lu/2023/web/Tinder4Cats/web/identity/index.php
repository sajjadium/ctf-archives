<?php

ini_set('session.cookie_httponly', 1);
session_start();


if(!isset($_SESSION['identity'])){
    header('Location: /login.php');
    die('Not logged in.');
}

if (isset($_GET['logout'])) {
    session_destroy();
    session_start();
    header('Location: /login.php');
    die('Logged out.');
}



?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Identity Provider</title>
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🆔</text></svg>">
</head>
<body>
<div class="container">
    <div class="card">            
        <div class="pic">
            <img src="<?= $_SESSION['identity']['picture']; ?>">
        </div>
        <hr>

        <table>
            <tr>
                <td>Name:</td>
                <td><?= $_SESSION['identity']['name']; ?></td>
            </tr>
            <tr>
                <td>Email:</td>
                <td><?= $_SESSION['identity']['email']; ?></td>
            </tr>
            <tr>
                <td>Username:</td>
                <td><?= $_SESSION['identity']['given_name']; ?></td>
            </tr>
        </table>
    
        <hr>
        <div class="buttons">
                <a href="?logout"><button class="logout-button">Logout</button></a>
        </div>
    </div>
</div>
</body>
</html>
