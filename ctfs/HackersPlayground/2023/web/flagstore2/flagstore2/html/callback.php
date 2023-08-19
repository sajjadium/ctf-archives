<?php
    include_once("config.php");
    include_once("auth_service.php");
    session_start();

    if (!isset($_SESSION["auth_server"])) 
        die("auth_server is not set.");
    
    if (!isset($_SESSION["state"]) || $_SESSION["state"] != $_GET["state"])
        die("Invalid state.");
        
    if (!isset($_GET["code"])) 
        die("Invalid code.");

    $res = request_token($_SESSION["auth_server"], $CLIENT_ID, $_SESSION["redirect_uri"], $_SESSION["code_verifier"], $_GET["code"]);
    $res = json_decode($res, true);
    if(!isset($res["access_token"]))
        die("Invalid access token.");

    $user = request_user_info($_SESSION["auth_server"], $res["access_token"]);

    if($user == null)
        die("Invalid access token.");

    $_SESSION["uid"] = $user["sub"];
    $_SESSION["username"] = $user["preferred_username"];
    $_SESSION["access_token"] = $res["access_token"];
    $_SESSION["refresh_token"] = $res["refresh_token"];

    header("Location: /index.php");
?>
