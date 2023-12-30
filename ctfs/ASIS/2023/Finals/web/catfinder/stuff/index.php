<?php
if(isset($_GET['q'])){
	header('Content-Type: text/plain');
	$q = $_GET['q'];
	$whitelist = "/^[a-z()`']+$/";
	$blacklist = "/flag|benchmark|sleep/";
	if(
		!preg_match($whitelist,$q) || 
		preg_match($blacklist,$q) || 
		substr_count($q,'(') > 1
	){
		die(':(');
	}
	$mysqli = new mysqli("db","ctf","ctf","ctf");
	$r = $mysqli->query("SELECT 1 FROM cats WHERE name = '{$q}'")->fetch_assoc();
	if($r){
		echo 'Could find a cat with this name wow!!!';
	} else {
		echo "Couldn't find any cat :(";
	}
	$mysqli->close();
	die();
}

highlight_file(__FILE__);

