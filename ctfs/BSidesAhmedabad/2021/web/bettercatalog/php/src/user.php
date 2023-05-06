<?php

include "include/index.php";

if ($_SERVER["REQUEST_METHOD"] != "POST") {
	send_to_referrer();
}

if (!is_string($_POST["action"])) {
	send_to_referrer();
}

if ($_POST["action"] == "logout") {
	session_unset();
	flash("success", "<em>Pow!</em> You are now logged out.");
	send_to_referrer();
}

if (!is_string($_POST["username"]) || !is_string($_POST["password"])) {
	flash("error", "<em>Zap!</em> Missing username or password.");
	send_to_referrer();
}

if ($_POST["username"] == "" || $_POST["password"] == "") {
	flash("error", "<em>Zap!</em> Missing username or password.");
	send_to_referrer();
}

if ($_POST["action"] == "login") {
	$stmt = $pdo->prepare("SELECT * FROM user WHERE username = :username");
	$stmt->execute(["username" => $_POST["username"]]);
	$user = $stmt->fetch();

	if ($user && password_verify($_POST["password"], $user["password"])) {
		flash("success", "<em>Boom!</em> Successfully logged in as <b>{$_POST["username"]}</b>!");
		$_SESSION["user"] = $user;
	} else {
		flash("error", "<em>Zap!</em> Incorrect password for user <b>{$_POST["username"]}</b>.");
	}

	send_to_referrer();
} else if ($_POST["action"] == "register") {
	if (!preg_match('/^[A-Za-z0-9_-]{1,24}$/', $_POST["username"])) {
		flash("error", "<em>Bang!</em> Invalid username.");
		send_to_referrer();
	}

	$stmt = $pdo->prepare("INSERT INTO user (username, password) VALUES (:username, :password)");
	$ok = $stmt->execute(["username" => $_POST["username"], "password" => password_hash($_POST["password"], PASSWORD_BCRYPT)]);

	if ($ok) {
		$user_id = $pdo->lastInsertId();
		$stmt = $pdo->prepare("SELECT * FROM user WHERE id = :id");
		$stmt->execute(["id" => $user_id]);
		$user = $stmt->fetch();

		if ($user) {
			flash("success", "<em>Wham!</em> Thanks for joining, <b>{$_POST["username"]}</b>!");
			$_SESSION["user"] = $user;
		} else {
			$ok = false;
		}
	}

	if (!$ok) {
		flash("error", "<em>Zap!</em> Something went wrong.  Perhaps try a different username?");
	}

	send_to_referrer();
} else {
	send_to_referrer();
}
