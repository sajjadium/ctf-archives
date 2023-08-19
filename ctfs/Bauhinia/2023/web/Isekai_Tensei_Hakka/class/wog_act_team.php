<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/06/04
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

class wog_act_team{

	function team_list($user_id)
	{
		global $DB_site,$_POST,$lang;
		$this->team_clear();
		$team_total=$DB_site->query_first("select count(a.t_id) as t_id from wog_team_main a ");
		if(empty($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$spage=((int)$_POST["page"]*8)-8;
		$team=$DB_site->query("select a.t_id,a.t_name,a.t_peo,a.p_id from wog_team_main a ORDER BY a.t_id desc LIMIT ".$spage.",8 ");
		$temp_s="";
		while($teams=$DB_site->fetch_array($team))
		{
			$p=$DB_site->query_first("select a.p_name,a.p_lv from wog_player a where a.p_id=".$teams[p_id]);
			$temp_s.=";".$teams[t_id].",".$teams[t_name].",".$teams[t_peo].",".$p["p_name"].",".$p["p_lv"];
		}
		$DB_site->free_result($team);
		unset($teams);
		unset($p);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.team_list($team_total[0],".$_POST["page"].",'$temp_s')");
		unset($temp_s);
		unset($group_total);
	}

	function team_creat($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_team_noname']);
		}
		if(eregi("[<>'\", ;]", $_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_errword']);
		}
		$_POST["temp_id"]=addslashes(htmlspecialchars($_POST["temp_id"]));
		$team=$DB_site->query_first("select t_name from wog_team_main where t_name='".$_POST["temp_id"]."'");
		if($team)
		{
			alertWindowMsg($lang['wog_act_team_used']);
		}else
		{
			$team=$DB_site->query_first("select t_id from wog_player where p_id=".$user_id."");	
			if($team[0]>0)
			{
				alertWindowMsg($lang['wog_act_team_notcreat']);
			}
			$DB_site->query("insert into wog_team_main(t_name,p_id,t_peo,t_time)values('".$_POST["temp_id"]."',".$user_id.",1,".time().")");
			$g_id=$DB_site->insert_id();
			$DB_site->query("update wog_player set t_id=".$g_id." where p_id=".$user_id."");
			showscript("parent.job_end(10);parent.t_team='".$_POST["temp_id"]."'");
		}
	}

	function team_status($user_id)
	{
		global $DB_site,$_POST,$lang;
//		echo "select b.p_name,b.p_id,b.p_online_time,b.p_lv,a.p_id as adm_id from wog_team_main a,wog_player b where a.p_id=".$user_id." and a.t_id=b.t_id ";
		$team1=$DB_site->query_first("select b.t_id,a.p_id as adm_id from wog_team_main a,wog_player b where b.p_id=".$user_id." and a.t_id=b.t_id ");
		if(!$team1)
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		$team2=$DB_site->query("select b.p_name,b.p_id,b.p_online_time,b.p_lv from wog_player b where b.t_id=".$team1["t_id"]);
		while($teams=$DB_site->fetch_array($team2))
		{
			$temp_s.=";".$teams[p_id].",".$teams[p_name].",".$teams[p_lv].",".$teams[p_online_time];
		}
		if($team1["adm_id"]==$user_id)
		{
			$adm=1;
		}else
		{
			$adm=0;
		}
		$DB_site->free_result($team2);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		$team_support=$DB_site->query_first("select p_support from wog_player where p_id=".$user_id."");
		showscript("parent.team_status('$temp_s',".time().",'".$team_support[p_support]."','$user_id','".$adm."')");
		unset($temp_s);
	}

	function team_support($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_team_nosupport']);
		}
		if($user_id==$_POST["temp_id2"])
		{
			alertWindowMsg($lang['wog_act_team_nosupport']);
		}
		$team=$DB_site->query_first("select t_id from wog_player where p_id=".$user_id."");
		if(!$team)
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		if($_POST["temp_id2"] != "0")
		{
			$team2=$DB_site->query_first("select t_id from wog_player where p_id=".$_POST["temp_id2"]." and t_id=".$team[t_id]);
			if(!$team2)
			{
				alertWindowMsg($lang['wog_act_team_noteam2']);
			}
			$DB_site->query("update wog_player set p_support=".$_POST["temp_id2"]." where p_id=".$user_id);
		}
		showscript("parent.job_end(3)");
	}

	function team_nosupport($user_id)
	{
		global $DB_site,$_POST,$lang;
		$team=$DB_site->query_first("select t_id from wog_player where p_id=".$user_id."");
		if(!$team)
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		$DB_site->query("update wog_player set p_support=0 where p_id=".$user_id);
		showscript("parent.job_end(3)");
	}
	
	function team_del($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_team_nosupport']);
		}
		$team_main=$DB_site->query_first("select a.t_id,a.p_id from wog_team_main a where a.p_id=".$user_id);
		$team_main2=$DB_site->query_first("select a.t_id from wog_player a where a.p_id=".$_POST["temp_id2"]);
		if($team_main["t_id"] != $team_main2["t_id"])
		{
			alertWindowMsg($lang['wog_act_team_nodel2']);
		}
		if($team_main)
		{
			$time=time();
			if($_POST["temp_id2"]==$team_main["p_id"])
			{
				$DB_site->query("delete from wog_team_main where t_id=".$team_main["t_id"]);
				$sql="select p_id from wog_player where t_id=".$team_main["t_id"];
				$p=$DB_site->query($sql);
				while($ps=$DB_site->fetch_array($p))
				{
					$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$ps["p_id"].",'".$lang['wog_act_team_del']."',".$time.")");
				}
				$DB_site->free_result($p);
				$DB_site->query("update wog_player set t_id=0,p_support=0 where t_id=".$team_main["t_id"]);
			}else
			{
				$DB_site->query("update wog_team_main set t_peo=t_peo-1 where t_id=".$team_main["t_id"]);
				$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$_POST["temp_id2"].",'".$lang['wog_act_team_leave']."',".$time.")");
				$DB_site->query("update wog_player set t_id=0,p_support=0 where p_id=".$_POST["temp_id2"]);
			}
			unset($p);
			unset($team_main);
			showscript("parent.job_end(3);");
		}else
		{
			alertWindowMsg($lang['wog_act_team_noadm']);
		}
	}

	function team_join($user_id)
	{
		global $DB_site,$_POST,$lang,$wog_arry;
		if(empty($_POST["t_id"]))
		{
			alertWindowMsg($lang['wog_act_team_nosel']);
		}
//		$_POST["temp_id"]=htmlspecialchars($_POST["temp_id"]);
		$team=$DB_site->query_first("select a.t_peo,a.p_id from wog_team_main a where a.t_id=".$_POST["t_id"]);
		if($team["t_peo"] >=$wog_arry["t_peo"] )
		{
			alertWindowMsg($lang['wog_act_team_ful']);
		}
		$team2=$DB_site->query_first("select a.t_id,a.p_lv from wog_player a where a.p_id=".$user_id);
		if($team2["t_id"])
		{
			alertWindowMsg($lang['wog_act_team_hav']);
		}
		$team3=$DB_site->query_first("select a.p_lv from wog_player a where a.p_id=".$team["p_id"]);
		if(($wog_arry["t_lv_limit"] < ($team2["p_lv"]-$team3["p_lv"])) || ($wog_arry["t_lv_limit"] < ($team3["p_lv"]-$team2["p_lv"])))
		{
			alertWindowMsg($lang['wog_act_team_errorlv']);
		}
		unset($team);
		unset($team2);
		unset($team3);
		$DB_site->query("insert wog_team_join(t_id,p_id,t_j_dateline)values(".$_POST["t_id"].",".$user_id.",".time().")");
		showscript("parent.job_end(14)");
	}

	function team_leave($user_id)
	{
		global $DB_site,$_POST,$lang;
		$team=$DB_site->query_first("select a.t_id,a.p_name from wog_player a where a.p_id=".$user_id."");
		if(!$team["t_id"])
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		$team2=$DB_site->query_first("select a.t_id,a.p_id from wog_team_main a where a.p_id=".$user_id);
		$time=time();
		if($team2)
		{
			$DB_site->query("delete from wog_team_main where t_id=".$team2["t_id"]);
			$sql="select p_id from wog_player where t_id=".$team2["t_id"];
			$p=$DB_site->query($sql);
			while($ps=$DB_site->fetch_array($p))
			{
				$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$ps["p_id"].",'".$lang['wog_act_team_del']."',".$time.")");
			}
			$DB_site->free_result($p);
			$DB_site->query("update wog_player set t_id=0,p_support=0 where t_id=".$team2["t_id"]);
		}else
		{
			$sql="select p_id from wog_player where t_id=".$team["t_id"];
			$p=$DB_site->query($sql);
			while($ps=$DB_site->fetch_array($p))
			{
				$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$ps["p_id"].",'".$team["p_name"]." ".$lang['wog_act_team_leave']."',".$time.")");
			}
			$DB_site->free_result($p);
			$DB_site->query("update wog_team_main set t_peo=t_peo-1 where t_id=".$team["t_id"]);
			$DB_site->query("update wog_player set t_id=0,p_support=0 where p_id=".$user_id);
		}
		unset($team);
		unset($p);
		showscript("parent.job_end(3);parent.t_team=''");
	}

	function team_get_member($user_id)
	{
		global $DB_site,$_POST,$lang;
		$DB_site->query("delete from wog_team_join where t_j_dateline < ".(time()-(24*60*60)));
		$team_main=$DB_site->query_first("select a.t_id,a.p_id from wog_team_main a,wog_player b where a.t_id=b.t_id and b.p_id=".$user_id."");
		if(!$team_main)
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		if($team_main["p_id"]!=$user_id )
		{
			alertWindowMsg($lang['wog_act_team_noadm']);
		}
		$team=$DB_site->query("select a.t_j_id,b.p_name,b.p_lv,c.ch_name from wog_team_join a,wog_player b,wog_character c where a.t_id=".$team_main["t_id"]." and a.p_id=b.p_id and b.ch_id=c.ch_id order by a.t_j_dateline asc");
		$temp_s="";
		while($teams=$DB_site->fetch_array($team))
		{
			$temp_s.=";".$teams[0].",".$teams[1].",".$teams[2].",".$teams[3];
		}
		$DB_site->free_result($team);
		unset($teams);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.team_join_list('$temp_s')");
		unset($temp_s);
	}

	function team_get_save_member($user_id)
	{
		global $DB_site,$_POST,$lang,$wog_arry;
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_team_nosel']);
		}
