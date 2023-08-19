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

class wog_act_job{

	function job_view($user_id)
	{
		global $DB_site,$lang;
		$sql="select p_agl,p_lv,p_str,p_smart,p_life,ch_id,p_money
		from wog_player where  p_id=".$user_id." 
		";
		$p=$DB_site->query_first($sql);
		if(empty($p))
		{
			alertWindowMsg($lang['wog_act_relogin']);
		}
		$c_exp=$DB_site->query_first("SELECT * FROM wog_ch_exp WHERE p_id=".$user_id." ");
		$sql="select ch_id,ch_name,ch_str,ch_smart,ch_life,ch_vit,ch_agl,ch_au,ch_be
		from wog_character where ch_mstr<=".$p[p_str]." and ch_magl<=".$p[p_agl]." and ch_msmart<=".$p[p_smart]." and ch_mlv <= ".$p[p_lv]." order by ch_mlv asc";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			$s=$s.";".$ps[ch_id]."|".$ps[ch_name]."|".$ps[ch_str]."|".$ps[ch_smart]."|".$ps[ch_life]."|".$ps[ch_vit]."|".$ps[ch_agl]."|".$ps[ch_au]."|".$ps[ch_be]."|".$c_exp["ch_".$ps[ch_id]];
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($p);
		unset($ps);
		if($s != "")
		{
			showscript("parent.job_view('$s')");
		}
		unset($s);
	}

	function job_setup($user_id,$job_id)
	{
		global $DB_site,$lang,$wog_item_tool,$a_id;
		if(empty($job_id))
		{
			alertWindowMsg($lang['wog_act_job_noselect']);
		}
		$sql="select p_agl,p_lv,p_str,p_smart,p_life,ch_id,a_id,d_body_id,d_head_id,d_hand_id,d_foot_id,d_item_id from wog_player where  p_id=".$user_id."";
		$p=$DB_site->query_first($sql);
		$sql="select ch_id,ch_name
		from wog_character where ch_mstr<=".$p[p_str]." and ch_magl<=".$p[p_agl]." and ch_msmart<=".$p[p_smart]." and ch_id=".$job_id."";
		$p3=$DB_site->query_first($sql);
		if($p3)
		{
			if(($p[a_id]+$p[d_body_id]+$p[d_head_id]+$p[d_hand_id]+$p[d_foot_id]+$p[d_item_id]) > 0)
			{
				$sql="select sum(d_df) as d_df,sum(d_mdf) as d_mdf,sum(d_agl) as d_agl,sum(d_at) as d_at,sum(d_mat) as d_mat
					from wog_df where d_id in (".$p[a_id].",".$p[d_body_id].",".$p[d_head_id].",".$p[d_hand_id].",".$p[d_foot_id].",".$p[d_item_id].")";
				$p2=$DB_site->query_first($sql);
				if($p2)
				{
					$DB_site->query("update wog_player set ch_id=".$job_id.",p_at=p_at-".$p2[d_at].",p_mat=p_mat-".$p2[d_mat].",p_df=p_df-".$p2[d_df].",p_mdf=p_mdf-".$p2[d_mdf].",p_agl=p_agl-".$p2[d_agl]."
									,a_id=0,d_body_id=0,d_head_id=0,d_hand_id=0,d_foot_id=0,d_item_id=0
									where p_id=".$user_id);
					$sql="select a_id,d_body_id,d_head_id,d_hand_id,d_foot_id,d_item_id from wog_item where p_id=".$user_id."";
					$p2=$DB_site->query_first($sql);
					if($p2[a_id]!="")
					{
						if($p[a_id]>0)$p2[a_id]=$p2[a_id].",".$p[a_id];
					}else
					{
						if($p[a_id]>0)$p2[a_id]=$p[a_id];
					}
					if($p2[d_body_id]!="")
					{
						if($p[d_body_id]>0) $p2[d_body_id]=$p2[d_body_id].",".$p[d_body_id];
					}else
					{
						if($p[d_body_id]>0) $p2[d_body_id]=$p[d_body_id];
					}
					if($p2[d_head_id]!="")
					{
						if($p[d_head_id]>0) $p2[d_head_id]=$p2[d_head_id].",".$p[d_head_id];
					}else
					{
						if($p[d_head_id]>0) $p2[d_head_id]=$p[d_head_id];
					}
					if($p2[d_hand_id]!="")
					{
						if($p[d_hand_id]>0) $p2[d_hand_id]=$p2[d_hand_id].",".$p[d_hand_id];
					}else
					{
						if($p[d_hand_id]>0) $p2[d_hand_id]=$p[d_hand_id];
					}
					if($p2[d_foot_id]!="")
					{
						if($p[d_foot_id]>0) $p2[d_foot_id]=$p2[d_foot_id].",".$p[d_foot_id];
					}else
					{
						if($p[d_foot_id]>0) $p2[d_foot_id]=$p[d_foot_id];
					}
					if($p2[d_item_id]!="")
					{
						$a_id="d_item_id";
						$p2[d_item_id]=split(",",$p2[d_item_id]);
						if($p[d_item_id]>0)
						{
							$p2[d_item_id]=$wog_item_tool->item_in($p2[d_item_id],$p[d_item_id],1);
						}
					}else
					{
						$p2[d_item_id]=array();
						if($p[d_item_id]>0) $p2[d_item_id][]=$p[d_item_id]."*1";
					}
					$sql="update wog_item set a_id='".$p2[a_id]."',d_body_id='".$p2[d_body_id]."',d_head_id='".$p2[d_head_id]."',d_hand_id='".$p2[d_hand_id]."',d_foot_id='".$p2[d_foot_id]."',d_item_id='".implode(',',$p2[d_item_id])."' where p_id=".$user_id;
					$DB_site->query($sql);
				}
			}else
			{
				$DB_site->query("update wog_player set ch_id=".$job_id.",a_id=0,d_body_id=0,d_head_id=0,d_hand_id=0,d_foot_id=0,d_item_id=0 where p_id=".$user_id);
			}
			showscript("parent.d_ch_name='".$p3[ch_name]."';parent.job_end(2)");
		}else
		{
			alertWindowMsg($lang['wog_act_job_err']);
		}
		unset($p);
		unset($p2);
		unset($p3);
	}

	function s_get($user_id,$job_id)
	{
		global $DB_site,$lang;
		if(empty($job_id))
		{
			alertWindowMsg($lang['wog_act_job_noselect']);
		}
		if((int)($job_id)<6)
		{
			alertWindowMsg($lang['wog_act_job_err']);
		}
		$p=$DB_site->query_first("SELECT ch_".$job_id." FROM wog_ch_exp WHERE p_id=".$user_id." ");
		if($p)
		{
			if($p[0]<3500)
			{
				alertWindowMsg($lang['wog_act_skill_nopoint']);
			}
			else
			{
				$DB_site->query("update wog_player set p_ch_s_id=".$job_id." where p_id=".$user_id." ");
				$sql="select ch_name from wog_character where ch_id=".$job_id."";
				$p2=$DB_site->query_first($sql);
				showscript("parent.d_s_ch_name='".$p2[ch_name]."';parent.job_end(8)");
			}
		}else
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		unset($p);
		unset($p2);
	}
	
}
?>