<?php
	if(!defined('__MAIN__')) exit('!^_^!');

	header("Content-Security-Policy: default-src 'self'; style-src 'self' https://stackpath.bootstrapcdn.com 'unsafe-inline'; script-src 'self'; img-src data:");
	function render_page($page) {
		$template = __TEMPLATE__ . $page  . '_page.php';

		if(!is_file($template)){
			die('Not Found, Plz contact admin');
		}

		include($template);
		exit;
	}

	function upperorlower($str,$mode="upper") {
		if($mode == "upper") {
			if(mb_detect_encoding($str) == "UTF-8") {
				return mb_strtoupper($str);
			} else {
				return strtoupper($str);
			}
		} else {
			if(mb_detect_encoding($str) == "UTF-8") {
				return mb_strtolower($str);
			} else {
				return strtolower($str);
			}
		}
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

?>