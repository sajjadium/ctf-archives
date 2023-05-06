<?php

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
require_once(__DIR__ . '/../vendor/autoload.php');
require_once('mysql.php');

define('JWT_SECRET',getenv('JWT_SECRET'));
define('ISS', 'srdnlenctf');
define('HASHING','HS512');

function set_jwt($jwt){
    try{
        $options = array(
            'expires' => time()+3600,
            'httpOnly' => true
        );
        setcookie('AUTHKEY', $jwt, $options);
    }catch(error $e){
        die('{"error":"Cant load authkey cookie correctly"}');
    }
    
}

function generate_jwt($name, $password){
    try{
        $now = strtotime("now");
        $jwt = JWT::encode([
        "iat" => $now, 
        "nbf" => $now, 
        "exp" => $now + 3600, // 1 hour elapse time
        "iss" => ISS,
        "data" => [
            "name" => $name,
            "password" => $password
        ]
        ], JWT_SECRET, HASHING);
        return $jwt;
    }catch(Exception $e){
        die('{"error":"Can\'t generate authkey"}');
    }
}

function validate_jwt($jwt){
    try{
        $token = JWT::decode($jwt, new Key(JWT_SECRET, HASHING));
        $now = new DateTimeImmutable();
        if($token->iss !== ISS || $token->nbf > $now->getTimestamp() || $token->exp < $now->getTimestamp()){
            return "";
        }
        $sql = new MySQLobject();
        if(!$sql->verify_login($token->data->name, $token->data->password)){
            return "";
        }
        return $token->data->name;
    }catch(Exception $e){
        die('{"error":"malformed authkey! '.$e.'"}');
    }
}


?>