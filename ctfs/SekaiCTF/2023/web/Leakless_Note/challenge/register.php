<?php
    include "db.php";
    header("Cache-Control: no-cache, no-store");
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
        <title>leaklessnote</title>
    </head>
    <body>
        <div>
            <h1>leaklessnote</h1>
            <hr />
            <form method="POST">
                <label for="name">Name</label>
                <input type="text" placeholder="Username" id="name" name="name">
                <br /><br />
                <label for="pass">Password</label>
                <input type="password" placeholder="Password" id="pass" name="pass">
                <br /><br />
                <input class="button-primary" type="submit" value="Register">
            </form>
        </div>
    </body>
</html>