<?php

error_reporting(E_ERROR | E_PARSE);

function validate_username($username){
    if(strlen($username) > 32){
        die('{"error":"username too long!"}');
    }
    return $username;
}

function validate_password($password){
    if(strlen($password) > 32){
        die('{"error":"password too long!"}');
    }
    return $password;
}

function validate_email($email){
    if(strlen($email) > 32){
        die('{"error":"email too long!"}');
    }
    return $email;
}

function validate_description($desc){
    $maxlength = 32;
    $finalstring = "";
    // Cut the string at the maxlength character
    for($i = 0; $i < $maxlength; $i++){
        $finalstring = $finalstring . $desc[$i];
    }
    $finalstring = urldecode($finalstring);
    $finalstring = str_replace("<","&lt;",$finalstring);
    $finalstring = str_replace(">","&gt;",$finalstring);

    return $finalstring;
}

function validate_color($color){
    $color = urldecode($color);
    if(strlen($color) > 48){
        die('{"error":"color too long!"}');
    }
    if(preg_match('/[\x00-\x7E]/',$color)){
        if(preg_match('/(\[|\]|\$|\ |\n|\'|\"|\<|\>|\\|\x00|\t|\`|\{|\}|.*on.+=)/',$color)){
            die('{"error":"Invalid character found!"}');
        }
    }else{
        die('{"error":"Invalid character found!"}');
    }
    return $color;
}

function validate_report($report){
    return validate_color($report);
}

?>