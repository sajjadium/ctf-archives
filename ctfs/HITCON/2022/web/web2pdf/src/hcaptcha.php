<?php

// NOT part of this challenge

function verify_hcaptcha()
{
    if (!isset($_POST['h-captcha-response']))
        return false;

    $data = file_get_contents('https://hcaptcha.com/siteverify', false, stream_context_create(['http' => [
        'method'  => 'POST',
        'header'  => 'Content-Type: application/x-www-form-urlencoded',
        'content' => http_build_query([
            'secret' => $_ENV['HCAPTCHA_SECRET_KEY'],
            'response' => $_POST['h-captcha-response']
        ])
    ]]));
    $data = json_decode($data);
    return $data->success;
}
