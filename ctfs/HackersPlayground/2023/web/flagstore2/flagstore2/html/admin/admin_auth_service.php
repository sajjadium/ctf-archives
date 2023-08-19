<?php
    include_once("../http.php");

    // reset password
    function request_resetpassword($auth_server, $access_token, $uid, $new_password)
    {
        $PATH_RESET_PASSWORD = "/admin/realms/sctf/users/".$uid."/reset-password";
        $data = [
            "type" => "password", 
            "temporary" => false, 
            "value" => $new_password
        ];
        $headers[] = "Authorization: Bearer " . $access_token;
        $response = put($auth_server . $PATH_RESET_PASSWORD, $data, $headers);
        return $response;
    }
?>