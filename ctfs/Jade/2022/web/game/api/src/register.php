<?php
    error_reporting(0);
    include "/var/www/db/secret.php";
    $database=array();
    $database=unserialize(file_get_contents('/var/www/db/database.bin'));
    if(isset($_GET["username"]) && isset($_GET["password"]) && isset($_GET["signature"])){
        $username=$_GET["username"];
        $password=$_GET["password"];
        $signature=$_GET["signature"];
        $concatenated=$username.$password.$secret;
        $computed=sha1($concatenated);
        if($signature===$computed && !array_key_exists($username,$database)){
            $entry=array();
            $entry['password']=$password;
            $entry['score']=0;
            $database[$username]=$entry;
            file_put_contents('/var/www/db/database.bin', serialize($database));
            http_response_code(200);
        }
        else if($signature===$computed && array_key_exists($username,$database)){
            if($password===$database[$username]['password']){
                http_response_code(200);
            }
            else{
                http_response_code(404);
            }
        }
        else{
            http_response_code(404);
        }
    }
    else{
        http_response_code(404);
    }
?>