//		$_POST["temp_id2"]=htmlspecialchars($_POST["temp_id2"]);

		$team_main=$DB_site->query_first("select a.t_id,a.p_id from wog_team_main a,wog_player b where a.t_id=b.t_id and b.p_id=".$user_id."");
		if(!$team_main)
		{
			alertWindowMsg($lang['wog_act_team_noteam']);
		}
		if($team_main["p_id"]!=$user_id )
		{
			alertWindowMsg($lang['wog_act_team_noadm']);
		}
		$team=$DB_site->query_first("select t_id,p_id from wog_team_join where t_j_id=".$_POST["temp_id2"]);
		if(!$team)
		{
			alertWindowMsg($lang['wog_act_team_cancel']);
		}
		if($team_main["t_id"]!=$team["t_id"])
		{
			alertWindowMsg($lang['wog_act_team_notset']);
		}

		$p=$DB_site->query_first("select t_id from wog_player where p_id=".$team["p_id"]);
		if($p["t_id"]>0)
		{
			$DB_site->query("delete from wog_group_join where p_id=".$team["p_id"]);
			alertWindowMsg($lang['wog_act_team_havgroup']);
		}
		$p_count=$DB_site->query_first("select t_peo from wog_team_main  where t_id=".$team["t_id"]."");
		if($p_count[0]>=$wog_arry["t_peo"])
		{
			alertWindowMsg($lang['wog_act_team_ful']);
		}
		$DB_site->query("update wog_player set t_id=".$team["t_id"]." where p_id=".$team["p_id"]."");
		$DB_site->query("update wog_team_main set t_peo=t_peo+1 where t_id=".$team["t_id"]."");
		$DB_site->query("delete from wog_team_join where p_id=".$team["p_id"]);
		unset($team);
		unset($p_count);
		unset($p);
		unset($team_main);
		showscript("parent.job_end(15)");
	}

	function team_clear()
	{
		global $DB_site;
		$clear_time=time()-(3*24*60*60);
		$sql="select t_id from wog_team_main where t_time<".$clear_time;
		$team=$DB_site->query($sql);
		while($teams=$DB_site->fetch_array($team))
		{
			$DB_site->query("update wog_player set t_id=0,p_support=0 where t_id=".$teams["t_id"]);
		}
		$DB_site->free_result($team);
		$sql="delete from wog_team_main where t_time<".$clear_time;
		$DB_site->query($sql);
	}
}
?>