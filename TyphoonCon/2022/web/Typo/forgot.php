<?php

header("Creators: @CTFCreators");

include 'database.php';

if($_SERVER['REQUEST_METHOD'] == "POST"){
	$uname = mysqli_real_escape_string($mysqli, $_POST['uname']);
	$s = system("date +%s%3N > /tmp/time");
	$time = file_get_contents("/tmp/time");
	$fullToken = md5( $unam . $time . "SECRET" );

	$sqlGetId = "SELECT id FROM users where username='$uname'";
	$result = $mysqli->query($sqlGetId);
	$data = mysqli_fetch_array($result);
	$uid = $data[0];

	$sqlDelete = "DELETE FROM tokens WHERE uid='$uid'";
	$mysqli->query($sqlDelete);

	$sqlInsert = "INSERT INTO tokens values('$uid','$fullToken')";
	$mysqli->query($sqlInsert);

	die("<script>alert('Token sent to you.');window.location.href='/index.php';</script>");

}

$valid = 0;

if($_SERVER['REQUEST_METHOD'] == "GET"){
	if ( isset($_GET['id'] ) && isset($_GET['sig']) ){
		$uid = mysqli_real_escape_string($mysqli, $_GET['id']);
		$sql = "SELECT token from tokens where uid='$uid'";
		
		$result = $mysqli->query($sql);
		$data = mysqli_fetch_array($result);
		$sig = substr($data[0],0,4);
		
		if($sig == substr($_GET['sig'],0,4)){
			$valid = 1;
		}
	}else{
		die("<script>alert('Missing headers (sig,id)')</script>");
	}
}

if( $valid == 1){
	echo '<!DOCTYPE html><html><head>	<meta charset="utf-8">	<meta name="viewport" content="width=device-width, initial-scale=1">	<link rel="stylesheet" type="text/css" href="./css/CTFCreators.css">	<title>Forgot Password</title></head><body><div id="id01" class="">    <form class="modal-content animate" action="/change.php" method="post">    <div class="imgcontainer">      <span onclick="document.getElementById(\'id01\').style.display=\'none\'" class="close" title="Close Modal">&times;</span>    </div>    <div class="container">      <label for="psw"><b>Password</b></label>      <input type="password" placeholder="Enter New Password" name="psw" required>            <input type="hidden" name="uid" value="'.htmlspecialchars($_GET['id']).'">      <input type="hidden" name="token" value="'.htmlspecialchars($_GET['sig']).'">      <button type="submit">Change</button>    </div>    <div class="container" style="background-color:#f1f1f1">      <button type="button" onclick="document.getElementById(\'id01\').style.display=\'none\'" class="cancelbtn">Cancel</button>    </div>  </form></div></body></html>';
}else{
	die("<script>alert('Not valid token.')</script>");
}