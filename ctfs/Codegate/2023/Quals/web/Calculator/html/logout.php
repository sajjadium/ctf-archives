<?php
	include("./config.php");

	if(!is_login()) alert("login plz", "back");

	session_destroy();
	alert("logout", "back");
?>