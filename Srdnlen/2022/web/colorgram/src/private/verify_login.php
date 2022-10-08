<?php
    require_once('private/jwt.php');
    require_once('private/mysql.php');

    if(isset($_COOKIE['AUTHKEY'])){
        if(isset($_GET['name'])){
            $name = $_GET['name'];
        }else if(isset($_POST['name'])){
            $name = $_POST['name'];
        }else{
            die('{"error":"Missing name"}');
        }
        $name = urldecode($name);
        
        $varname = validate_jwt($_COOKIE['AUTHKEY']);
        if($varname === ""){
            die('{"error":"invalid authkey"}');
        }else if($varname !== $name && $varname !== 'admin'){
            die('{"error":"you cant see this account"}');
        }
    }else{
        die('{"error":"missing authkey"}');
    }
  
?>