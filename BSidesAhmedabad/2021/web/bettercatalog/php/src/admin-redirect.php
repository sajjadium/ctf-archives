<?php
include "./include/index.php";

if (!isset($_SESSION["user"]) || !$_SESSION["user"]["is_admin"]) {
	send_to_referrer();
}

if (!is_numeric($_GET["id"])) {
	send_to_referrer();
}

$stmt = $pdo->prepare("SELECT * FROM admin_queue WHERE id = :id");
$success = $stmt->execute([ "id" => $_GET["id"] ]);

if (!$success) {
	flash("error", "<em>ZAP!</em> Something went wrong.");
	send_to_referrer();
}

$result = $stmt->fetch();

$stmt = $pdo->prepare("DELETE FROM admin_queue WHERE id = :id");
$success = $stmt->execute([ "id" => $_GET["id"] ]);

if (!$success || $stmt->rowCount() != 1) {
	flash("error", "<em>ZAP!</em> Something went wrong.");
	send_to_referrer();
}

header("Location: /issue.php?id=" . $result["issue_id"]);
exit();
