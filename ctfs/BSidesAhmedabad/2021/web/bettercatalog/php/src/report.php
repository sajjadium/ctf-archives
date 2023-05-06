<?php
include "include/index.php";

if ($_SERVER["REQUEST_METHOD"] != "POST") {
	send_to_referrer();
}

if (!isset($_SESSION["user"]) || !is_numeric($_POST["id"]) || !isset($_POST["token"])) {
	send_to_referrer();
}

$recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify';
$recaptcha_secret = $_ENV["RECAPTCHA_SECRET"];
$recaptcha_response = $_POST["token"];

$recaptcha = json_decode(file_get_contents($recaptcha_url . "?secret=" . $recaptcha_secret . "&response=" . $recaptcha_response));

if ($recaptcha->score < 0.5) {
	flash("error", "<em>ZAP!</em> I'm pretty sure you're a robot");
	send_to_referrer();
}

$stmt = $pdo->prepare("INSERT INTO admin_queue (issue_id) SELECT id FROM issue WHERE id = :id");
$success = $stmt->execute([ "id" => $_POST["id"] ]);

if (!$success || $stmt->rowCount() != 1) {
	flash("error", "<em>ZAP!</em> Failed to submit issue for approval.");
	send_to_referrer();
}

flash("success", "<em>BOOM!</em> Successfully submitted to admin for approval.");
send_to_referrer();

// FIXME: put a captcha check in here somewhere

