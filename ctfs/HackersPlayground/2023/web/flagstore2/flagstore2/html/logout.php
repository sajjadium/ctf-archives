<?php
    include_once("config.php");
    include_once("auth_service.php");
    session_start();
    request_logout($_SESSION["auth_server"], $CLIENT_ID, $_SESSION["access_token"], $_SESSION["refresh_token"]);
    session_destroy();
    $return_uri = $_GET["return_uri"];
    if($return_uri == null)
        $return_uri = $_SERVER["HTTP_REFERER"];
    header("Location: " . $return_uri);
?>