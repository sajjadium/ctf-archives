<!DOCTYPE html>
<html>

<head>
    <title>cps test register</title>
</head>

<body>
    <?php
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    if (isset($_POST["username"]) && isset($_POST["password"])) {
        try{
            $mysqli = new mysqli("p:db", "app", "ead549a4a7c448926bfe5d0488e1a736798a9a8ee150418d27414bd02d37b9e5", "cps");
            $result = $mysqli->query(sprintf("INSERT INTO users (username, password) VALUES ('%s', '%s')", $_POST["username"], $_POST["password"]));
            if ($result) {
                $token = bin2hex(random_bytes(16));
                $add_token = $mysqli->query(sprintf("INSERT INTO tokens (token, username) VALUES ('%s', '%s')", $token, $_POST["username"]));
                if ($add_token) {
                    setcookie("token", $token);
                    echo "<p>Successfully created account. You are now logged in</p>";
                }
            } else {
                echo "<p>Something went wrong. Username " + $_POST["username"] + " (might) have been taken already</p>";
            }
        } catch (Exception $e) {
            if (str_starts_with($e, "mysqli_sql_exception: Duplicate entry '") and str_contains($e, "' for key 'PRIMARY'")) {
                echo sprintf("<p>Something went wrong. Username starting with %s has been taken already</p>", substr(explode("' for key", substr($e, 39))[0], 0, 5));
            }
        }

    }
    ?>
    <form action="register.php" method="post">
        <p>username: <input type="text" name="username" /></p>
        <p>password: <input type="password" name="password" /></p>
        <p><input type="submit" value="register" /></p>
    </form>
</body>

</html>