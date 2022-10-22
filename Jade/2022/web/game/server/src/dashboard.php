<?php
    error_reporting(0);
    session_start();
    include '/var/www/db/secret.php';
    include '/var/www/db/flag.php';
    function fetch($url) {
        $headers=get_headers($url, 1);
        if($headers && strpos($headers[0],'200')){
            return true;
        }
        else{
            return false;
        }
    }
    $target=PHP_INT_MAX;
    if(!isset($_SESSION['username'])){
        header("Location: index.php");  
    }
    $username=$_SESSION['username'];
    if(isset($_POST['inc'])){
        $recaptcha = $_POST['g-recaptcha-response'];
        $secret_key = '<<REDACTED>>';
        $url = 'https://www.google.com/recaptcha/api/siteverify?secret='.$secret_key.'&response='.$recaptcha;
        $response = file_get_contents($url);
        $response = json_decode($response);
        if ($response->success===false) {
            die('Captcha failed!');
        }
        $current=$_SESSION['score'];
        $new_score=$current+1;
        $concat=$username.$new_score.$secret;
        $signature=sha1($concat);
        $var="http://api/update_score.php?username={$username}&next_level={$new_score}&signature={$signature}";
        $head=sprintf("API: %s",$var);
        header($head);
        $status=fetch($var);
    }
    $username=$_SESSION['username'];
    $database=array();
    $database=unserialize(file_get_contents('/var/www/db/database.bin'));
    $_SESSION['score']=$database[$username]['score'];
    $score=$_SESSION['score'];
    echo "<center><h2>Welcome user, {$username} <br></h2></center>";
    echo "<center><h2>Your current score : {$score} <br></h2></center>";
    echo "<center><h2>Your target : {$target} <br></h2></center>";
    if($score>=$target){
        echo "<center><h2>Bruh! You have earned it {$flag}</h2></center>";
    }
?>
<link rel="stylesheet" type="text/css" href="assets/index.css" />
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
<style>
.g-recaptcha{
    margin: 15px auto !important;
    width: auto !important;
    height: auto !important;
    text-align: -webkit-center;
    text-align: -moz-center;
    text-align: -o-center;
    text-align: -ms-center;
    }
</style>
<center>
<form action="" method="POST">
    <input type="submit" name="inc" value="inc"/>
    <div class="g-recaptcha" data-sitekey="<<REDACTED>>"></div> 
</form>

<a href="logout.php" style="text-decoration: none;"><input type="button" value="Logout"/></a>
</center>
