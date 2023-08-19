<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2001/01/21
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

require_once('./forum_support/function.php');
require_once('./language/wog_main_traditional_chinese.php');
require_once('./language/wog_fight_traditional_chinese.php');
/*
if(substr(getenv("HTTP_REFERER"),0,39)!="http://www.2233.idv.tw/wog/wog_foot.htm")
{
	if(substr(getenv("HTTP_REFERER"),0,31)!="http://www.2233.idv.tw/wog/wog_")
	{
		alertWindowMsg("請從www.2233.idv.tw登入論壇後再進入遊戲");
	}
}
*/
if($HTTP_COOKIE_VARS["wog_cookie"]=="")
{
	alertWindowMsg($lang['wog_act_nologin']);
}
//error_reporting(7);

require_once("wog_act_config.php");
require_once("./forum_support/global.php");
session_register('act_time');
session_check($wog_arry["f_time"],3);
if ($HTTP_COOKIE_VARS["wog_cookie_name"] != Null || $HTTP_COOKIE_VARS["wog_cookie"] != Null)
{
	if ($HTTP_COOKIE_VARS["wog_cookie_debug"] != md5($HTTP_COOKIE_VARS["wog_cookie"].$HTTP_COOKIE_VARS["wog_bbs_id"].$wog_arry["cookie_debug"])) 
	{ 
		cookie_clean();
		showscript("alert('".$lang['wog_act_check_cookie']."');window.open('../','_top')");
	}
}
include("./class/wog_fight_event.php");
$wog_event_class = new wog_fight_event;

if(!isset($_POST["act"]))
{
	$_POST["act"]="";
}

if(!isset($_POST["f"]))
{
	$_POST["f"]="";
}

if(!isset($_POST["temp_id3"]))
{
	$_POST["temp_id3"]="20";
}

//Gen Code SETTING 



//########################## switch case begin #######################
if(empty($HTTP_COOKIE_VARS["wog_bbs_id"]))
{
	alertWindowMsg($lang['wog_act_nofroum_member']);
}
/*
if(!empty($forum_message))
{
	$datecut = time() - $wog_arry["offline_time"];
	$online=$DB_site->query_first("select p_name from wog_player where p_online_time > $datecut and p_id<>".$HTTP_COOKIE_VARS["wog_cookie"]." and p_bbsid=".$HTTP_COOKIE_VARS["wog_bbs_id"]."");
	if($online)
	{
		setcookie("wog_cookie","");
		setcookie("wog_cookie_name","");
		setcookie("wog_bbs_id","");
		showscript("alert('".$lang['wog_act_logined']."');window.open('../','_top')");
	}
}
*/
if($_POST["temp_id3"] > 40)
{
	$wog_arry["f_count"]=40;
}else
{
	$wog_arry["f_count"]=(int)$_POST["temp_id3"];
}
if($_POST["temp_id4"] > 100 || $_POST["temp_id4"] < 0)
{
	$wog_arry["f_hp"]=0.15;
}else
{
	$wog_arry["f_hp"]=(int)$_POST["temp_id4"]/100;
}
echo charset();
switch ($_POST["f"])
{
	case "fire":
		include("./class/wog_fight_select.php");
		switch ($_POST["temp_id"])
		{
			case "0":
				include_once("./class/wog_item_tool.php");
				$wog_item_tool = new wog_item_tool;
				require_once("./class/wog_fight_m.php");
				$wogclass = new wog;
				$wogclass->win=0;
				$wogclass->lost=0;
				$wogclass->f_count=$wog_arry["f_count"];
				$wogclass->f_hp=$wog_arry["f_hp"];
				fire($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "1":
				require_once("./class/wog_fight_m.php");
				$wogclass = new wog;
				$wogclass->win=0;
				$wogclass->lost=0;
				$wogclass->f_count=$wog_arry["f_count"];
				switch ($_POST["act"])
				{
					case "20":
						fire_cp($HTTP_COOKIE_VARS["wog_cookie"]);
					break;
					case "21":
						fire_pk($HTTP_COOKIE_VARS["wog_cookie"]);
					break;
					case "22":
						alertWindowMsg("暫不開放");
//						fire_a($HTTP_COOKIE_VARS["wog_cookie"]);
					break;
				}
			break;
			case "2":
				require_once("./class/wog_fight_g.php");
				$wogclass = new wog;
				$wogclass->win=0;
				$wogclass->lost=0;
				$wogclass->f_count=$wog_arry["g_f_count"];
				fire_group($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	default:
//		die("不正常操作");
	break;
}
unset($wog_event_class);
unset($wog_act_class);
if(isset($DB_site))
{
	$DB_site->close();
}

//########################## switch case end #######################

//###########  fire   ##########

function fire($user_id)
{
	global $DB_site,$_POST,$HTTP_COOKIE_VARS;
	$mission_id=0;
	$m_monster_id=0;
	$m_kill_num=0;
	if($_POST["act"]==$HTTP_COOKIE_VARS["wog_cookie_mission_area"])
	{
		$mission_id=$HTTP_COOKIE_VARS["wog_cookie_mission_id"];
		$sql="select a.m_monster_id,b.m_kill_num,a.m_kill_num as m_need_num from wog_mission_main a,wog_mission_book b where b.p_id=".$user_id." and b.m_id=".$mission_id." and b.m_status=0 and a.m_id=b.m_id";

		$m_item=$DB_site->query_first($sql);
		if(!$m_item)
		{
			setcookie("wog_cookie_mission_id",0);
			setcookie("wog_cookie_mission_area",0);
			$mission_id=0;
		}else
		{
			if($m_item["m_kill_num"]==0)
			{
				setcookie("wog_cookie_mission_id",0);
				setcookie("wog_cookie_mission_area",0);
				$sql="update wog_mission_book set m_status=1 where p_id=".$user_id." and m_id=".$mission_id." ";
				$DB_site->query($sql);
				$mission_id=0;
			}else
			{
				$m_monster_id=$m_item["m_monster_id"];
				$m_kill_num=$m_item["m_kill_num"];
			}
		}
	}
	$wog_act_class = new wog_fight_select;
	$wog_act_class->fire($user_id,$mission_id,$m_monster_id,$m_kill_num,$m_item["m_need_num"]);
}

//############  fire cp   ###########

function fire_cp($user_id)
{
	$wog_act_class = new wog_fight_select;
	$wog_act_class->fire_cp($user_id);
}

//############  fire pk   ###########
function fire_pk($user_id)
{
	$wog_act_class = new wog_fight_select;
	$wog_act_class->fire_pk($user_id);
}

//###############  fire a   ############
function fire_a($user_id)
{
	$wog_act_class = new wog_fight_select;
	$wog_act_class->fire_a($user_id);
}
//##########  fire group   #########
function fire_group($user_id)
{
	$wog_act_class = new wog_fight_select;
	$wog_act_class->fire_group($user_id);
}

//###### this php end ######
echo "</script>\n";
compress_exit();
?>
