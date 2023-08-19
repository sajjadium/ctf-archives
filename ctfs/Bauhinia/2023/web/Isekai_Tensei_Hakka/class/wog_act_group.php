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

class wog_act_group{

	function group_fire_set($user_id)
	{
		global $DB_site,$_POST,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2,a.g_fire_time from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id);
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($user_id!=$group_main["g_adm_id1"])
		{
			alertWindowMsg($lang['wog_act_group_nolyadmin']);
		}
		if($group_main["g_fire_time"]+(60*60*2)>time())
		{
			alertWindowMsg($lang['wog_act_group_nochang']);
		}
		$DB_site->query("update wog_group_main set g_fire=".$_POST["temp_id2"].",g_fire_time=".time()." where g_id=".$group_main["g_id"]);
		$this->group_center($user_id);
		unset($group_main);
	}

	function group_news($user_id)
	{
		global $DB_site,$lang;
		$group_main=$DB_site->query_first("select a.g_id from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		$DB_site->query("delete from wog_group_event where g_b_dateline < ".(time()-(10*24*60*60))." ");
		$sql="select g_b_body,g_b_dateline from wog_group_event where g_b_id=".$group_main[g_id]." order by g_b_inid desc LIMIT 10";
		$pack=$DB_site->query($sql);
		$s="";
		while($packs=$DB_site->fetch_array($pack))
		{
			$s=$s.";".$packs[g_b_body].",".date("Y/m/d  g:i a",$packs[g_b_dateline]);
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($pack);
		showscript("parent.system_view('$s')");
		unset($s);
		unset($packs);
	}

	function group_fire_list_peo($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$time=time();
		$g_f_t=date("G",$time);
		if($g_f_t<$wog_arry["g_f_stime"] || $g_f_t>=$wog_arry["g_f_etime"])
		{
			alertWindowMsg($lang['wog_act_group_firetime'].$wog_arry["g_f_stime"].":00-".$wog_arry["g_f_etime"].":00");
		}
		$group_main=$DB_site->query_first("select a.g_id,a.g_fire from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["g_fire"]==0)
		{
			alertWindowMsg($lang['wog_act_group_fireset']);
		}
		$temp_s="";
		$u_g_a=$DB_site->query_first("select p_name,p_g_number,p_g_morale,p_g_a_id from wog_player a,wog_group_area b where a.p_id=".$user_id." ");
		if($u_g_a)
		{
			$g_a_type=$DB_site->query_first("select g_a_type from wog_group_area  where g_a_id=".$u_g_a["p_g_a_id"]."");
			if(!$g_a_type)
			{
				$g_a_type[0]="7";
			}
			$temp_s.=";".$u_g_a["p_name"].",".$u_g_a["p_g_morale"].",".$u_g_a["p_g_number"].",".$g_a_type[0];
		}
		$temp_s=substr($temp_s,1,strlen($temp_s));
		$group=$DB_site->query("select a.g_id,a.g_name from wog_group_main a where a.g_id<>".$group_main[0]." and g_fire=1");
		$temp_ss="";
		while($groups=$DB_site->fetch_array($group))
		{
			$temp_ss.=";".$groups[0].",".$groups[1];
		}
		$DB_site->free_result($group);
		unset($groups);
		$temp_ss=substr($temp_ss,1,strlen($temp_ss));
		showscript("parent.group_fire_list_peo('".$temp_s."','".$temp_ss."')");
		unset($temp_s);
		unset($temp_ss);
		unset($u_g_a);
	}

	function group_money($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		if(!is_numeric($_POST["temp_id"]) || (int)$_POST["temp_id"] < 1)
		{
			alertWindowMsg($lang['wog_act_errmoney']);
		}
		$_POST["temp_id"]=(int)$_POST["temp_id"];
		$group_main=$DB_site->query_first("select p_money,p_g_id from wog_player where p_id=".$user_id." ");
		if($group_main["p_g_id"]==0)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["p_money"]<$_POST["temp_id"])
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$DB_site->query("update wog_group_main set g_money=g_money+".$_POST["temp_id"]." where g_id=".$group_main["p_g_id"]);
		$DB_site->query("update wog_player set p_money=p_money-".$_POST["temp_id"]." where p_id=".$user_id);
		showscript("parent.job_end(15)");
		unset($group);
	}
	
	function group_hp($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_money,b.p_g_a_id,c.g_a_hp,c.g_a_dateline,b.p_smart from wog_group_main a,wog_player b,wog_group_area c where a.g_id=b.p_g_id and b.p_id=".$user_id." and c.g_a_id=b.p_g_a_id ");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["g_a_dateline"]+(60*$wog_arry["g_ea_time"]) > time())
		{
			alertWindowMsg($lang['wog_act_group_needmin'].$wog_arry["g_ea_time"]." minutes");
		}
		if($group_main["g_money"]<1000)
		{
			alertWindowMsg($lang['wog_act_group_needmoney']);
		}
		$g_hp=rand(1,round(($p["p_smart"]/1500)*15))+10;
		$g_hp=$g_hp+$group_main["g_a_hp"];
		if($g_hp>100){$g_hp=100;}
		$DB_site->query("update wog_group_area set g_a_hp=$g_hp where g_a_id=".$group_main["p_g_a_id"]);
		$DB_site->query("update wog_group_main set g_money=g_money-1000 where g_id=".$group_main["g_id"]);
		$this->group_center($user_id);
		unset($group);
	}

	function group_del($user_id)
	{
		global $DB_site,$_POST,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id);
		if($group_main)
		{
			if($user_id==$group_main["g_adm_id1"])
			{
				$DB_site->query("delete from wog_group_main where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_area where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_event where g_b_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_book where g_id=".$group_main["g_id"]."");
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_g_id=".$group_main["g_id"]."");
			}else
			{
				$DB_site->query("update wog_group_main set g_peo=g_peo-1 where g_id=".$group_main["g_id"]."");
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_id=".$user_id."");
			}
			showscript("parent.p_group='';parent.job_end(15)");
		}
		unset($group);
	}	

	function group_get_save_member($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_group_nosel']);
		}
		$_POST["temp_id2"]=htmlspecialchars($_POST["temp_id2"]);
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["g_adm_id1"]!=$user_id && $group_main["g_adm_id2"]!=$user_id)
		{
			alertWindowMsg($lang['wog_act_group_nolv']);
		}
		$group=$DB_site->query_first("select g_id,p_id from wog_group_join where g_j_id=".$_POST["temp_id2"]);
		if(!$group)
		{
			alertWindowMsg($lang['wog_act_group_cancel']);
		}
		if($group_main["g_id"]!=$group["g_id"])
		{
			alertWindowMsg($lang['wog_act_group_notset']);
		}
		$p=$DB_site->query_first("select p_g_id from wog_player where p_id=".$group["p_id"]);
		if($p["p_g_id"]>0)
		{
			alertWindowMsg($lang['wog_act_group_havgroup']);
		}
		$p_count=$DB_site->query_first("select g_peo from wog_group_main  where g_id=".$group["g_id"]."");
		if($p_count[0]>=20)
		{
			alertWindowMsg($lang['wog_act_group_ful']);
		}
		$DB_site->query("update wog_player set p_g_id=".$group["g_id"].",p_g_number=1000,p_g_morale=100 where p_id=".$group["p_id"]."");
		$DB_site->query("update wog_group_main set g_peo=g_peo+1 where g_id=".$group["g_id"]."");
		$DB_site->query("delete from wog_group_join where p_id=".$group["p_id"]);
		showscript("parent.job_end(15)");
		unset($group);
		unset($p_count);
		unset($p);
		unset($group_main);
	}

	function group_get_member($user_id)
	{
		global $DB_site,$_POST,$lang;
		$DB_site->query("delete from wog_group_join where g_j_dateline < ".(time()-(7*24*60*60)));
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["g_adm_id1"]!=$user_id && $group_main["g_adm_id2"]!=$user_id)
		{
			alertWindowMsg($lang['wog_act_group_nolv']);
		}
		$group=$DB_site->query("select a.g_j_id,b.p_name,b.p_lv,c.ch_name from wog_group_join a,wog_player b,wog_character c where a.g_id=".$group_main["g_id"]." and a.p_id=b.p_id and b.ch_id=c.ch_id order by a.g_j_dateline asc");
		$temp_s="";
		while($groups=$DB_site->fetch_array($group))
		{
			$temp_s.=";".$groups[0].",".$groups[1].",".$groups[2].",".$groups[3];
		}
		$DB_site->free_result($group);
		unset($groups);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.group_join_list('$temp_s')");
		unset($temp_s);
	}

	function group_add($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["g_id"]))
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		$_POST["g_id"]=htmlspecialchars($_POST["g_id"]);
		$DB_site->query("delete from wog_group_join where g_j_dateline < ".(time()-(7*24*60*60)));
		$group=$DB_site->query_first("select p_g_id from wog_player where p_id=".$user_id." ");
		if($group[0]!=0)
		{
			$group_chk=$DB_site->query_first("select g_id from wog_group_main where g_id=".$group[0]." ");
			if($group_chk)
			{
				alertWindowMsg($lang['wog_act_group_havgroup']);
			}else
			{
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_id=".$user_id."");
			}
			unset($group_chk);
		}
		$group=$DB_site->query_first("select g_peo  from wog_group_main  where g_id=".$_POST["g_id"]."");
		if($group[0]>=20)
		{
			alertWindowMsg($lang['wog_act_group_ful']);
		}
		$group=$DB_site->query_first("select g_j_id from wog_group_join where p_id=".$user_id." and g_id=".$_POST["g_id"]."");
		if($group)
		{
			alertWindowMsg($lang['wog_act_group_post']);
		}
		$DB_site->query("insert into wog_group_join(g_id,p_id,g_j_dateline)values(".$_POST["g_id"].",".$user_id.",".time().")");
		showscript("parent.job_end(14)");
		unset($group);
	}

	function group_join($user_id)
	{
		global $DB_site,$_POST,$lang;
		$group_total=$DB_site->query_first("select count(a.g_id) as g_id from wog_group_main a ");
		if(empty($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$spage=((int)$_POST["page"]*8)-8;
		$group=$DB_site->query("select a.g_id,a.g_name,sum(b.p_g_number) as p_g_number,avg(b.p_g_morale),a.g_peo,a.g_money,a.g_win,a.g_lost,a.g_adm_id1 from wog_group_main a,wog_player b where a.g_id=b.p_g_id  group by b.p_g_id  ORDER BY a.g_id desc LIMIT ".$spage.",8 ");
		$temp_s="";
		while($groups=$DB_site->fetch_array($group))
		{
			$p=$DB_site->query_first("select a.p_name from wog_player a where a.p_id=".$groups[8]);
			$temp_s.=";".$groups[0].",".$groups[1].",".$groups[2].",".round($groups[3]).",".$groups[4].",".$groups[5].",".$groups[6].",".$groups[7].",".$p["p_name"];
		}
		$DB_site->free_result($group);
		unset($groups);
		unset($p);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.group_join($group_total[0],".$_POST["page"].",'$temp_s')");
		unset($temp_s);
		unset($group_total);
	}

	function group_p_number($user_id)
	{
		global $DB_site,$_POST,$lang;
		$p=$DB_site->query_first("select a.g_id,a.g_money,c.g_a_hp,b.p_g_number from wog_group_main a,wog_player b,wog_group_area c where a.g_id=b.p_g_id and b.p_id=".$user_id." and c.g_a_id=b.p_g_a_id ");
		$temp_money=0;
		if($_POST["temp_id"]=="full")
		{
			$temp_money=10000-$p["p_g_number"];
			$p["p_g_number"]=10000;
		}else
		{
			$p["p_g_number"]=$p["p_g_number"]+(int)$_POST["temp_id"];
			if($p["p_g_number"]>10000)
			{
				$temp_money=$p["p_g_number"]-10000;
				$p["p_g_number"]=10000;
			}
			$temp_money=(int)$_POST["temp_id"]-$temp_money;
		}
		if($p["g_a_hp"]<=0)
		{
			alertWindowMsg($lang['wog_act_group_noadd']);
		}
		if($p["g_money"]<$temp_money)
		{
			alertWindowMsg($lang['wog_act_group_nogmoney']);	
		}
		$DB_site->query("update wog_player set p_g_number=".$p["p_g_number"].",p_money=p_money-".$temp_money." where p_id=".$user_id);
		$DB_site->query("update wog_group_main set g_money=g_money-".$temp_money." where g_id=".$p["g_id"]);
		$this->group_center($user_id);
		unset($p);
	}

	function group_morale($user_id)
	{
		global $DB_site,$lang;
		$p=$DB_site->query_first("select p_money,p_au,p_g_morale from wog_player where p_id=".$user_id);
		if($p["p_money"]<100)
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$p_morale=rand(1,round(($p["p_au"]/680)*15))+9;
		$p_morale=$p_morale+$p["p_g_morale"];
		if($p_morale>100){$p_morale=100;}
		$DB_site->query("update wog_player set p_g_morale=$p_morale,p_money=p_money-100 where p_id=".$user_id);
		$this->group_center($user_id);
		unset($p);
	}

	function group_number($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["p_id"]))
		{
			alertWindowMsg($lang['wog_act_group_nosel']);
		}
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($group_main["g_adm_id1"]!=$user_id && $group_main["g_adm_id2"]!=$user_id)
		{
			alertWindowMsg($lang['wog_act_group_nolv']);
		}
		if($_POST["g_del"]==1)
		{
			if(htmlspecialchars($_POST["p_id"])==$group_main["g_adm_id1"])
			{
				$DB_site->query("delete from wog_group_main where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_area where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_event where g_b_id=".$group_main["g_id"]."");
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_g_id=".$group_main["g_id"]."");
			}else
			{
				$DB_site->query("update wog_group_main set g_peo=g_peo-1 where g_id=".$group_main["g_id"]."");
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_id=".htmlspecialchars($_POST["p_id"])."");
			}
		}else
		{
			if(empty($_POST["g_a_type"]))
			{
				alertWindowMsg($lang['wog_act_group_settype']);
			}
			if($_POST["g_a_type"]=="7")
			{
				$DB_site->query("update wog_player set p_g_a_id=0 where p_id=".htmlspecialchars($_POST["p_id"])."");
			}else
			{
				$get_g_a_id=$DB_site->query_first("select g_a_id from wog_group_area  where g_id=".$group_main["g_id"]." and g_a_type=".$_POST["g_a_type"]." ");
				$peo_num=$DB_site->query_first("select count(p_id) as p_id from wog_player where p_g_a_id=".$get_g_a_id[0]." ");
				if($peo_num[0]>=$wog_arry["g_a_peo"])
				{
					alertWindowMsg($lang['wog_act_group_fulpeople'].$wog_arry["g_a_peo"]." member");
				}else
				{
					$DB_site->query("update wog_player set p_g_a_id=".$get_g_a_id[0]." where p_id=".htmlspecialchars($_POST["p_id"])."");
				}
			}
		}
		showscript("parent.job_end(11)");
		unset($temp_s);
		unset($group_main);
		unset($u_g_a);
	}
	
	function group_peolist($user_id)
	{
		global $DB_site,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_name,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		$temp_s="";
		$u_g_a=$DB_site->query("select a.p_id,a.p_name,a.p_g_number,a.p_g_morale,a.p_g_a_id,a.p_lv from wog_player a where a.p_g_id=".$group_main[0]." ");
		while($u_g_as=$DB_site->fetch_array($u_g_a))
		{
			$g_a_type=$DB_site->query_first("select g_a_type from wog_group_area  where g_a_id=".$u_g_as["p_g_a_id"]."");
			if(!$g_a_type)
			{
				$g_a_type[0]="7";
			}
			if($u_g_as["p_id"]==$group_main["g_adm_id1"])
			{
				$u_g_as["p_name"].=$lang['wog_act_group_ad'];
			}
			$temp_s.=";".$u_g_as["p_id"].",".$u_g_as["p_name"].",".$u_g_as["p_g_morale"].",".$u_g_as["p_g_number"].",".$u_g_as["p_lv"].",".$g_a_type[0];
		}
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.group_peolist('".$temp_s."','".$group_main[1]."')");
		unset($temp_s);
		unset($group_main);
		unset($u_g_a);
	}
	
	function group_center($user_id)
	{
		global $DB_site,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_name,a.g_fire from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id."");
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		$temp_s="";
		$group_area=$DB_site->query("select g_a_type,g_a_hp,g_a_id from wog_group_area where g_id=".$group_main[0]." ");
		while($group_areas=$DB_site->fetch_array($group_area))
		{
			$g_a_body=$DB_site->query_first("select sum(p_g_number) as p_g_number,avg(p_g_morale) as p_g_morale,count(p_id) as p_id 
			from wog_player where p_g_id=".$group_main[0]." and p_g_a_id=".$group_areas["g_a_id"]."");
			$temp_s.=";".$group_areas["g_a_type"].",".$g_a_body["p_g_number"].",".round($g_a_body["p_g_morale"]).",".$group_areas["g_a_hp"].",".$g_a_body["p_id"];
		}
		$DB_site->free_result($group_area);
		unset($group_area);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		$u_g="";
		$u_g_a=$DB_site->query_first("select a.p_g_number,a.p_g_morale,b.g_a_type from wog_player a,wog_group_area b where p_id=".$user_id." and b.g_a_id=a.p_g_a_id");
		if($u_g_a)
		{
			$u_g=$u_g_a[2].",".$u_g_a[0].",".$u_g_a[1];	
		}
		showscript("parent.group_center('".$temp_s."','".$group_main[g_name]."','".$u_g."',".$group_main[g_fire].")");
		unset($temp_s);
		unset($group_areas);
		unset($group_main);
		unset($u_g_a);
		unset($u_g);
	}
	
	function group_creat($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_group_noname']);
		}
		if(eregi("[<>'\", ;]", $_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_errword']);
		}
		$_POST["temp_id"]=addslashes(htmlspecialchars($_POST["temp_id"]));
		$group=$DB_site->query_first("select g_name from wog_group_main where g_name='".$_POST["temp_id"]."'");
		if($group)
		{
			alertWindowMsg($lang['wog_act_group_used']);
		}else
		{
			$have_price=$DB_site->query_first("select p_money,p_g_id from wog_player where p_id=".$user_id."");	
			if($have_price[0]<$wog_arry["creat_group"])
			{
				alertWindowMsg($lang['wog_act_nomoney']);
			}
			if($have_price[1]>0)
			{
				alertWindowMsg($lang['wog_act_group_notcreat']);
			}
				$DB_site->query("insert into wog_group_main(g_name,g_adm_id1,g_peo)values('".$_POST["temp_id"]."',".$user_id.",1)");
				$g_id=$DB_site->insert_id();
				$DB_site->query("update wog_player set p_g_id=".$g_id.",p_g_number=1000,p_g_morale=100,p_money=p_money-".$wog_arry["creat_group"]." where p_id=".$user_id."");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",1,100,".time().")");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",2,100,".time().")");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",3,100,".time().")");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",4,100,".time().")");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",5,100,".time().")");
				$DB_site->query("insert into wog_group_area(g_id,g_a_type,g_a_hp,g_a_dateline)values(".$g_id.",6,100,".time().")");
				showscript("parent.job_end(10);parent.p_group='".$_POST["temp_id"]."'");
		}
		unset($groups);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.group_join($group_total[0],".$_POST["page"].",'$temp_s')");
		unset($temp_s);
		unset($group_total);
	}

	function group_book_view($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$group=$DB_site->query_first("select p_g_id from wog_player where p_id=".$user_id."");
		if($group['p_g_id']==0)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		$group=$DB_site->query_first("select g_book from wog_group_book where g_id=".$group['p_g_id']."");
		$temp=str_replace("\r\n","&n",$group[0]);
		showscript("parent.group_book_view('$temp')");
		unset($group);
	}

	function group_book_save($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_nodata']);
		}
		$temp=htmlspecialchars($_POST["temp_id"]);
		if(strlen($temp) > 800)
		{
			alertWindowMsg($lang['wog_act_group_long']);
		}
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$user_id);
		if(!$group_main)
		{
			alertWindowMsg($lang['wog_act_group_nogroup']);
		}
		if($user_id!=$group_main["g_adm_id1"])
		{
			alertWindowMsg($lang['wog_act_group_nolyadmin']);
		}
		$g_id=$group_main['g_id'];
		$group_main=$DB_site->query_first("select g_id from wog_group_book where g_id=".$g_id);
		if($group_main)
		{
			$DB_site->query("update wog_group_book set g_book='".$temp."' where g_id=".$g_id);
		}else
		{
			$DB_site->query("insert wog_group_book(g_id,g_book)values(".$g_id.",'".$temp."')");
		}
		unset($group_main);
		unset($temp);
		$this->group_book_view($user_id);
	}

}
?>