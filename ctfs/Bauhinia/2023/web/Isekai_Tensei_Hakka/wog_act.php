<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/08/28
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

require_once('./forum_support/function.php');
require_once('./language/wog_main_traditional_chinese.php');
require_once('./language/wog_act_traditional_chinese.php');
/*
if(substr(getenv("HTTP_REFERER"),0,26)!="http://www.2233.idv.tw/wog")
{
		alertWindowMsg("請從www.2233.idv.tw登入論壇後再進入遊戲");
}
*/
//error_reporting(7);
if(!isset($_POST["act"]))
{
	$_POST["act"]="";
}
if(!isset($_POST["f"]))
{
	$_POST["f"]="";
}

if( $_POST["f"] != "chara"  && empty($HTTP_COOKIE_VARS["wog_cookie"]))
{
	alertWindowMsg($lang['wog_act_nologin']);
}

require_once("wog_act_config.php");

//session_check($wog_arry["act_dely_time"]);
require_once("./forum_support/global.php");
session_register('act_time');
if ($HTTP_COOKIE_VARS["wog_cookie_name"] != Null || $HTTP_COOKIE_VARS["wog_cookie"] != Null)
{
	if ($HTTP_COOKIE_VARS["wog_cookie_debug"] != md5($HTTP_COOKIE_VARS["wog_cookie"].$HTTP_COOKIE_VARS["wog_bbs_id"].$wog_arry["cookie_debug"])) 
	{ 
		cookie_clean();
		showscript("alert('".$lang['wog_act_check_cookie']."');window.open('../','_top')");
	}
}
//########################## switch case begin #######################
$a_id="";
$temp_ss="";
switch ($_POST["f"])
{
	case "chara":
		if($_POST["act"]=="login" || $_POST["act"]=="make" || $_POST["act"]=="save")
		{
			$p_ip=get_ip();
			eval($forum_check);
			if ($bbs_id<=0) {
				showscript("alert('".$lang['wog_act_nofroum_member']."');window.open('../','_top');");
			}
		}
		include("./class/wog_act_chara.php");
		$wog_act_class = new wog_act_chara;
		switch ($_POST["act"])
		{
			case "login":
				$wog_act_class->login($bbs_id,$p_ip);
			break;
			case "status_view":
				$wog_act_class->show_chara($HTTP_COOKIE_VARS["wog_cookie"],$userid,3);
			break;
			case "make":
				$wog_act_class->chara_make();
			break;
			case "save":
				$wog_act_class->chara_save($bbs_id);
			break;
			case "revive":
				$wog_act_class->revive($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "logout":
				if($HTTP_COOKIE_VARS["wog_cookie"]=="")
				{
					alertWindowMsg($lang['wog_act_nologin']);
				}
				$wog_act_class->logout($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "view2":
				$wog_act_class->system_view2($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "cp":
				$wog_act_class->cp_view();
			break;
			case "kill":
				$wog_act_class->kill();
			break;
		}
	break;
	case "shop":
		include_once("./class/wog_item_tool.php");
		$wog_item_tool = new wog_item_tool;
		include("./class/wog_act_shop.php");
		$wog_act_class = new wog_act_shop;
		switch ($_POST["act"])
		{
			case "view":
				$wog_act_class->shop($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "buy":
				$wog_act_class->buy($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
		unset($wog_item_tool);
	break;
	case "store":
		include("./class/wog_act_store.php");
		$wog_act_class = new wog_act_store;
		switch ($_POST["act"])
		{
			case "hotel":
				$wog_act_class->hotel($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "img":
				$wog_act_class->p_img($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "img2":
				$wog_act_class->p_img2($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "sex":
				alertWindowMsg("此功能關閉");
				$wog_act_class->p_sex($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "bank":
		if($HTTP_COOKIE_VARS["wog_cookie"]=="")
		{
			alertWindowMsg($lang['wog_act_nologin']);
		}
		include("./class/wog_act_store.php");
		$wog_act_class = new wog_act_store;
		switch ($_POST["act"])
		{
			case "view":
				$wog_act_class->bank($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "save":
				$wog_act_class->bank_save($HTTP_COOKIE_VARS["wog_cookie"],$HTTP_COOKIE_VARS["wog_cookie"],$_POST["money"]);
			break;
			case "get":
				$wog_act_class->bank_get($HTTP_COOKIE_VARS["wog_cookie"],$_POST["money"]);
			break;
			case "pay":
				$pay_id=$DB_site->query_first("SELECT p_id FROM wog_player WHERE p_name='".addslashes(htmlspecialchars($_POST["pay_id"]))."'");
				if($pay_id)
				{
					$wog_act_class->bank_save($HTTP_COOKIE_VARS["wog_cookie"],$pay_id[p_id],$_POST["temp_id"]);
				}else
				{
				    alertWindowMsg($lang['wog_act_noid']);
					
				}
				unset($pay_id);
			break;
		}
	break;
	case "arm":
		include_once("./class/wog_item_tool.php");
		$wog_item_tool = new wog_item_tool;
		include("./class/wog_act_arm.php");
		$wog_act_class = new wog_act_arm;
		switch ($_POST["act"])
		{
			case "view":
				$wog_act_class->arm_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "setup":
				$wog_act_class->arm_setup($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "move":
				$wog_act_class->arm_move($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "sale":
				$wog_act_class->arm_sale($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
		unset($wog_item_tool);
	break;
##########----------syn_system_start----------########## 
	case "syn": 
		include_once("./class/wog_item_tool.php");
		$wog_item_tool = new wog_item_tool;
		include("./class/wog_act_syn.php");
		$wog_act_class = new wog_act_syn;
		switch ($_POST["act"]) 
		{
			case "view":
				$wog_act_class->syn_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break; 
			case "purify": 
				$wog_act_class->syn_purify($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "list": 
				$wog_act_class->syn_list($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "detail": 
				$wog_act_class->syn_detail($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "special": 
				$wog_act_class->syn_special($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
		unset($wog_item_tool);
	break;
##########------------syn_system_end-----------##########
	case "job":
		include("./class/wog_act_job.php");
		$wog_act_class = new wog_act_job;
		switch ($_POST["act"])
		{
			case "view": 
				$wog_act_class->job_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "setup": 
				include_once("./class/wog_item_tool.php");
				$wog_item_tool = new wog_item_tool;
				$wog_act_class->job_setup($HTTP_COOKIE_VARS["wog_cookie"],$_POST["temp_id2"]);
				unset($wog_item_tool);
			break;
			case "get_skill": 
				$wog_act_class->s_get($HTTP_COOKIE_VARS["wog_cookie"],$_POST["temp_id2"]);
			break;
		}
	break;
	case "system":
		switch ($_POST["act"])
		{
			case "view1":
				include("./class/wog_act_message.php");
				$wog_act_class = new wog_act_message;
				$wog_act_class->system_view1($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "sale":
		include_once("./class/wog_item_tool.php");
		$wog_item_tool = new wog_item_tool;
		include("./class/wog_act_bid.php");
		$wog_act_class = new wog_act_bid;
		switch ($_POST["act"])
		{
			case "sale":
				$wog_act_class->bid($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "buy":
				if($_POST["stype"]=="0")
				{
					$wog_act_class->sale_buy_item($HTTP_COOKIE_VARS["wog_cookie"]);
				}elseif($_POST["stype"]=="1")
				{
					$wog_act_class->sale_buy_pet($HTTP_COOKIE_VARS["wog_cookie"]);
				}
			break;
		}
		unset($wog_item_tool);
	break;
	case "team":
		include("./class/wog_act_team.php");
		$wog_act_class = new wog_act_team;
		switch ($_POST["act"])
		{
			case "list":
				$wog_act_class->team_list($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "creat":
				$wog_act_class->team_creat($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "status":
				$wog_act_class->team_status($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "support":
				$wog_act_class->team_support($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "join":
				$wog_act_class->team_join($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "del":
				$wog_act_class->team_del($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "leave":
				$wog_act_class->team_leave($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "get_member":
				$wog_act_class->team_get_member($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "get_save_member":
				$wog_act_class->team_get_save_member($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "nosupport":
				$wog_act_class->team_nosupport($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	case "group":
		include("./class/wog_act_group.php");
		$wog_act_class = new wog_act_group;
		switch ($_POST["act"])
		{
			case "join":
				$wog_act_class->group_join($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "creat":
				$wog_act_class->group_creat($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "center":
				$wog_act_class->group_center($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "p_list":
				$wog_act_class->group_peolist($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "number":
				$wog_act_class->group_number($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "up_morale":
				$wog_act_class->group_morale($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "up_number":
				$wog_act_class->group_p_number($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "add":
				$wog_act_class->group_add($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "get_member":
				$wog_act_class->group_get_member($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "get_save_member":
				$wog_act_class->group_get_save_member($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "del":
				$wog_act_class->group_del($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "up_hp":
				$wog_act_class->group_hp($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "up_money":
				$wog_act_class->group_money($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "fire_list_peo":
				$wog_act_class->group_fire_list_peo($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "news":
				$wog_act_class->group_news($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "fire_set":
				$wog_act_class->group_fire_set($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "book":
				$wog_act_class->group_book_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "save_book":
				$wog_act_class->group_book_save($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "pet":
		include("./class/wog_act_pet.php");
		$wog_act_class = new wog_act_pet;
		switch ($_POST["act"])
		{
			case "index":
				$wog_act_class->pet_index($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "ac":
				$wog_act_class->pet_ac($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "eat":
				$wog_act_class->pet_eat($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "fight":
				$wog_act_class->pet_fight($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "sale":
				$wog_act_class->pet_sale($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "chg_st":
				$wog_act_class->pet_chg_st($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "rename":
				$wog_act_class->pet_rename($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "leave":
				$wog_act_class->pet_leave($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "mission":
		include("./class/wog_act_mission.php");
		$wog_act_class = new wog_act_mission;
		switch ($_POST["act"])
		{
			case "1":
				$wog_act_class->mission_list($HTTP_COOKIE_VARS["wog_cookie"],1);
			break;
			case "2":
				$wog_act_class->mission_list($HTTP_COOKIE_VARS["wog_cookie"],2);
			break;
			case "3":
				$wog_act_class->mission_list($HTTP_COOKIE_VARS["wog_cookie"],3);
			break;
			case "4":
				$wog_act_class->mission_list($HTTP_COOKIE_VARS["wog_cookie"],4);
			break;
			case "detail":
				$wog_act_class->mission_detail($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "book":
				$wog_act_class->mission_book($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "get":
				$wog_act_class->mission_get($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "break":
				$wog_act_class->mission_break($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "end":
				include("./class/wog_item_tool.php");
				include("./class/wog_mission_tool.php");
				include("./mission/wog_mission_".$_POST["temp_id"].".php");
				$wog_item_tool= new wog_item_tool;
				$wog_mission_tool= new wog_mission_tool;
				mission_end($HTTP_COOKIE_VARS["wog_cookie"],$_POST["temp_id"]);
				unset($wog_item_tool);
				unset($wog_mission_tool);
			break;
			case "paper":
				$wog_act_class->mission_paper($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "message": // 論壇專用
		include("./class/wog_act_message.php");
		eval($forum_message);
	break;
	case "event":
		event_ans($HTTP_COOKIE_VARS["wog_cookie"]);
	break;
	case "pk":
		include("./class/wog_act_pk.php");
		$wog_act_class = new wog_act_pk;
		switch ($_POST["act"])
		{
			case "view":
				$wog_act_class->pk_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "setup":
				$wog_act_class->pk_setup($HTTP_COOKIE_VARS["wog_cookie"],$_POST["job_id"]);
			break;
		}
	break;
	default:
//		die("不正常操作");
	break;
}
unset($wog_act_class);
if(isset($DB_site))
{
	$DB_site->close();
}
//##################### switch case end #################

//##################### event_ans begin #################
function event_ans($user_id)
{
	global $DB_site,$_POST,$HTTP_SESSION_VARS,$wog_arry,$lang;
	$p=$DB_site->query_first("select p_key,p_attempts,p_lock from wog_player where p_id=".$user_id." ");
	if(!$p)
	{
		alertWindowMsg($lang['wog_act_relogin']);
	}
	if($p["p_lock"]==1)
	{
		alertWindowMsg(sprintf($lang['wog_act_event_lock'],$wog_arry["unfreeze"]));
	}
	if ($_POST["pay_id"] == ""){ 
		if($p["p_attempts"]>$wog_arry["attempts"])
		{
			$DB_site->query("update wog_player set p_lock=1,p_lock_time=".time().",p_attempts=0 where p_id=".$user_id."");
			cookie_clean();
			alertWindowMsg(sprintf($lang['wog_act_event_lock'],$wog_arry["unfreeze"]));
		}else
		{
			$DB_site->query("update wog_player set p_attempts=p_attempts+1 where p_id=".$user_id."");
			alertWindowMsg(sprintf($lang['wog_act_event_err'],($wog_arry["attempts"]-$p["p_attempts"]-1)));
		}
	}
	if($p[p_key]==$_POST["pay_id"])
	{
		$DB_site->query("update wog_player set p_key='',p_attempts=0 where p_id=".$user_id."");
		showscript("alert('".$lang['wog_act_event_ok']."');parent.ad_view()");
	}else
	{
		if($p["p_attempts"]>$wog_arry["attempts"])
		{
			$DB_site->query("update wog_player set p_lock=1,p_lock_time=".time()." where p_id=".$user_id."");
			cookie_clean();
			alertWindowMsg(sprintf($lang['wog_act_event_lock'],$wog_arry["unfreeze"]));
		}else
		{
			$DB_site->query("update wog_player set p_attempts=p_attempts+1 where p_id=".$user_id."");
			alertWindowMsg(sprintf($lang['wog_act_event_err'],($wog_arry["attempts"]-$p["p_attempts"]-1)));
		}
	}
	unset($s);
	unset($packs);
}
/*
//################## item_check ################
function item_check($user_id,$item_id)
{
	global $DB_site,$temp_ss,$lang;
	$sql="select ".check_type($item_id)." from wog_item where p_id=".$user_id."  ";
	$item=$DB_site->query_first($sql);
	if($item[0]=="N/A" || $item[0]=="")
	{
		alertWindowMsg($lang['wog_act_errwork']);
		
	}else
	{
			$items=split(",",$item[0]);
			$adds=split(",",$item_id);
			$s="";
			$s2="";
			for($i=0;$i<count($adds);$i++)
			{
				$s="";
				$chks=false;
				$items=split(",",$item[0]);
				for($j=0;$j<count($items);$j++)
				{
					if($adds[$i]!=$items[$j] || $chks)
					{
						$s.=",".$items[$j];
						
					}else
					{
						$s2.=",".$adds[$i];
						$chks=true;
					}
				}
				$item[0]=substr($s,1,strlen($s));
			}
			if($s2=="")
			{
				alertWindowMsg($lang['wog_act_errdate']);
				
			}
			$s2=substr($s2,1,strlen($s2));//所選擇的東西
			$temp_ss=$item[0];//扣掉選擇後剩下的東西
			return $s2;
	}
	unset($items);
	unset($adds);
	unset($s);
	unset($s2);
	unset($item);
}
*/
compress_exit();
?>