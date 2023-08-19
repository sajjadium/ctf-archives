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

class wog_act_pk{

	function pk_view($user_id)
	{
		global $DB_site,$lang;
		$sql="select p_pk_s,p_pk_money,p_pk_win,p_pk_lost
		from wog_player where  p_id=".$user_id." 
		";
		$p=$DB_site->query_first($sql);
		showscript("parent.pk_view($p[p_pk_s],'$p[p_pk_money]','$p[p_pk_win]','$p[p_pk_lost]')");
		unset($p);
	}

	function pk_setup($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(empty($_POST["pk_money"]))
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		if(!is_numeric($_POST["pk_money"]))
		{
			alertWindowMsg($lang['wog_act_errmoney']);
		}
		$money=(int)$_POST["pk_money"];
		$sql="select p_money from wog_player where p_id=".$user_id." ";
		$p=$DB_site->query_first($sql);
		if($money>$p[p_money] || ($money<1000 and $_POST["pk_setup"]=="1") || ($money>100000 and $_POST["pk_setup"]=="1"))
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}else
		{
			$DB_site->query("update wog_player set p_pk_s=".$_POST["pk_setup"].",p_pk_money=".$money." where p_id=".$user_id."");
			showscript("parent.job_end(3)");
		}
		unset($p);
	}

}
?>