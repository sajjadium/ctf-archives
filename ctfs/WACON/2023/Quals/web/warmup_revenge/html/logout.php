<?php
	include('./config.php');

	if(!is_login()) die('Login Plz');

	session_destroy();
	die('Logout success. Bye~');
?>