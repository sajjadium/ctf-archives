<!DOCTYPE html>
<html>

<head>
    <title>cps test login</title>
</head>

<body>
    <?php
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    if (isset($_POST["username"]) && isset($_POST["password"])) {
        $mysqli = new mysqli("p:db", "app", "ead549a4a7c448926bfe5d0488e1a736798a9a8ee150418d27414bd02d37b9e5", "cps");
        $stmt = $mysqli->prepare("SELECT username, password FROM users WHERE username = ? AND password = ?");
        $stmt->bind_param("ss", $_POST["username"], $_POST["password"]);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
        if ($row) {
            $token = bin2hex(random_bytes(16));
            $add_token = $mysqli->query(sprintf("INSERT INTO tokens (token, username) VALUES ('%s', '%s')", $token, $_POST["username"]));
            if ($add_token) {
                setcookie("token", $token);
                echo "<p>You are now logged in</p>";
            }
        } else {
            echo "<p>Something went wrong.</p>";
        }

    }
    ?>
    <form action="login.php" method="post">
        <p>username: <input type="text" name="username" /></p>
        <p>password: <input type="password" name="password" /></p>
        <p><input type="submit" value="login" /></p>
    </form>
</body>

</html>