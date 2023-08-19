<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/10/06
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

class wog_act_store{

	function hotel($user_id)
	{
		global $DB_site,$wog_arry,$lang,$HTTP_SESSION_VARS;
		$have_price=$DB_site->query_first("select p_money,p_lv,p_hp,p_hpmax,p_win,p_lost,p_au from wog_player where p_id=".$user_id."");
		if($have_price[p_lv] > 50)
		{
			$slv=1;
			$have_price[p_hpmax]=$have_price[p_hpmax]-($have_price[p_au]*2);
			if($have_price[p_hp]>$have_price[p_hpmax])
			{
				$have_price[p_hp]=$have_price[p_hpmax];
			}
			if($have_price[p_hp]<=0)
			{
				$slv=5;
				$hotel_time=$wog_arry["hotel_die_time"];
			}else
			{
				if(($have_price[p_hpmax]/10) > $have_price[p_hp])
				{
					$slv=3;
				}else
				{
					$slv=2*(($have_price[p_hpmax]-$have_price[p_hp])/$have_price[p_hpmax]);
				}
				$hotel_time=$wog_arry["hotel_time"];
			}
			$mmoney=round($wog_arry["hotel_money"]*$have_price[p_lv]*$slv);
			if($mmoney < ($wog_arry["hotel_money"]*$have_price[p_lv]))
			{
				$mmoney=$wog_arry["hotel_money"]*$have_price[p_lv];
			}
			if($have_price[p_money] < $mmoney)
			{
				alertWindowMsg(sprintf($lang['wog_act_nomoney_must'], $mmoney));
				
			}else
			{
				$DB_site->query("update wog_player set p_money=p_money-".$mmoney.",p_hp=p_hpmax where p_id=".$user_id."");
			}
		}else
		{
			$DB_site->query("update wog_player set p_hp=p_hpmax where p_id=".$user_id."");
			if($have_price[p_hp]<=0)
			{
				$hotel_time=$wog_arry["hotel_die_time"];
			}else
			{
				$hotel_time=$wog_arry["hotel_time"];
			}
		}
		if(time()-$HTTP_SESSION_VARS["act_time"] > $wog_arry["f_time"])
		{
			$HTTP_SESSION_VARS["act_time"]=time()-($wog_arry["f_time"]-$wog_arry["hotel_time"]);
		}else
		{
			$HTTP_SESSION_VARS["act_time"]=$HTTP_SESSION_VARS["act_time"]+$wog_arry["hotel_time"];
		}
		showscript("parent.job_end(5);parent.cd_add(".$hotel_time.")");
	}

	function bank($user_id)
	{
		global $DB_site,$_POST,$lang;
		$have_price=$DB_site->query_first("select p_bbsid,p_money from wog_player where p_id=".$user_id."");
		$bank_price=$DB_site->query_first("select ".BANK_FIELB." from ".USER_TABLE." where ".USER_ID."=".$have_price["p_bbsid"]."");
		showscript("parent.bank('".$have_price[p_money]."','".$bank_price[0]."')");
	}

	function bank_save($user_id,$pay_id,$money)
	{
		global $DB_site,$lang;
		$have_price=$DB_site->query_first("select p_name,p_money,p_lv,p_bbsid from wog_player where p_id=".$user_id."");
		if($have_price[p_money] < $money || $money <=0 || $have_price[p_lv]<15 || !is_numeric($money) || eregi("[^0-9]",$money) )
		{
			alertWindowMsg($lang['wog_act_bank_noues']);
			
		}else
		{
			if($user_id != $pay_id)
			{
				$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$pay_id.",'".$have_price[p_name]." 匯入 ".$money."元 到你的銀行 ',".time().")");
				$p=$DB_site->query_first("select p_bbsid from wog_player where p_id=".$pay_id."");
				$DB_site->query("update ".USER_TABLE." set ".BANK_FIELB." = ".BANK_FIELB."+".$money." WHERE ".USER_ID."=".$p["p_bbsid"]."");
			}else
			{
				$DB_site->query("update ".USER_TABLE." set ".BANK_FIELB." = ".BANK_FIELB."+".$money." WHERE ".USER_ID."=".$have_price["p_bbsid"]."");
			}
			$DB_site->query("update wog_player set p_money = p_money-".$money." where p_id=".$user_id."");
			showscript("parent.job_end(4)");
		}
	}

	function bank_get($user_id,$money)
	{
		global $DB_site,$lang;
		$bank_memey=$DB_site->query_first("select b.".BANK_FIELB.",b.".USER_ID." from wog_player a,".USER_TABLE." b where a.p_id=".$user_id." and a.p_bbsid=b.".USER_ID." ");
		if($bank_memey[BANK_FIELB] < $money )
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		if($bank_memey[BANK_FIELB] < $money || $money <=0  || !is_numeric($money) || eregi("[^0-9]",$money) )
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}else
		{
			$DB_site->query("update ".USER_TABLE." set ".BANK_FIELB." = ".BANK_FIELB."-".$money." WHERE ".USER_ID."=".$bank_memey[1]."");
			$DB_site->query("update wog_player set p_money = p_money+".$money." where p_id=".$user_id."");
			showscript("parent.job_end(4)");
		}
	}

	function p_sex($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["num"]))
		{
			alertWindowMsg($lang['wog_act_img_nosexg']);
		}
		if(eregi("[12]",$_POST["num"]))
		{
			$have_price=$DB_site->query_first("select p_money from wog_player where p_id=".$user_id."");
			if($wog_arry["chang_sex"]>$have_price[0]){
				alertWindowMsg($lang['wog_act_nomoney']);
			}
			$DB_site->query("update wog_player set p_sex=".$_POST["num"].",p_money=p_money-".$wog_arry["chang_sex"]." where p_id=".$user_id."");
			showscript("parent.job_end(11)");
		}else
		{
			alertWindowMsg($lang['wog_act_img_errsex']);
		}
		unset($have_price);
	}

	function p_img($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["num"]))
		{
			alertWindowMsg($lang['wog_act_img_noimg']);
		}
		if(!is_numeric($_POST["num"]))
		{
			alertWindowMsg($lang['wog_act_img_errimg']);
		}
		$p=$DB_site->query_first("SELECT i_id FROM wog_img WHERE i_id=".$_POST["num"]." ");
		if($p)
		{
			$have_price=$DB_site->query_first("select p_money from wog_player where p_id=".$user_id."");
			if($wog_arry["chang_face"]>$have_price[0]){
				alertWindowMsg($lang['wog_act_nomoney']);
			}
			$DB_site->query("update wog_player set p_img_set=0,i_img=".$_POST["num"].",p_money=p_money-".$wog_arry["chang_face"]." where p_id=".$user_id."");
			showscript("parent.job_end(11)");
		}else
		{
			alertWindowMsg($lang['wog_act_img_errimg']);
		}
		unset($p);
		unset($have_price);
	}

	function p_img2($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["url"]))
		{
			alertWindowMsg($lang['wog_act_img_noimg']);
		}
		$have_price=$DB_site->query_first("select p_money,p_st from wog_player where p_id=".$user_id."");
		if($wog_arry["chang_face"]>$have_price['p_money']){
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$DB_site->query("update wog_player set p_img_set=1,p_img_url='".$_POST["url"]."',p_money=p_money-".$wog_arry["chang_face"]." where p_id=".$user_id."");
		showscript("parent.job_end(11)");
		unset($have_price);
	}
}
?>