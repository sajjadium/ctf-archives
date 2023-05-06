<?php

header("Creators: @CTFCreators");
session_start();
if( $_SESSION['loggedin'] != 1 || $_SESSION['username'] != "admin" ){
	die("You have to be an admin.");
}

$uuid = $_SERVER['HTTP_UUID'];

if( $uuid != "XXXX" ){
	die("UUID is not valid");
}
include 'database.php';
$xml = urldecode($_POST['data']);

$dom = new DOMDocument();
try{
	@$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
}catch (Exception $e){
	echo '';
}
$userInfo = @simplexml_import_dom($dom);
$output = "User Sucessfully Added.";

$user = mysqli_real_escape_string($mysqli, @$userInfo->username);

$sql = "select * from users where username='$user'";

if($result = $mysqli->query($sql)){
	$data = mysqli_fetch_array($result);
	if(@count($data) != 0){
		echo "User is exists";
	}else{
		echo "User is not exists";
	}
}