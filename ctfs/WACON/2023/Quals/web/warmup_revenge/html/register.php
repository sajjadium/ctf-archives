<?php
	include('./config.php');

	if(is_login()) die('Already Login');

	$require_params = array('username', 'pw', 'email');

	if($_POST){
		foreach ($require_params as $key){
			if(!trim($_POST[$key])){
				die('Empty value provided');
			}

			$$key = trim($_POST[$key]);
		}

		if(!valid_str($username, 'username') || !valid_str($email, 'email')){
			die('Invalid Value');
		}
		$pw = md5($pw . __SALT__);

		$query = array(
			'username' => $username
		);

		$dup_check = fetch_row('user', $query, 'or');
		if($dup_check) die('already exists');

		$query = array(
			'username' => $username,
			'pw' => $pw,
			'email' => $email,
			'profilebio' => "hi!",
			'level' => '1',
			'point' => '0',
			'is_admin' => '0',
			'is_note' => '1'
		);

		if(!insert('user', $query)){
			die('Fail');
		}

		die('Register success');
		exit;
	}	
	render_page('register');
?>