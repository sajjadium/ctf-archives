<?php
header("Creators: @CTFCreators");
session_start();
$_SESSION['loggedin'] = 0;

if( $_SERVER['REQUEST_METHOD'] != "POST" ){
	header("Location: /index.php");
}

include 'database.php';

$uname = mysqli_real_escape_string($mysqli, $_POST['uname']);
$paswd = md5($_POST['psw']);

$sql = "SELECT * FROM users where username='$uname'";

if( $result = $mysqli->query($sql) ){
	$data = mysqli_fetch_array($result);

	if($data[2] == $paswd){
		$_SESSION['username'] = $data[1];
		$_SESSION['loggedin'] = 1;

		echo "<script>window.location.href='/profile.php';</script>";
	}else{
		echo "<script>window.location.href='/index.php';</script>";
	}
}	