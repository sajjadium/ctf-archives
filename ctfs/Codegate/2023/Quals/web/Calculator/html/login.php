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
			"username" => $username,
		);
		$id_check = fetch_row("user", $query);
		if(!$id_check) alert("login fail", "back");

		if($id_check["pw"] !== $pw) alert("login fail", "back");
		
		$_SESSION["idx"] = $id_check["idx"];
		$_SESSION["isAdmin"] = $id_check["isAdmin"];

		alert("login success", "./");
		exit;
	}	
	render_page("login");
?>