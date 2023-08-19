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

class wog_mission_tool{
	function mission_check($user_id,$m_id)
	{
		global $DB_site,$_POST,$lang;
		$sql="select a.m_id,b.m_end_message,a.m_status,b.m_pet_id,a.m_kill_num,m_lv from wog_mission_book a,wog_mission_main b where a.p_id=".$user_id." and a.m_id=".$m_id." and a.m_status<2 and b.m_id=a.m_id";
		$m_book=$DB_site->query_first($sql);
		if(!$m_book)
		{
			alertWindowMsg($lang['wog_act_mission_error4']);
		}
		if($m_book["m_status"]!=1 && $m_book["m_kill_num"]!=0)
		{
			alertWindowMsg($lang['wog_act_mission_error6']);
		}
		return $m_book;
	}
	function mission_pet($user_id,$m_pet_id)
	{
		global $DB_site,$lang;
		$sql="select pe_id  from wog_pet where pe_p_id=".$user_id." and pe_m_id=".$m_pet_id;
		$pet=$DB_site->query_first($sql);
		if(!$pet)
		{
			alertWindowMsg($lang['wog_act_mission_error4']);
		}
		$DB_site->query("delete from  wog_pet  where pe_p_id=".$user_id." and pe_st=0 and pe_m_id=".$m_pet_id);
	}
	function mission_pet_get($user_id,$m_pet_id,$up)
	{
		global $DB_site,$lang;
		$sql="select m_id,m_name,m_img from wog_monster where m_id=".$m_pet_id." LIMIT 1 ";
		$m=$DB_site->query_first($sql);
		if(!$m)//m date check start
		{
			alertWindowMsg($lang['wog_act_errdate']);
		}
		$pet[pe_at]=rand(1,10)*$up;
		$pet[pe_mt]=rand(1,10)*$up;
		$pet[pe_def]=rand(1,10)*$up;
		$pet[pe_type]=rand(1,4);
		$sql="insert into wog_pet(pe_p_id,pe_name,pe_at,pe_mt,pe_fu,pe_def,pe_hu,pe_type,pe_age,pe_he,pe_fi,pe_dateline,pe_mname,pe_m_id,pe_b_dateline,pe_mimg)";
		$sql.="values(".$user_id.",'".$m[m_name]."',".$pet[pe_at].",".$pet[pe_mt].",80,".$pet[pe_def].",0,".$pet[pe_type].",1,0,1,".(time()-20).",'".$m[m_name]."',".$m[m_id].",".time().",'".$m[m_img]."')";
		$DB_site->query($sql);
		unset($m);
		unset($pet);
	}
	function mission_item($user_id,$item_array,$item_date)
	{
		global $DB_site,$_POST,$lang,$wog_item_tool,$a_id;
		$sql="select a_id,d_body_id,d_foot_id,d_hand_id,d_head_id,d_item_id from wog_item where p_id=".$user_id."";
		$item=$DB_site->query_first($sql);
		$temp_sql="";
		for($i=0;$i<count($item_array);$i++)
		{
			$a_id=$item_array[$i];
			$items=array();
			if(!empty($item[$a_id]))
			{
				$items=split(",",$item[$a_id]);
			}
			for($j=0;$j<count($item_date[$a_id]);$j++)
			{
				if($a_id=="d_item_id")
				{
					$need_item=split("\*",$item_date[$a_id][$j]);
					$items=$wog_item_tool->item_out($user_id,$need_item[0],$need_item[1],$items);
				}else
				{
					$items=$wog_item_tool->item_out($user_id,$item_date[$a_id][$j],1,$items);
				}
			}
			$temp_sql.=",".$a_id."='".implode(',',$items)."'";
		}
		$temp_sql=substr($temp_sql,1,strlen($temp_sql));
		$DB_site->query("update wog_item set ".$temp_sql." where p_id=".$user_id." ");
	}
	function mission_reward($user_id,$item_array,$item_date)
	{
		global $DB_site,$_POST,$lang,$wog_item_tool,$a_id;
		$sql="select a_id,d_body_id,d_foot_id,d_hand_id,d_head_id,d_item_id from wog_item where p_id=".$user_id."";
		$item=$DB_site->query_first($sql);
		$temp_sql="";
		for($i=0;$i<count($item_array);$i++)
		{
			$a_id=$item_array[$i];
			$items=array();
			if(!empty($item[$a_id]))
			{
				$items=split(",",$item[$a_id]);
			}
			for($j=0;$j<count($item_date[$a_id]);$j++)
			{
				if($a_id=="d_item_id")
				{
					$need_item=split("\*",$item_date[$a_id][$j]);
					$items=$wog_item_tool->item_in($items,$need_item[0],$need_item[1]);
				}else
				{
					$items=$wog_item_tool->item_in($items,$item_date[$a_id][$j],0);
				}
			}
			$temp_sql.=",".$a_id."='".implode(',',$items)."'";
		}
		$temp_sql=substr($temp_sql,1,strlen($temp_sql));
		$DB_site->query("update wog_item set ".$temp_sql." where p_id=".$user_id." ");
	}
	function mission_money($user_id,$money)
	{
		global $DB_site;
		$DB_site->query("update wog_player set p_money=p_money+".$money." where p_id=".$user_id." ");
	}
	
	function mission_status_update($user_id,$m_id,$m_end_message,$m_lv)
	{
		global $DB_site,$_POST,$lang;
		$DB_site->query("update wog_mission_book set m_status=2 where p_id=".$user_id." and m_id=".$m_id);
		$DB_site->query("update wog_player set p_exp=p_exp+".($m_lv*150)." where p_id=".$user_id);
		setcookie("wog_cookie_mission_id",0);
		$m_end_message=str_replace("\r\n","&n",$m_end_message);
		showscript("parent.job_end(21,'".$m_end_message."')");
	}
}
