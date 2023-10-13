<?php

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    die("Method not allowed");
}

if (!$_SESSION["loggedin"] || $_SESSION["username"] !== "rater" || !$_SESSION["csrf"] || $_POST["csrf"] !== $_SESSION["csrf"]) {
    http_response_code(403);
    die("Unauthorized");
}

if (!$_POST["url"]) {
    http_response_code(400);
    die("Invalid input");
}

include_once("include/API.php");

$res = notify_admin($_POST["url"]);

if ($res === "ok") {
    $_SESSION["message"] = "The admin will decide the competitor's fate!";
    $_SESSION["message_type"] = "success";
} else if ($res === false) {
    $_SESSION["message"] = "The bot is down. :(";
    $_SESSION["message_type"] = "error";
} else {
    $_SESSION["message"] = $res;
    $_SESSION["message_type"] = "error";
}

header("Location: /", true, 303);