<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);
header("Content-Type: application/json");

function ms_escape_string($data) {
    if ( !isset($data) or empty($data) ) return '';
    if ( is_numeric($data) ) return $data;

    $non_displayables = array(
        '/%0[0-8bcef]/',            
        '/%1[0-9a-f]/',             
        '/[\x00-\x08]/',            
        '/\x0b/',                   
        '/\x0c/',                   
        '/[\x0e-\x1f]/'             
    );
    foreach ( $non_displayables as $regex )
        $data = preg_replace( $regex, '', $data );
    $data = str_replace("'", "''", $data );
    return $data;
}

function save_in_redis()
{
    #todo : save users input on redis to train our waf on it
}

if($_SERVER["REQUEST_METHOD"] === "POST")
{
    $json = file_get_contents("php://input");

    $data = json_decode($json, true);
    $res = "";
    if($data["type"] == "de")
    {
        $res = urldecode(urldecode(base64_decode($data["payload"])));
    }
    else if($data["type"] == "sqli")
    {
        $res = ms_escape_string(base64_decode($data["payload"]));
    }
    else if($data["type"] == "xss")
    {
        $res = htmlentities(base64_decode($data["payload"]));
    }
    else $err = "Invalid type provided.";
    http_response_code(200);
    if(isset($err))
    {
        echo '{"err":"'.$err.'"}';
        die();
    }
    echo '{"ok":"'.base64_encode($res).'"}';
}
else
{
    http_response_code("400");
    echo '{"err":"Invalid HTTP method."}';
}
