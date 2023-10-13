<?php

function post($api, $data) {
    $options = [
        'http' => [
            'header' => 'Content-type: application/json',
            'method' => 'POST',
            'content' => json_encode($data),
            'ignore_errors' => true
        ]
    ];
    $context = stream_context_create($options);
    $response = file_get_contents($api, false, $context);
    if ($response === false) return false;
    $response = json_decode($response, true);
    return $response;
}

function check_captcha($solution) {
    $data = [
        "solution" => $solution,
        "secret" => getenv("CAPTCHA_APIKEY"),
        "sitekey" => getenv("CAPTCHA_SITEKEY")
    ];
    $response = post("https://api.friendlycaptcha.com/api/v1/siteverify", $data);
    return $response ? $response["success"] : false;
}

function notify_rater($id) {
    $origin = getenv("ORIGIN") ?: "http://localhost";
    $data = [
        "username" => "rater",
        "link" => "$origin/view.php?id=$id",
        "secret" => getenv("SHARED_SECRET") ?: "secret"
    ];
    return post("http://bot/", $data) ?: "Error while starting bot";
}

function notify_admin($url) {
    $data = [
        "username" => "admin",
        "link" => $url,
        "secret" => getenv("SHARED_SECRET") ?: "secret"
    ];
    return post("http://bot/", $data) ?: "Error while starting bot";
}