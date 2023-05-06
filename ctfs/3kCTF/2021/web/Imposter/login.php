<?php
session_start();
if (isset($_SESSION["username"])) {
	header("Location: index.php");
	exit(0);
}
if ($_SERVER["REQUEST_METHOD"] === "POST") {
	if (!isset($_POST["username"]) || !isset($_POST["password"]))
		die('Username or Password not set.');
	require("./db/config.php");
	$username = trim($_POST["username"]);
	$password = trim($_POST["password"]);
	if (!($log = $conn->prepare("SELECT * FROM Blog_users WHERE username=? AND password=?")))
		die('Error while logging in.');
	if (!($log->bind_param("ss", $username, $password)) || !($log->execute()) || !($log->store_result()))
			die('Error while logging in.');
	if ($log->num_rows > 0) {
		$_SESSION["username"] = $username;
		header("Location: index.php");
	}
	else {
		$resp = "Bad Credentials.";
	}
	$log->close();
	$conn->close();
}
?>
<!DOCTYPE html>
<html>
<head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Login</title>
        <link rel="stylesheet" type="text/css" href="./css/styles.css" />
</head>
<body>
        <div class="nav-top">
                <ul class="points">
                        <li style="border-right: 1px solid white;"><a href="register.php">Register</a></li>
                        <li style="background-color: #ff2600;"><a href="login.php">Login</a></li>
                </ul>
        </div>
        <div class="main">
		<form method="POST">
			<?php
				if (isset($resp))
					echo "<div><p class=\"resp\">{$resp}</p></div>\r\n";
			?>
			<div class="ftags">
				<label for="user">Username:</label>
				<input class="in" id="user" type="text" name="username" placeholder="Username" />
			</div>
			<div class="ftags">
				<label for="pass">Password:</label>
				<input class="in" id="pass" type="password" name="password" placeholder="Passwd" />
			</div>
			<div class="ftags">
				<input class="button" type="submit" value="Login" />
			</div>
		</form>
		</form>
        </div>
</body>
</html>
