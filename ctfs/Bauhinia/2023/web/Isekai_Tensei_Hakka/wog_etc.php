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

require('./forum_support/function.php');

require_once('./language/wog_main_traditional_chinese.php');
require_once('./language/wog_etc_traditional_chinese.php');

//session_register('act_time');
require("wog_act_config.php");
//session_check($wog_arry["etc_dely_time"]);
require("./forum_support/global.php");
if ($HTTP_COOKIE_VARS["wog_cookie_name"] != Null || $HTTP_COOKIE_VARS["wog_cookie"] != Null)
{
	if ($HTTP_COOKIE_VARS["wog_cookie_debug"] != md5($HTTP_COOKIE_VARS["wog_cookie"].$HTTP_COOKIE_VARS["wog_bbs_id"].$wog_arry["cookie_debug"])) 
	{
		setcookie("wog_cookie",""); 
		setcookie("wog_cookie_name",""); 
		setcookie("wog_bbs_id",""); 
		setcookie("wog_cookie_debug","");
		showscript("alert('".$lang['wog_act_check_cookie']."');window.open('../','_top')");
	}
}
$a_id="";
//###### switch case begin ######

switch ($_GET["f"])
{
	case "peo":
		include("./class/wog_etc_peo.php");
		$wog_act_class = new wog_etc_peo;
		$wog_act_class->peo_view($HTTP_COOKIE_VARS["wog_cookie"]);
	break;
	case "king":
		include("./class/wog_etc_king.php");
		$wog_act_class = new wog_etc_king;
		$wog_act_class->king_view();
	break;
	case "well":
		include("./class/wog_etc_well.php");
		$wog_act_class = new wog_etc_well;
		$wog_act_class->well_view();
	break;
	case "sale":
		include_once("./class/wog_item_tool.php");
		$wog_item_tool = new wog_item_tool;
		include("./class/wog_act_bid.php");
		$wog_act_class = new wog_act_bid;
		$wog_act_class->bid_view();
		unset($wog_item_tool);
	break;
	case "img":
		include("./class/wog_etc_img.php");
		$wog_act_class = new wog_etc_img;
		$wog_act_class->img_view();
	break;
	case "race":
		if($HTTP_COOKIE_VARS["wog_cookie"]=="")
		{
			alertWindowMsg($lang['wog_act_nofroum_member']);
		}
		include("./class/wog_etc_race.php");
		$wog_act_class = new wog_etc_race;
		switch ($_GET["act"])
		{
			case "join":
				$wog_act_class->race_view($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
			case "end":
				$wog_act_class->race_end($HTTP_COOKIE_VARS["wog_cookie"]);
			break;
		}
	break;
	case "password":
		include("./class/wog_act_chara.php");
		$wog_act_class = new wog_act_chara;
		$wog_act_class->get_password($_GET["email"]);
	break;
	case "king_cache":
		include("./class/wog_etc_king_cache.php");
		$wog_act_class = new wog_etc_king_cache;
		$wog_act_class->king_view_cache();
	break;
	case "shop_cache":
		include("./class/wog_act_shop_cache.php");
		$wog_act_class = new wog_act_shop_cache;
		$wog_act_class->shop_cache();
	break;
	case "confirm":
		include("./class/wog_etc_confirm.php");
		$wog_act_class = new wog_etc_confirm;
		$wog_act_class->confirm_view($HTTP_COOKIE_VARS["wog_cookie"]);
	break;
	default:
//		die("不正常操作");
	break;
}
//$HTTP_SESSION_VARS['act_time']=time();
unset($wog_act_class);
if(isset($DB_site))
{
	$DB_site->close();
}
//##### switch case end #####

compress_exit();
?>
