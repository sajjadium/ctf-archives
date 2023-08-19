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

class wog_etc_peo{
	function peo_view($userid)
	{
		global $DB_site,$wog_arry,$forum_check,$root_path;
		eval($forum_check);
		if(!empty($userid))
		{
			$DB_site->query("update wog_player set p_online_time=".time().",p_ipadd='".$p_ip."' where p_id=".$userid." and p_lock=0");
			$p=$DB_site->query_first("select pe_dateline from wog_pet where pe_p_id=".$userid);
			if($p)
			{
				if(time()-$p["pe_dateline"] > $wog_arry["pet_fu_time"]*60)
				{
					$DB_site->query("update wog_pet set pe_dateline=".time().",pe_he=pe_he-1,pe_fu=pe_fu-".rand(5,10).",pe_hu=pe_hu+1 where pe_p_id=".$userid." and pe_st=0 ");
				}
			}
		}
		$datecut = time() - $wog_arry["offline_time"];
		$online=$DB_site->query("select p_name,p_sex,p_lv,p_pk_s,p_pk_money,p_place from wog_player where p_online_time > $datecut and p_lock=0 order by p_lv desc");
		$temp_s="";

		while($onlines=$DB_site->fetch_array($online))
		{
			$temp_s.=";".$onlines[0].",".$onlines[1].",".$onlines[2].",".$onlines[3].",".$onlines[4].",".$onlines[5];
		}
		$DB_site->free_result($online);
		unset($onlines);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.onlinelist('$temp_s')");
		unset($temp_s);
	}
}
?>