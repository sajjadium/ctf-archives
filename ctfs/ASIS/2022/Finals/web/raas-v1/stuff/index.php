<?php

if($_SERVER['REMOTE_ADDR'] == '127.0.0.1'){
	die('curl :thonk:');
}

$url = 'http://localhost';
$method = 'GET';
$formParams = [];

if(isset($_GET['url'])){
	$url = $_GET['url'];
}

if(isset($_GET['method'])){
	$method = $_GET['method'];
}

if(isset($_GET['formParams'])){ 
	$formParams = $_GET['formParams'];
}

$cmd = 'curl ';
$cmd .= '--proto -file '; 
$cmd .= escapeshellarg($url).' ';
$cmd .= '-X ';
$cmd .= escapeshellarg($method).' ';


foreach($formParams as $key => $value){
	if(preg_match("/^\w+$/",$key)){
		$cmd .= '-F ';
		$cmd .= escapeshellarg($key.'= '.$value);
	}
}

header('Content-Type: text/plain');
system($cmd);
