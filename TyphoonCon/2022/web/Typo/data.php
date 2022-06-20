<?php
header("Creators: @CTFCreators");

session_start();
include 'database.php';

if( $_SESSION['loggedin'] != 1 ){
	die("<script>window.location.href='/index.php';</script>");
}

$uname = $_GET['u'];
$sql = "SELECT email FROM users where username='$uname'";

if( $result = $mysqli->query($sql) ){
	$data = @mysqli_fetch_array($result);
	$email = $data[0];
	echo $email;
}else{
	echo "Erorr";
}