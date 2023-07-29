<?php
    include "db.php";
    session_start();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST["name"]) && is_string($_POST["name"]) && isset($_POST["pass"]) && is_string($_POST["pass"])) {
            $stmt = $db->prepare("SELECT * FROM users WHERE username=?");
            $stmt->execute([$_POST["name"]]);
            $user = $stmt->fetch();
            
            if ($user) {
                die("A user already exists with that username");
            }

            if (strlen($_POST["name"]) > 32 || strlen($_POST["name"]) < 5) {
                die("Username must be at least 5 characters, and less than 32 characters");
            }

            if (strlen($_POST["pass"]) < 7) {
                die("Password must be at least 7 characters");
            }

            $hash = password_hash($_POST["pass"], PASSWORD_BCRYPT);
            $stmt = $db->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
            $stmt->execute([$_POST["name"], $hash]);

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
                    
                    <input class="button-primary" type="submit" value="Register">
                </fieldset>
            </form>
        </div>
    </body>
</html>