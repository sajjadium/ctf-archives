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

class wog_act_mission{
	function mission_list($user_id,$store_id)
	{
		global $DB_site,$lang,$_POST;
		$sql="select p_lv,p_sex,ch_id,p_birth from wog_player where p_id=".$user_id."";
		$p=$DB_site->query_first($sql);
		if(!$p)
		{
			alertWindowMsg($lang['wog_act_relogin']);
		}

		$m_total=$DB_site->query_first("select count(a.m_id) as m_id from wog_mission_main a LEFT JOIN wog_mission_book b ON  b.p_id=".$user_id." and a.m_id=b.m_id 
				LEFT JOIN wog_mission_book c ON  c.p_id=".$user_id." and a.m_need_id=c.m_id and a.m_not_id<>c.m_id
				LEFT JOIN wog_mission_book d ON d.p_id=1 and a.m_not_id=d.m_id
				where  a.m_store_id=".$store_id." and (a.m_job=".$p["ch_id"]." or a.m_job=99) and a.m_lv <= ".$p["p_lv"]." and (a.m_sex=".$p["p_sex"]." or a.m_sex=3)
				and (m_birth is null or m_birth = ".$p["p_birth"].")
				and ((b.m_id is null and a.m_need_id=0) or (c.m_status=2 and b.m_id is null) ) and d.m_id is null");

		if(empty($_POST["page"]) || !is_numeric($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$spage=((int)$_POST["page"]*8)-8;

		$sql="select a.m_id,a.m_subject,a.m_name from wog_mission_main a LEFT JOIN wog_mission_book b ON  b.p_id=".$user_id." and a.m_id=b.m_id 
				LEFT JOIN wog_mission_book c ON  c.p_id=".$user_id." and a.m_need_id=c.m_id and a.m_not_id<>c.m_id
				LEFT JOIN wog_mission_book d ON d.p_id=1 and a.m_not_id=d.m_id
				where  a.m_store_id=".$store_id." and (a.m_job=".$p["ch_id"]." or a.m_job=99) and a.m_lv <= ".$p["p_lv"]." and (a.m_sex=".$p["p_sex"]." or a.m_sex=3)
				and (m_birth is null or m_birth = ".$p["p_birth"].")
				and ((b.m_id is null and a.m_need_id=0) or (c.m_status=2 and b.m_id is null) ) and d.m_id is null LIMIT ".$spage.",8 ";

		$m=$DB_site->query($sql);
		while($ms=$DB_site->fetch_array($m))
		{
			$s.=";".$ms["m_id"].",".$ms["m_name"].",".$ms["m_subject"];
		}
		$DB_site->free_result($ms);
		unset($ms);
		unset($p);
		unset($m);
		$s=substr($s,1,strlen($s));
		showscript("parent.mission_list($m_total[0],".$_POST["page"].",'$s',$store_id)");
	}
	function mission_detail($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["m_id"])){alertWindowMsg($lang['wog_act_mission_error1']);}
		$m_item=$DB_site->query_first("select m_body,m_subject,m_name from wog_mission_main where m_id=".$_POST["m_id"]);
		if(!$m_item){alertWindowMsg($lang['wog_act_syn_error1']);}
		$temp_s=$m_item["m_subject"].",".$m_item["m_name"].",".$m_item["m_body"];
		$temp_s=str_replace("\r\n","&n",$temp_s);
		unset($m_item);
		showscript("parent.mission_detail('$temp_s',".$_POST["m_id"].")");
		unset($temp_s);
	}
	function mission_get($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["m_id"])){alertWindowMsg($lang['wog_act_mission_error1']);}
		$sql="select p_lv,p_sex,ch_id from wog_player where p_id=".$user_id."";
		$p=$DB_site->query_first($sql);
		if(!$p)
		{
			alertWindowMsg($lang['wog_act_relogin']);
		}
		$m_item=$DB_site->query_first("select m_id from wog_mission_book where  p_id=".$user_id." and m_status<2");
		if($m_item)
		{
			alertWindowMsg($lang['wog_act_mission_error6']);
		}
		$m_item=$DB_site->query_first("select a.m_id from wog_mission_main a ,wog_mission_book b where  b.p_id=".$user_id." and a.m_id=".$_POST["m_id"]." and a.m_not_id=b.m_id ");
		if($m_item){alertWindowMsg($lang['wog_act_mission_error3']);}
		$m_item=$DB_site->query_first("select a.m_id,a.m_area_id,a.m_kill_num from wog_mission_main a LEFT JOIN wog_mission_book b ON  b.p_id=".$user_id." and a.m_id<>b.m_id  
				where a.m_id=".$_POST["m_id"]." and (a.m_job=".$p["ch_id"]." or a.m_job=99) and a.m_lv <= ".$p["p_lv"]." and (a.m_sex=".$p["p_sex"]." or a.m_sex=3)");
		if(!$m_item){alertWindowMsg($lang['wog_act_mission_error3']);}
		$sql="insert wog_mission_book (m_id,p_id,m_status,m_kill_num)values(".$_POST["m_id"].",".$user_id.",0,".$m_item["m_kill_num"].")";
		$DB_site->query($sql);
		setcookie("wog_cookie_mission_id",$_POST["m_id"]);
		setcookie("wog_cookie_mission_area",$m_item["m_area_id"]);
		unset($m_item);
		showscript("parent.job_end(20)");
		unset($temp_s);
	}
	function mission_book($user_id)
	{
		global $DB_site,$_POST,$lang;
		$m_item=$DB_site->query_first("select a.m_body,a.m_subject,a.m_name,a.m_id from wog_mission_main a,wog_mission_book b where b.p_id=".$user_id." and b.m_status<2 and b.m_id=a.m_id");
		if(!$m_item){alertWindowMsg($lang['wog_act_mission_error5']);}
		$temp_s=$m_item["m_subject"].",".$m_item["m_name"].",".$m_item["m_body"];
		$temp_s=str_replace("\r\n","&n",$temp_s);
		showscript("parent.mission_book('$temp_s',".$m_item["m_id"].")");
		unset($m_item);
		unset($temp_s);
	}
	function mission_break($user_id)
	{
		global $DB_site,$_POST,$lang;
		$m_item=$DB_site->query_first("select a.m_id from wog_mission_book a where a.p_id=".$user_id." and a.m_status<2 and a.m_id=".$_POST["temp_id"]);
		if(!$m_item){alertWindowMsg($lang['wog_act_mission_error5']);}
		$sql="delete from wog_mission_book where p_id=".$user_id." and m_status<2 and m_id=".$m_item["m_id"];
		$DB_site->query($sql);
		unset($m_item);
		showscript("parent.job_end(22)");
	}
	function mission_paper($user_id)
	{
		global $DB_site,$lang,$_POST;
		$m_total=$DB_site->query_first("select count(a.m_id) as m_id from wog_mission_main a ,wog_mission_book b where b.p_id=".$user_id." and m_status=2 and a.m_id=b.m_id ");

		if(empty($_POST["page"]) || !is_numeric($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$spage=((int)$_POST["page"]*8)-8;

		$sql="select a.m_subject,a.m_name from wog_mission_main a ,wog_mission_book b where b.p_id=".$user_id." and m_status=2 and a.m_id=b.m_id LIMIT ".$spage.",8";
		$m=$DB_site->query($sql);
		while($ms=$DB_site->fetch_array($m))
		{
			$s.=";".$ms["m_name"].",".$ms["m_subject"];
		}
		$DB_site->free_result($ms);
		unset($ms);
		unset($p);
		unset($m);
		$s=substr($s,1,strlen($s));
		showscript("parent.mission_paper($m_total[0],".$_POST["page"].",'$s')");
	}
}