<?php
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    die("Method not allowed");
}

if ($_SESSION["loggedin"]) {
    http_response_code(403);
    die("Staff members and their family are not allowed to participate in the competition. You should know this >:(");
}

include_once("include/API.php");

// only check captcha in production
if (getenv("CAPTCHA_APIKEY") && getenv("CAPTCHA_SITEKEY")) {
    if (!is_string($_POST["captcha-solution"]) || !check_captcha($_POST["captcha-solution"])) {
        $_SESSION["message"] = "Invalid captcha";
        $_SESSION["message_type"] = "error";
        header("Location: /", true, 303);
        die("Invalid captcha");
    }
}

if (!is_string($_POST["css"]) || !is_string($_POST["email"]) || strlen($_POST["css"]) > 10000 || strlen($_POST["email"]) > 100) {
    $_SESSION["message"] = "Invalid submission";
    $_SESSION["message_type"] = "error";
    header("Location: /", true, 303);
    die("Invalid submission");
}

include_once("include/DB.php");
$id = insert_submission($_POST["css"], $_POST["email"]);
if (!$id) {
    $_SESSION["message"] = "Server error - submission not saved";
    $_SESSION["message_type"] = "error";
    header("Location: /", true, 303);
    die("Server error");
}

$res = notify_rater($id);
if ($res === "ok") {
    $_SESSION["message"] = "Submission received! One of our expert stylists will rate it soon.";
    $_SESSION["message_type"] = "success";
} else if ($res === false) {
    $_SESSION["message"] = "The bot is down. :(";
    $_SESSION["message_type"] = "error";
} else {
    $_SESSION["message"] = $res;
    $_SESSION["message_type"] = "error";
}
header("Location: /view.php?id=$id", true, 303);