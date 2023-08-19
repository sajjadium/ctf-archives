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

class wog_act_shop_cache{

	function shop_cache()
	{
		global $DB_site,$_GET,$a_id,$lang;
		$sql="select a.d_id,a.d_df,a.d_mdf,a.d_agl,a.d_money,a.d_name,a.d_at,a.d_mat,a.d_mstr,a.d_magl,a.d_msmart,b.ch_name
			from wog_df a left join wog_character b on b.ch_id=a.ch_id
			where a.d_type=".$_GET["temp_id"]." and a.d_lv=".$_GET["temp_id2"]." and a.d_dbst=0 ";
		$pack=$DB_site->query($sql);
		$s="";
		while($packs=$DB_site->fetch_array($pack))
		{
			if($packs[ch_name]==null){$packs[ch_name]="";}
			$s=$s.";".$packs[d_id].",".$packs[d_df].",".$packs[d_mdf].",".$packs[d_agl].",".$packs[d_money].",".$packs[d_name].",".$packs[d_at].",".$packs[d_mat].",".$packs[d_mstr].",".$packs[d_magl].",".$packs[d_msmart].",".$packs[ch_name];
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($pack);
		$DB_site->close();
		echo "var s='".$s."'";
		unset($packs);
		unset($temp_where);
		unset($temp);
		unset($s);
		unset($ss);
		unset($p);
		unset($a_id);
		unset($df_total);
		compress_exit();
	}
}