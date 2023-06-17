<?php
	if(!defined('__MAIN__')) exit('!^_^!');

	define('MAX_SERIALIZED_INPUT_LENGTH', 10240);
	define('MAX_SERIALIZED_ARRAY_LENGTH', 256);
	define('MAX_SERIALIZED_ARRAY_DEPTH', 5);

	
	function render_page($page) {
		$template = __TEMPLATE__ . $page  . '_page.php';

		if(!is_file($template)){
			alert('cant find template file.', 'back');
		}

		include($template);
		exit;
	}

	function alert($msg, $location) {

		$msg = htmlspecialchars($msg, ENT_QUOTES);
		$location = htmlspecialchars($location, ENT_QUOTES);

		if($location === 'back'){
			exit('<script>alert("' . $msg. '"); history.go(-1);</script>');
		}

		exit('<script>alert("' . $msg . '"); location.href="' . $location . '";</script>');
	}

	function valid_str($str, $type) {
		switch (trim($type)) {
			case 'username':
				if(strlen($str) > 30 || preg_match('/[^a-z0-9_]/', $str)) return false;
				break;
			case 'email':
				if(strlen($str) > 50 || !filter_var($str, FILTER_VALIDATE_EMAIL)) return false;
				break;
			default:
				return false;
				break;
		}
		return true;
	}

	function is_login() {
		if($_SESSION['idx']) return true;
		return false;
	}

	function clean_html($str) {
		return htmlspecialchars($str, ENT_QUOTES);
	}

	function clean_sql($str) {
		return addslashes($str);
	}

	function now() {
		return date("Y-m-d H:i:s");
	}

	function verify_pow($prefix, $pow) {
		$pow = intval($pow);
		$result = trim(shell_exec("python3 /tmp/verify_pow.py $prefix $pow"));
		if($result == "success") {
			return true;
		} else {
			return false;
		}
}
?>