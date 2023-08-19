<?php    
    include_once("http.php");
    $PATH_AUTH = "/realms/sctf/protocol/openid-connect/auth";
    $PATH_TOKEN = "/realms/sctf/protocol/openid-connect/token";
    $PATH_USER_INFO = "/realms/sctf/protocol/openid-connect/userinfo";
    $PATH_LOGOUT = "/realms/sctf/protocol/openid-connect/logout";


    function request_token($auth_server, $client_id, $redirect_uri, $code_verifier, $code) {
        global $PATH_TOKEN;
        $data = [
            "client_id" => $client_id,
            "grant_type" => "authorization_code",
            "redirect_uri" => $redirect_uri,
            "code_verifier" => $code_verifier,
            "code" => $code
        ];
        
        $response = post($auth_server . $PATH_TOKEN, $data);
        return $response;
    }

    function request_refresh($auth_server, $client_id, $refresh_token) {
        global $PATH_TOKEN;
        $data = [
            "client_id" => $client_id,
            "grant_type" => "refresh_token",
            "refresh_token" => $refresh_token
        ];
        $response = post($auth_server . $PATH_TOKEN, $data);
        return $response;
    }

    function request_user_info($auth_server, $access_token) {
        global $PATH_USER_INFO;
        $headers[] = "Authorization: Bearer " . $access_token;
        $response = get($auth_server . $PATH_USER_INFO, $headers);
        $user = json_decode($response, true);
        return $user;
    }

    function request_logout($auth_server, $client_id, $access_token, $refresh_token) {
        global $PATH_LOGOUT;

        $data = [
            "client_id" => $client_id,
            "refresh_token" => $refresh_token
        ];
        $headers[] = "Authorization: Bearer " . $access_token;
        $response = post($auth_server . $PATH_LOGOUT, $data);
        return $response;
    }

    function generate_randstring($len) {
        $code_verifier = "";
        $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        for ($i = 0; $i < $len; $i++) 
            $code_verifier .= $chars[mt_rand(0, strlen($chars) - 1)];
        
        return $code_verifier;
    }

    function generate_pkce_challenge($code_verifier) {
        $hash = hash("sha256", $code_verifier, true);
        $encoded_hash = base64_encode($hash);
        $encoded_hash = str_replace("+", "-", $encoded_hash);
        $encoded_hash = str_replace("/", "_", $encoded_hash);
        $encoded_hash = str_replace("=", "", $encoded_hash);
        return $encoded_hash;
    }

?>