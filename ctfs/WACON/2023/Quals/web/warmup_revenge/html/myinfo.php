<?php
	include('./config.php');

	if(!is_login()) die('Plz login');

	if($_POST){
		$replace = array();
		
		if(trim($_POST['pw'])){
			$replace['pw'] = sha1($pw . __SALT__);
		}

		if(trim($_POST['note']) === 'enable'){
			$replace['is_note'] = '1';
		}
		else{
			$replace['is_note'] = '0';	
		}

		$search = array('idx' => $_SESSION['idx']);
		if(update('user', $replace, $search)){
			foreach ($replace as $key => $value) {
				$_SESSION[$key] = clean_sql($value);
			}
			die('Edit Success');
		}
		else{
			die('Error occurred');
		}
		exit;
	}

	render_page('myinfo');
?>