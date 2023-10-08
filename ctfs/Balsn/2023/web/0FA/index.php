<?php
include_once("config.php");
?>
<html style="box-shadow:inset 0 0 5rem rgba(0,0,0,.5)">
<head>
<title>Balsn CTF 2023 - 0FA</title>
<meta charset="utf-8">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
</head>
<body style="background-color:#333; padding:100px">
<div class="container">
    <div class="jumbotron">
        <h2 class="title is-2">Login</h2>
        <p class="subtitle is-5">No more password! No more 2FA!</p>
        <hr>
        <form method="post" action="flag.php">
            <div class="field">
                <input type="text" class="input" name="username" placeholder="Username...">
            </div>
            <input type="submit" class="button is-primary"><br>
        </form>
    </div>
    <p style="color: #c7c7c7">balsn 2023</p>
</div>
</body>
</html>
