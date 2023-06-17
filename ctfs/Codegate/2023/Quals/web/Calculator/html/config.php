<?php
	error_reporting(0);

	define('__BASE__', __DIR__);
	define('__TEMPLATE__', __BASE__ . '/templates/');
	define('__MAIN__', true);

	define('__SALT__', '1Na!!ji192.13931293(!!!!');
	session_start();
	
	include(__BASE__ . '/inc/function.php');

	if(!is_file(__BASE__ . '/config/db.config.php')) alert('db.config.php 파일이 없습니다.', 'install/index.php');

	include(__BASE__ . '/config/db.config.php');
	include(__BASE__ . '/inc/db.inc.php');
?>