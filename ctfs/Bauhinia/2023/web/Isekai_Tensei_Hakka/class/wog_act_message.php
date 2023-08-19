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

class wog_act_message{

	function system_view1($user_id)
	{
		global $DB_site,$lang;
		$DB_site->query("delete from wog_message where dateline < ".(time()-(10*24*60*60))." ");
		$sql="select title,dateline from wog_message where p_id=".$user_id." order by m_id desc LIMIT 10";
		$pack=$DB_site->query($sql);
		$s="";
		while($packs=$DB_site->fetch_array($pack))
		{
			$s=$s.";".$packs[title].",".date("Y/m/d  g:i a",$packs[dateline]);
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($pack);
		showscript("parent.system_view('$s')");
		unset($s);
		unset($packs);
	}

	function phpbb_message($user_id,$user_name,$bbs_id)
	{
		global $DB_site,$_POST,$root_path,$lang,$db, $board_config;
		define('IN_PHPBB', true);
		$phpbb_root_path=$root_path;
		include_once($root_path . 'extension.inc');
		include_once($root_path . 'includes/bbcode.'.$phpEx);
		include_once($root_path . 'includes/functions.'.$phpEx);
		include_once($root_path . 'config.'.$phpEx);
		include_once($root_path . 'includes/constants.'.$phpEx);
		include_once($root_path . 'includes/db.'.$phpEx);
		$_POST["pay_id"]=addslashes(htmlspecialchars($_POST["pay_id"]));
		$board_config = array();
		$userdata = array();
		$sql = "SELECT *
			FROM " . CONFIG_TABLE;
		if( !($result = $db->sql_query($sql)) )
		{
			message_die(CRITICAL_ERROR, "Could not query config information", "", __LINE__, __FILE__, $sql);
		}
		while ( $row = $db->sql_fetchrow($result) )
		{
			$board_config[$row['config_name']] = $row['config_value'];
		}
		$p=$DB_site->query_first("SELECT p_bbsid FROM wog_player  WHERE p_name='".$_POST["pay_id"]."' ");
		if($p)
		{
			if($p["p_bbsid"]==0)
			{
				$db->sql_close();
				alertWindowMsg($lang['wog_act_nofroum_member']);
				
			}else
			{
				$sql = "INSERT  INTO phpbb_privmsgs(privmsgs_type,privmsgs_subject, privmsgs_from_userid, privmsgs_to_userid, privmsgs_date, privmsgs_ip)
				VALUES (5,'WOG訊息通知-".$user_name."', ".$bbs_id.",".$p["p_bbsid"].",".time(). ",'".get_ip(). "')";
				$DB_site->query($sql);
				$privmsg_sent_id=$DB_site->insert_id();
				$sql = "INSERT  INTO phpbb_privmsgs_text(privmsgs_text_id, privmsgs_bbcode_uid, privmsgs_text)
				VALUES ($privmsg_sent_id, '".make_bbcode_uid()."', '" . str_replace("\'", "''", addslashes($_POST["temp_id"])) . "')";
				$DB_site->query($sql);
				$sql = "update phpbb_users set user_new_privmsg=1 where user_id=".$p["p_bbsid"]."";
				$DB_site->query($sql);
				$db->sql_close();
				showscript("parent.job_end(7)");
			}
		}else
		{
			$db->sql_close();
			alertWindowMsg($lang['wog_act_noid']);
			
		}
		unset($p);
	}

	function vbb_message($user_id,$user_name,$bbs_id)
	{
		global $DB_site,$_POST,$lang;
		$_POST["pay_id"]=addslashes(htmlspecialchars($_POST["pay_id"]));
		$p=$DB_site->query_first("SELECT p_bbsid FROM wog_player WHERE p_name='".$_POST["pay_id"]."'");
		if($p)
		{
			$DB_site->query("INSERT INTO privatemessage (privatemessageid,userid,touserid,fromuserid,title,message,dateline)VALUES(NULL,$p[p_bbsid],$p[p_bbsid],$bbs_id,'".$user_name." 傳來WOG訊息','".addslashes($_POST["temp_id"])."',".time().")");
			showscript("parent.job_end(7)");
		}else
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		unset($p);
	}

	function dz_message($user_id,$user_name,$bbs_id)
	{
		global $DB_site,$_POST,$lang;
		$_POST["pay_id"]=addslashes(htmlspecialchars($_POST["pay_id"]));
		$p=$DB_site->query_first("SELECT p_bbsid FROM wog_player WHERE p_name='".$_POST["pay_id"]."'");
		if($p)
		{
			$DB_site->query("INSERT INTO cdb_pms (msgfrom, msgfromid, msgtoid, folder, new, subject, dateline, message)
				VALUES('$user_name', '$bbs_id', '$p[p_bbsid]', 'inbox', '1','".$user_name." 傳來WOG訊息', '".time()."', '".addslashes($_POST["temp_id"])."')");
			showscript("parent.job_end(7)");
		}else
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		unset($p);
	}

	function vbb3_message($user_id,$user_name,$bbs_id)
	{
		global $DB_site,$_POST,$lang,$root_path;
//		$tostring = array(); // the array of users who will appear in the pmtext record
//		$tostring["$user[userid]"] = $user['username'];
		$_POST["pay_id"]=addslashes(htmlspecialchars($_POST["pay_id"]));
		$p=$DB_site->query_first("SELECT p_bbsid FROM wog_player WHERE p_name='".$_POST["pay_id"]."'");
		$p2=$DB_site->query_first("SELECT username  FROM user WHERE userid =".$bbs_id."");
		if($p && $p2)
		{
			// insert private message text
			require_once($root_path.'includes/functions.php');
			$message = addslashes(fetch_censored_text($_POST["temp_id"]));
			$DB_site->query("INSERT INTO pmtext\n\t(fromuserid, fromusername, title, message, touserarray, iconid, dateline, showsignature, allowsmilie)\nVALUES\n\t($bbs_id, '" . addslashes($p2[username]) . "', '".$user_name." 傳來WOG訊息', '".$message."', '', 0, " . time() . ", 0, 1)");
			// get the inserted private message id
			$pmtextid = $DB_site->insert_id();
			// save a copy into $bbuserinfo's sent items folder
			$DB_site->query("INSERT INTO pm (pmtextid, userid, folderid, messageread) VALUES ($pmtextid, $bbs_id, 0, 0)");
			$DB_site->shutdown_query("UPDATE user SET pmtotal=pmtotal+1,pmunread=pmunread+1 WHERE userid=$bbs_id");
			showscript("parent.job_end(7)");
		}else
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		unset($p);
		unset($p2);
	}

}
?>