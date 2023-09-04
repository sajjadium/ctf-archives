<?php
	#error_reporting(E_ALL);
	ini_set( 'display_errors', '0' );
	define('__BASE__', __DIR__);
	define('__TEMPLATE__', __BASE__ . '/templates/');
	define('__MAIN__', true);

	define('__SALT__', '1Na!!ji192.13931293(!!!!');
	session_start();
	
	include('./inc/function.php');

	if(!is_file(__BASE__ . '/config/db.config.php')) die('DB Config Not Found');

	include(__BASE__ . '/config/db.config.php');
	include(__BASE__ . '/inc/db.inc.php');

	if(is_login()){
		if(intval($_SESSION['point']) > 10){
			$_SESSION['level'] = intval($_SESSION['level']) + 1;
			$_SESSION['point'] = 0;

			$query = array(
				'idx' => $_SESSION['idx']				
			);	

			$replace = array(
				'point' => $_SESSION['point'],
				'level' => $_SESSION['level']
			);

			if(!update('user', $replace, $query, 'and')) die('DB Error');
		}
	}

	// global filter
	if(trim($_GET['idx'])){
		if(preg_match('/[^0-9]/', $_GET['idx'])){
			die('Invalid Value');;
		}
	}
	if(trim($_GET['level'])){
		if(preg_match('/[^0-9]/', $_GET['level'])){
			die('Invalid Value');;
		}	
	}
	if(trim($_GET['p'])){
		if(preg_match('/[^a-zA-Z_]/', $_GET['p'])){
			die('Invalid Value');;
		}
	}
	if(trim($_POST['idx'])){
		if(preg_match('/[^0-9]/', $_POST['idx'])){
			die('Invalid Value');;
		}
	}
	if(trim($_POST['level'])){
		if(preg_match('/[^0-9]/', $_POST['level'])){
			die('Invalid Value');;
		}	
	}
	if(trim($_POST['p'])){
		if(preg_match('/[^a-zA-Z_]/', $_POST['p'])){
			die('Invalid Value');;
		}
	}
?>