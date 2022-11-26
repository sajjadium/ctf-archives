<?php

$turnstile_secret = $_SERVER["TURNSTILE_SECRETKEY"];
$turnstile_sitekey = $_SERVER["TURNSTILE_SITEKEY"];

function verify_turnstile($response) {
    if (!isset($turnstile_secret)) return true;
    
    $curl = curl_init();
    curl_setopt_array($curl, array(
        CURLOPT_URL => "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => array(
            "secret" => $turnstile_secret,
            "response" => $response
        )
    ));

    $result = curl_exec($curl);
    curl_close($curl);

    return json_decode($result, true)["success"];
}


?>