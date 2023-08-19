<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2004/01/23
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

// wog show java script
function alertWindowMsg($theMsg,$theURL = "default",$s_save=1) {
	global $DB_site,$HTTP_SESSION_VARS;
	if(isset($DB_site))
	{
		$DB_site->close();
	}
	echo "<html>\n<head>\n";
	echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">";
	echo "<script language=\"JavaScript\">\n";
	echo "alert(\"$theMsg\")\n";
	if ($theURL != "default") {
		echo "document.URL = '" . $theURL . "'\n";
	} 
	echo "</script>\n</head>\n<body></body>\n</html>\n";
/*	if($s_save)
	{
		$HTTP_SESSION_VARS['act_time']=time();
	}
*/
	compress_exit();		// EXIT here!
}

// wog show java script
function showscript($temp_s) {
	global $DB_site,$HTTP_SESSION_VARS,$wog_arry,$HTTP_SERVER_VARS,$HTTP_USER_AGENT;
	if(isset($DB_site))
	{
		$DB_site->close();
	}
	echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">";
	echo "<script language=\"JavaScript\">\n";
	echo $temp_s.";\n";
	echo "</script>\n";
//	$HTTP_SESSION_VARS['act_time']=time();
	compress_exit();		// EXIT here!
}

function charset() {
	return "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">";
}
//################## check_type begin ################
function check_type($temp_id,$type=0)
{
	global $a_id,$DB_site;
	if($type==0)
	{
		$arm_main=$DB_site->query_first("select d_type from wog_df where d_id=".$temp_id);
		if(!$arm_main)
		{
			alertWindowMsg("無此物品");
		}
		$temp_id=$arm_main[0];
	}
	$temp["a_id"]=type_name($temp_id);
	$a_id=$temp["a_id"];
	return $temp["a_id"];
	unset($temp);
}

function type_name($temp_id)
{
	switch($temp_id)
	{
		case "0":
			return "a_id";
		break;
		case "1":
			return "d_head_id";
		break;
		case "2":
			return "d_body_id";
		break;
		case "3":
			return "d_hand_id";
		break;
		case "4":
			return "d_foot_id";
		break;
		case "5":
			return "d_item_id";
		break;
		case "5,6":
			return "d_item_id";
		break;
		case "6":
			return "d_item_id";
		break;
		default:
			alertWindowMsg("無此物品");
		break;
	}
}

//######## post_check begin #########

function post_check($post)
{
	global $HTTP_COOKIE_VARS;
	foreach ($post as $v) {
		if(is_array($v))
		{
			for($i=0;$i<count($v);$i++)
			{
				if(eregi("[<>'\";\]", $v[$i]))
				{
					alertWindowMsg("有不正常符號(1)");
				}
			}
		}else
		{
			if(eregi("[<>'\";\]", $v))
			{
				alertWindowMsg("有不正常符號(1)");
			}
		}
	}
	if(isset($HTTP_COOKIE_VARS["wog_cookie"]))
	{
//		if(eregi("[<>'\";\]",$HTTP_COOKIE_VARS["wog_cookie"]))
		if(!is_numeric($HTTP_COOKIE_VARS["wog_cookie"]))
		{
			alertWindowMsg("有不正常符號(2)");
		}
	}
	if(isset($HTTP_COOKIE_VARS["wog_bbs_id"]))
	{
//		if(eregi("[<>'\";\]",$HTTP_COOKIE_VARS["wog_bbs_id"]))
		if(!is_numeric($HTTP_COOKIE_VARS["wog_bbs_id"]))
		{
			alertWindowMsg("有不正常符號(3)");
		}
	}
}

//######### player_age begin ############ 

function player_age($p_cdate,$day)
{
	return floor((time()-$p_cdate)/($day*24*60*60));
}

//######### cookie_clean begin ############ 

function cookie_clean()
{
	global $HTTP_COOKIE_VARS;
	setcookie("wog_cookie",""); 
	setcookie("wog_cookie_name",""); 
	setcookie("wog_bbs_id",""); 
	setcookie("wog_cookie_debug","");
	setcookie("wog_cookie_mission_id",0);
	setcookie("wog_cookie_mission_area",0);
}

//######### get_ip begin ############ phpbb論壇專用

function get_ip()
{
	global $HTTP_SERVER_VARS,$HTTP_ENV_VARS,$REMOTE_ADDR;
	$client_ip = ( !empty($HTTP_SERVER_VARS['REMOTE_ADDR']) ) ? $HTTP_SERVER_VARS['REMOTE_ADDR'] : ( ( !empty($HTTP_ENV_VARS['REMOTE_ADDR']) ) ? $HTTP_ENV_VARS['REMOTE_ADDR'] : getenv('REMOTE_ADDR') );
	return $client_ip;
}

//########## session_check begin ##########

function session_check($time,$check_type)
{
	global $HTTP_SESSION_VARS,$_GET,$_POST;
	if(isset($HTTP_SESSION_VARS["act_time"]))
	{
		$check_time=$HTTP_SESSION_VARS["act_time"];
		if((time()-$check_time)<$time)
		{
			if($_POST["act"]!="22")
			{
				alertWindowMsg("請等完 : ".$time."秒","default",0);
			}else
			{
				alertWindowMsg("請等完 : 3秒","default",0);
			}
		}else
		{
			$HTTP_SESSION_VARS["act_time"]=time();
		}
	}else
	{
		$HTTP_SESSION_VARS["act_time"]=time();
	}
/*
	if($_GET["f"]=="peo")
	{
		if((time()-$HTTP_SESSION_VARS["act_time"])<$time)
		{
			showscript("parent.no_onlinelist()");
		}
	}
*/
}

function compress_exit($str="")
{
	global $do_gzip_compress;
	if ( $do_gzip_compress )
	{
//
// Borrowed from php.net!
//
		$gzip_contents = ob_get_contents();
		ob_end_clean();
		$gzip_size = strlen($gzip_contents);
		$gzip_crc = crc32($gzip_contents);
		$gzip_contents = gzcompress($gzip_contents, 9);
		$gzip_contents = substr($gzip_contents, 0, strlen($gzip_contents) - 4);
		echo "\x1f\x8b\x08\x00\x00\x00\x00\x00";
		echo $gzip_contents;
		echo pack('V', $gzip_crc);
		echo pack('V', $gzip_size);
	}
	exit;
}
?>
