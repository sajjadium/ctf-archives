<?php
	include('./config.php');

	if(is_login()) die('Already Login');

	$require_params = array('username', 'pw');

	if($_POST){
		foreach ($require_params as $key){
			if(!trim($_POST[$key])){
				die('Parameter is empty');
			}

			$$key = trim($_POST[$key]);
		}

		if(!valid_str($username, 'username')){
			die('Invalid Value');
		}
		$pw = md5($pw . __SALT__);

		$query = array(
			'username' => $username,
		);
		$id_check = fetch_row('user', $query);
		if(!$id_check) die('Login Fail');

		if($id_check['pw'] !== $pw) die('Login Fail');

		foreach ($id_check as $key => $value) {
			$_SESSION[$key] = $value;
		}

		die('Success');
		exit;
	}	
	render_page('login');
?>