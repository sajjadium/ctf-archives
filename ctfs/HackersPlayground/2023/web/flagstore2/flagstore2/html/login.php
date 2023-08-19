<?php
    include_once("config.php");
    include_once("auth_service.php");
    session_start();
    
    if (isset($_SESSION["access_token"])) {
        header("Location: /index.php");
        die();
    }

    if(!isset($_GET["auth_server"]))
        die("auth_server is not set.");
    
    if (!str_starts_with($_GET["auth_server"], $AUTH_SERVER)) 
        die("auth_server is not in whitelist.");

    $_SESSION["code_verifier"] = generate_randstring(96);
    $_SESSION["state"] = generate_randstring(16);
    $_SESSION["nonce"] = generate_randstring(16);
    $_SESSION["auth_server"] = $_GET["auth_server"];
    $_SESSION["redirect_uri"] = $BASE_URL . "/callback.php";

    $query_string = "client_id=" . $CLIENT_ID . "&";
    $query_string .= "redirect_uri=" . urlencode($_SESSION["redirect_uri"]) . "&";
    $query_string .= "response_type=code&";
    $query_string .= "scope=openid+email+profile&";
    $query_string .= "state=" . $_SESSION["state"] . "&";
    $query_string .= "nonce=" . $_SESSION["nonce"] . "&";
    $query_string .= "code_challenge=" . generate_pkce_challenge($_SESSION["code_verifier"]) . "&";
    $query_string .= "code_challenge_method=S256";
    $url = $_SESSION["auth_server"] . $PATH_AUTH . "?" . $query_string;
    
    header("Location: " . $url);
?>