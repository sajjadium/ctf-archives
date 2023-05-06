<?php
header("Creators: @CTFCreators");

if($_SERVER['REQUEST_METHOD'] != "POST"){
	header("Location: index.php");
}
include 'database.php';
session_start();

$uid = mysqli_real_escape_string($mysqli, $_POST['uid']);
$pwd = md5(mysqli_real_escape_string($mysqli, $_POST['psw']));
$sig = mysqli_real_escape_string($mysqli, $_POST['token']);

$sqlGetTokens = "SELECT token from tokens where uid='$uid'";

$result = $mysqli->query($sqlGetTokens);
$data = mysqli_fetch_array($result);
$sigDB = substr($data[0], 0, 4);

if( $sig == $sigDB ){

	$sqlChange = "UPDATE users SET password='$pwd' where id='$uid'";
	$mysqli->query($sqlChange);
	
	$sqlDelete = "DELETE FROM tokens WHERE uid='$uid'";
	$mysqli->query($sqlDelete);
	
	echo "<script>alert('Password Changed.');window.location.href='/index.php';</script>";

}else{
	echo "<script>alert('Token is invalid.');window.location.href='/index.php';</script>";
}