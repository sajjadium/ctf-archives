<?php
include "include/index.php";

if ($_SERVER["REQUEST_METHOD"] != "POST") {
	send_to_referrer();
}

if (!isset($_SESSION["user"])) {
	send_to_referrer();
}

if (!is_string($_POST["title"]) || !is_string($_POST["content"]) || !is_string($_POST["image"]) || $_POST["title"] == "" || $_POST["content"] == "") {
	flash("error", "<em>Zap!</em> Failed to update this issue.");
	send_to_referrer();
}

if (is_numeric($_POST["id"])) {
	$stmt = $pdo->prepare("UPDATE issue SET title = :title, content = :content, image = :image WHERE id = :id AND author_id = :author_id");
	$success = $stmt->execute([ "title" => $_POST["title"], "content" => $_POST["content"], "image" => $_POST["image"], "id" => $_POST["id"], "author_id" => $_SESSION["user"]["id"] ]);

	if ($success) {
		flash("success", "<em>Bam!</em> Issue updated successfully!");
		header("Location: /issue.php?id=" . $_POST["id"]);
		exit();
	} else {
		flash("error", "<em>Zap!</em> Something went wrong.");
		send_to_referrer();
	}
} else {
	$stmt = $pdo->prepare("INSERT INTO issue (title, content, image, author_id) VALUES (:title, :content, :image, :author_id)");
	$success = $stmt->execute([ "title" => $_POST["title"], "content" => $_POST["content"], "image" => $_POST["image"], "author_id" => $_SESSION["user"]["id"] ]);

	if ($success) {
		flash("success", "<em>Bam!</em> Issue created successfully!");
		$stmt = $pdo->prepare("SELECT LAST_INSERT_ID() AS id");
		$stmt->execute();
		header("Location: /issue.php?id=" . $stmt->fetch()["id"]);
		exit();
	} else {
		var_dump($pdo->errorInfo());
		var_dump($success);
		flash("error", "<em>Zap!</em> Something went wrong.");
		send_to_referrer();
	}
}

