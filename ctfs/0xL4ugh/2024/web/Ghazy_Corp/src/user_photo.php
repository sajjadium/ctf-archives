<?php
session_start();
error_reporting(0);
require_once('rate-limiting.php');

if(!isset($_SESSION['user_id'])||!isset($_SESSION['role'])||$_SESSION['role']!=="admin" )
{
    die("Not Authorized");
}
echo "Still Under Development<Br>";
if(!empty($_POST['img']))
{
    $name=$_POST['img'];
    $content=file_get_contents($name);
    if(bin2hex(substr($content,1,3))==="89504e47") // PNG magic bytes
    {
        echo "<img src=data:base64,".base64_encode($content);
    }
    else
    {
        echo "Not allowed";
    }
}


?>