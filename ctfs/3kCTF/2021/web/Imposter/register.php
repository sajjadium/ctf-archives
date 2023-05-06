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
	if (strlen($password)<6){
		die('check the password length');
	}
	if (!($check = $conn->prepare("SELECT username FROM Blog_users WHERE username=?")))
		die('Error while registering.');
	if (!($check->bind_param("s", $username)) || !($check->execute()) || !($check->store_result()))
		die('Error while registering.');
	if ($check->num_rows === 0) {
		$check->close();
		if (!($reg = $conn->prepare("INSERT INTO Blog_users (username, password) VALUES (?, ?)")))
			die('Error while registering.');
		if (!($reg->bind_param("ss", $username, $password)) || !($reg->execute()))
			die('Error while registering.');
		$resp = "User Created.";
		$reg->close();
	}
	else {
		$resp = "Username Already Exists.";
	}
	$conn->close();
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Register</title>
	<link rel="stylesheet" type="text/css" href="./css/styles.css" />
</head>
<body>
	<div class="nav-top">
		<ul class="points">
			<li style="border-right: 1px solid white; background-color: #ff2600"><a href="register.php">Register</a></li>
			<li><a href="login.php">Login</a></li>
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
				<input class="button" type="submit" value="Register" />
			</div>
		</form>
	</div>
</body>
</html>
