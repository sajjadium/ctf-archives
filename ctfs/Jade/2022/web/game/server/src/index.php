<?php
    error_reporting(0);
    include "/var/www/db/secret.php";
    ini_set('default_socket_timeout', 2);
    session_start();    
    function fetch($url) {
        $headers=get_headers($url, 1);
        if($headers && strpos($headers[0],'200')){
            return true;
        }
        else{
            return false;
        }
    }
    if(isset($_POST["username"]) && isset($_POST["password"])){
        $username=$_POST["username"];
        $password=$_POST["password"];
        $concat=$username.$password.$secret;
        $signature=sha1($concat);
        $var="http://api/register.php?username={$username}&password={$password}&signature={$signature}";
        $head=sprintf("API: %s",$var);
        header($head);
        $status=fetch($var);
        if($status===true){
            $database=array();
            $database=unserialize(file_get_contents('/var/www/db/database.bin'));
            $_SESSION['username']=$username;
            echo '<script>window.open("dashboard.php","_self");</script>';
        }
        else{
            echo "<script>alert('Username already exists or incorrect password!');</script>";
        }
    }
?>
<html>
<link rel="stylesheet" type="text/css" href="assets/index.css" />
<script src="assets/index.js"></script>

<form method="post" action="">
  <h2><span class="entypo-login"><i class="fa fa-sign-in"></i></span> Login</h2>
  <button class="submit"><span class="entypo-lock"><i class="fa fa-lock"></i></span></button>
  <span class="entypo-user inputUserIcon">
     <i class="fa fa-user"></i>
   </span>
  <input type="text" class="user" placeholder="username" name="username"/>
  <span class="entypo-key inputPassIcon">
     <i class="fa fa-key"></i>
   </span>
  <input type="password" class="pass"placeholder="password" name="password"/>
</form>




</html>
