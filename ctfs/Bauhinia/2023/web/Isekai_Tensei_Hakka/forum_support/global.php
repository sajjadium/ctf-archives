<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/01/01
 URL : http://www.2233.idv.tw

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */
// ###################### Start init #######################


// gzip start
$do_gzip_compress = FALSE;
if ($wog_arry["gzip_compress"])
{

	$phpver = phpversion();
	$useragent = (isset($_SERVER["HTTP_USER_AGENT"]) ) ? $_SERVER["HTTP_USER_AGENT"] : $HTTP_USER_AGENT;
	if ( $phpver >= '4.0.4pl1' && ( strstr($useragent,'compatible') || strstr($useragent,'Gecko') ) )
	{
		if ( extension_loaded('zlib') )
		{
			ob_start('ob_gzhandler');
		}
	}
	else if ( $phpver > '4.0' )
	{

		if ( strstr($HTTP_SERVER_VARS['HTTP_ACCEPT_ENCODING'], 'gzip') )
		{
			if ( extension_loaded('zlib') )
			{
				$do_gzip_compress = TRUE;
				ob_start();
				ob_implicit_flush(0);
				header('Content-Encoding: gzip');
			}
		}
	}
}

post_check($_POST);
unset($dbservertype);
//load config
require('./forum_support/config/config.php');
// init db **********************
// load db class
$dbservertype = strtolower($dbservertype);
$dbclassname="./forum_support/config/db_$dbservertype.php";
require($dbclassname);

$DB_site=new DB_Sql_vb;
$DB_site->appname='WOG';
$DB_site->appshortname='WOG';
$DB_site->database=$dbname;

$DB_site->connect($servername, $dbusername, $dbpassword, $usepconnect);
$DB_site->query_first("SET NAMES utf8;"); 
$DB_site->query_first("SET CHARACTER_SET_CLIENT=utf8;"); 
$DB_site->query_first("SET CHARACTER_SET_RESULTS=utf8;");
unset($servername, $dbusername, $dbpassword, $usepconnect);
//$DB_site->connect();
$dbpassword="";
$DB_site->password="";

// end init db
// ###################### Start functions #######################
?>