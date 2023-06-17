<?php
	include("./config.php");

	if(is_login()) alert("already login", "./");

	$require_params = array("username", "pw");

	if($_POST){
		foreach ($require_params as $key){
			if(!trim($_POST[$key])){
				alert("invalid parameter", "back");
			}

			$$key = trim($_POST[$key]);
		}

		if(!valid_str($username, "username")){
			alert("invalid parameter", "back");
		}
		$pw = md5($pw . __SALT__);

		$query = array(
			"username" => $username
		);

		$dup_check = fetch_row("user", $query, "or");
		if($dup_check) alert("already exist", "back");

		$query = array(
			"username" => $username,
			"pw" => $pw,
			"isAdmin" => "0"
		);

		if(!insert("user", $query)){
			alert("register fail", "back");
		}

		alert("register success", "./");
		exit;
	}	
	render_page("register");
?>