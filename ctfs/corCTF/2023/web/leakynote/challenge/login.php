<?php
    include "db.php";
    session_start();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST["name"]) && is_string($_POST["name"]) && isset($_POST["pass"]) && is_string($_POST["pass"])) {
            $stmt = $db->prepare("SELECT * FROM users WHERE username=?");
            $stmt->execute([$_POST["name"]]);
            $user = $stmt->fetch();
            
            if (!$user) {
                die("No user exists with that username");
            }

            if (!password_verify($_POST["pass"], $user["password"])) {
                die("Incorrect password");
            }

            $_SESSION["user"] = $_POST["name"];
            header("Location: /index.php");
        }
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width" />
        <meta charset="utf-8" />
        <title>leakynote</title>
        <link rel="stylesheet" href="/assets/normalize.css" />
        <link rel="stylesheet" href="/assets/milligram.css" />
    </head>
    <body>
        <br />
        <div class="container">
            <h1>leakynote</h1>
            <hr />
            <form method="POST">
                <fieldset>
                    <label for="name">Name</label>
                    <input type="text" placeholder="Username" id="name" name="name">

                    <label for="pass">Password</label>
                    <input type="password" placeholder="Password" id="pass" name="pass">
                    
                    <input class="button-primary" type="submit" value="Login">
                </fieldset>
            </form>
        </div>
    </body>
</html>