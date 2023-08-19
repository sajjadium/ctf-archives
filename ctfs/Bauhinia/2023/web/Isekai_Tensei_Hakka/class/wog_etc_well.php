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

class wog_etc_well{

	function well_view()
	{
		global $DB_site,$wog_arry;
		$p=$DB_site->query_first("select cp.p_name,cp.p_at,cp.p_df,cp.p_mat
		,cp.p_mdf,cp.p_at,cp.p_df,cp.p_s,cp.p_url,cp.p_birth,cp.p_img_set,cp.p_img_url
		,cp.p_homename,cp.p_str,cp.p_life,cp.p_vit,cp.p_smart,cp.p_agl,cp.p_au,cp.p_be
		,cp.p_hp,cp.p_hpmax,cp.p_money,cp.p_lv,cp.p_exp,cp.p_url,cp.p_homename
		,cp.p_nextexp,cp.p_win,cp.p_lost,cp.p_sex,cp.i_img,cp.p_win_total,cp.p_place,cp.p_cdate
		,wog_character.ch_name,a.d_name as a_name ,b.d_name,e.d_name as e_name,d.d_name as dd_name
		,c.d_name as c_name,f.d_name as item_name,s.ch_name as s_ch_name
		from wog_cp cp left join wog_character on cp.ch_id=wog_character.ch_id 
		left join wog_character s on cp.p_ch_s_id=s.ch_id
		left join wog_df a on cp.a_id=a.d_id 
		left join wog_df b on cp.d_body_id=b.d_id 
		left join wog_df e on cp.d_head_id=e.d_id 
		left join wog_df d on cp.d_hand_id=d.d_id 
		left join wog_df c on cp.d_foot_id=c.d_id 
		left join wog_df f on cp.d_item_id=f.d_id 
		LIMIT 1 ");
		if($p[p_img_set]==1)
		{
			$p[i_img]=$p[p_img_url];
		}
		if($p)
		{
			$p[p_cdate]=player_age($p[p_cdate],$wog_arry["player_age"]);
			showscript("parent.well_view($p[p_win],$p[p_lost],$p[p_img_set],'$p[i_img]','$p[p_name]','$p[p_sex]','$p[ch_name]','$p[p_s]','$p[p_lv]','$p[p_exp]','$p[p_nextexp]','$p[p_money]','$p[p_hp]','$p[p_hpmax]',$p[p_str],$p[p_smart],$p[p_agl],$p[p_life],$p[p_vit],$p[p_au],$p[p_be],'$p[p_at]','$p[p_mat]','$p[p_df]','$p[p_mdf]','$p[a_name]','$p[d_name]','$p[e_name]','$p[dd_name]','$p[c_name]','$p[item_name]',$p[p_place],$p[p_birth],$p[p_cdate],".$wog_arry["del_day"].",".$wog_arry["f_time"].",'$p[p_url]','$p[p_homename]','$p[s_ch_name]','$p[p_win_total]',".$wog_arry["cp_mmoney"].",'');parent.f_count='".$wog_arry["f_count"]."'");
		}else
		{
			showscript("parent.no_cp(".$wog_arry["del_day"].",".$wog_arry["f_time"].",".$wog_arry["cp_mmoney"].");parent.f_count='".$wog_arry["f_count"]."'");
		}
		unset($p);
		unset($temp_s);
	}
}
?>