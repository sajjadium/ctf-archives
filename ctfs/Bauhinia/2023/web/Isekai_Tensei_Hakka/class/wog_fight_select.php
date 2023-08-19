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

class wog_fight_select{
	function fire($user_id,$mission_id=0,$m_monster_id=0,$m_kill_num=0,$m_need_num=0)
	{
		global $DB_site,$_POST,$wogclass,$wog_arry,$wog_event_class,$lang;
		$mission_chk=1;
		$mission_str=" and m_mission in (".$mission_id.",0)";
		$datecut=time()-$wog_arry["f_time"];
		$sql="select a.p_name,a.p_at,a.p_df,a.p_mat,a.p_mdf,a.p_s,a.p_agl,a.p_hp,a.p_hpmax,a.p_luck
		,a.p_sat_name,a.p_lv,a.p_exp,a.p_nextexp,a.p_life,a.p_smart,a.ch_id,a.a_id,a.p_ch_s_id,a.p_key,a.p_st
		,f.d_g_hp,f.d_name,a.d_item_id,a.i_img,a.p_img_set,a.p_img_url,a.p_au,a.t_id,g.d_s,a.p_bag,a.p_attempts
		from wog_player a left join wog_df f on a.d_item_id=f.d_id  
		left join wog_df g on a.a_id=g.d_id  
		where a.p_id=".$user_id." and a.p_act_time < $datecut and a.p_lock=0
		";
		if($p=$DB_site->query_first($sql))//check act_timt benig
		{
			if($p[p_hp]==0)
			{
				alertWindowMsg($lang['wog_fight_no_hp']);
			}
			if($p[p_key]!="" && $wog_arry["event_ans"])
			{
				$wog_event_class->event_start($user_id,$p["p_attempts"]);
			}
			if(rand(1,$wog_arry["event_ans_max"])==1 && $wog_arry["event_ans"])
			{
				$wog_event_class->event_creat($user_id);
			}
			if(eregi("[^0-9]",$_POST["act"]))
			{
				alertWindowMsg($lang['wog_fight_select_area']);
			}
			if( $m_monster_id==0 )
			{
				$mission_str="and m_mission=0";
				$mission_chk=0;
			}
			$sql="select * from wog_monster where m_place in (".$_POST["act"].",0) and m_meet <= ".rand(0,100)." ".$mission_str." ORDER BY RAND() LIMIT 1 ";
			$m=$DB_site->query_first($sql);
			if($m)//m date check start
			{
				echo charset();
				echo "<script language=JavaScript >\n";
				if($m["m_npc"]==1)
				{
					if(!empty($m_monster_id))
					{
						$m_monster_id=split(",",$m_monster_id);
					}
					if($mission_chk==1 && in_array($m[m_id],$m_monster_id))
					{
						echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]',$p[p_img_set],'$p[i_img]','?????','?????','?????','?????','?????','?????','$m[m_s]','$m[m_name]','$m[m_img]',0);\n";
						$sql="update wog_mission_book set m_kill_num=m_kill_num-1 where p_id=".$user_id." and m_id=".$mission_id;
						$DB_site->query($sql);
						echo "parent.setup_mname('".$m["m_name"]."');\n";
						$m["m_npc_message"]=str_replace("\r\n","&n",$m["m_npc_message"]);
						echo "parent.npc_message('".$m["m_npc_message"]."',".($m_kill_num-1).",".$m_need_num.");\n";
					}
				}else
				{
					if($p["t_id"]>0)
					{
						$datecut=time()-($wog_arry["t_time"]*60);
						$sql="select a.p_name,a.p_at,a.p_df,a.p_mat,a.p_mdf,a.p_s,a.p_agl,a.p_hp,a.p_hpmax
						,a.p_sat_name,a.p_lv,a.i_img,a.p_ch_s_id,a.p_img_set,a.p_img_url
						from wog_player a 
						where a.p_support=".$user_id." and a.t_id=".$p["t_id"]." and a.p_act_time > $datecut and a.p_place=".$_POST["act"]." and a.p_lock=0 ORDER BY RAND() LIMIT 1
						";
						$p_support=$DB_site->query_first($sql);
						if(!$p_support)
						{
							$p_support=NULL;
						}else
						{
							if($p_support[p_img_set]==1)
							{
								$p_support[i_img]=$p_support[p_img_url];
							}
							$p_support["p_at"]=$p_support["p_at"]*0.9;
							$p_support["p_mat"]=$p_support["p_mat"]*0.9;
							echo "parent.p_support_name='$p_support[p_name]';";
							echo "parent.p_support_img='$p_support[i_img]';";
						}
					$sql="select count(a.p_id) as members from wog_player a 
						where a.p_id<>".$user_id." and a.t_id=".$p["t_id"]." and a.p_act_time > $datecut and a.p_place=".$_POST["act"]." and a.p_lock=0";
					$my_member=$DB_site->query_first($sql);
					}else
					{
						$p_support=NULL;
					}

					$sql="select pe_id,pe_name,pe_at,pe_mt,pe_fu,pe_def,pe_hu,pe_type,pe_age,pe_he,pe_fi,pe_b_old,pe_mimg from wog_pet where pe_p_id=".$user_id." and pe_st=0";
					$pet=$DB_site->query_first($sql);
					if(!$pet)
					{
						$pet=NULL;
					}else
					{
						echo "parent.pet_pname='$pet[pe_name]';";
						echo "parent.pet_img='$pet[pe_mimg]';";
					}
					if($p[p_img_set]==1)
					{
						$p[i_img]=$p[p_img_url];
					}
					if(($p[p_at]*2)<$m[m_at] && ($p[p_mt]*2)<$m[m_mat])
					{
						echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]',$p[p_img_set],'$p[i_img]','?????','?????','?????','?????','$m[m_hp]','$m[m_hp]','$m[m_s]','$m[m_name]','$m[m_img]',0);\n";
					}else
					{
						echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]',$p[p_img_set],'$p[i_img]','$m[m_at]','$m[m_df]','$m[m_mat]','$m[m_mdf]','$m[m_hp]','$m[m_hp]','$m[m_s]','$m[m_name]','$m[m_img]',0);\n";
					}
					echo "fightrow = new Array(\"戰鬥開始\"";
					$wogclass->p_place=$_POST["act"];
					$wogclass->fight_count($user_id,$p,$m,0,$pet,$p_support,$my_member,$datecut);

					if($wogclass->win > $wogclass->lost)
					{
						if(!empty($m_monster_id))
						{
							$m_monster_id=split(",",$m_monster_id);
						}
//						if($mission_chk==0)
//						{
							if($p[d_name]=="捕捉器" && !$pet )
							{
								if(rand(1,15)==1)
								{
									echo ",\"parent.pet_break()\"";
									echo ",\"parent.d_item_name=''\"";
									$DB_site->query("update wog_player set d_item_id=0 where p_id=".$user_id);
								}
								if(rand(1,25)==1)
								{
									$sql="select count(pe_id) as num from wog_pet where pe_p_id=".$user_id." and pe_st in (0,2) ";
									$pet=$DB_site->query_first($sql);
									if($pet["num"]<3)
									{
										$pet=$wog_event_class->pet_stats();
										$sql="insert into wog_pet(pe_p_id,pe_name,pe_at,pe_mt,pe_fu,pe_def,pe_hu,pe_type,pe_age,pe_he,pe_fi,pe_dateline,pe_mname,pe_m_id,pe_b_dateline,pe_mimg,pe_st)";
										$sql.="values(".$user_id.",'".$m[m_name]."',".$pet[pe_at].",".$pet[pe_mt].",80,".$pet[pe_def].",0,".$pet[pe_type].",1,0,1,".(time()-20).",'".$m[m_name]."',".$m[m_id].",".time().",'".$m[m_img]."',2)";
										$DB_site->query($sql);
										$DB_site->query("update wog_player set d_item_id=0 where p_id=".$user_id);
										echo ",\"parent.pet_get('".$m[m_name]."')\"";
										echo ",\"parent.d_item_name=''\"";
									}
								}
							}
						if($mission_chk==1 && in_array($m[m_id],$m_monster_id))
						{
							$sql="update wog_mission_book set m_kill_num=m_kill_num-1 where p_id=".$user_id." and m_id=".$mission_id;
							$DB_site->query($sql);
							echo ",\"parent.mission_achieve(".($m_kill_num-1).",".$m_need_num.")\"";
						}
						if($m_[m_mission]==0 || ($m_[m_mission]==1 && $m_monster_id==$m[m_id]))
						{
							if($m[d_id] && rand(1,$m[m_topr])<=1 )//判斷是否撿到物品
							{
								$wog_event_class->get_item($user_id,$m[d_id],$p[p_st],$p[p_bag]);
							}
						}
					}else
					{
						if($pet!=NULL)
						{
							$DB_site->query("update wog_pet set pe_he=pe_he-".rand(0,1)." where pe_id=".$pet["pe_id"]);
						}
					}
					echo ");\n";
					echo "parent.set_fight(fightrow);\n";
				}
			}else
			{
				alertWindowMsg($lang['wog_fight_no_date']);
			}//m date check end
		}else
		{
			alertWindowMsg($wog_arry["f_time"].$lang['wog_fight_cant_fight1']);
		}//check act_time end
		unset($m);
		unset($p);
		unset($pet);
		echo "parent.cd(".$wog_arry["f_time"].")\n";
		echo "parent.p_sat_name='".$_POST["sat_name"]."'\n";
	}
	function fire_cp($user_id)
	{
		global $DB_site,$_POST,$wogclass,$wog_arry,$lang;
		$win=0;
		$lost=0;
    		$datecut=time()-$wog_arry["f_time"];
		$sql="select a.p_name,a.p_at,a.p_df,a.p_mat,a.p_mdf,a.p_s,a.p_agl,a.p_hp,a.p_hpmax,a.p_luck,a.p_sat_name,a.p_lv,a.p_birth
		,a.p_exp,a.p_nextexp,a.p_str,a.p_smart,a.p_life,a.p_vit,a.p_au,a.p_be,a.ch_id,a.p_url,a.p_homename,a.a_id,a.d_body_id,a.d_hand_id
		,a.d_head_id,a.d_foot_id,a.d_item_id,a.p_sex,a.p_money,a.p_win,a.p_lost,a.i_img,a.p_ch_s_id,a.p_place,a.p_cdate
		,f.d_g_hp,f.d_name,a.p_img_set,a.p_img_url
		from wog_player a left join wog_df f on a.d_item_id=f.d_id  
		where p_id=".$user_id." AND p_act_time < $datecut and p_lock=0
		";
		if($p=$DB_site->query_first($sql))//check act_timt benig
		{
			if($p[p_money]<$wog_arry["cp_mmoney"])
			{
				alertWindowMsg($lang['wog_fight_cp_money'].$wog_arry["cp_mmoney"]);
			}
			if($p[p_hp]==0)
			{
				alertWindowMsg($lang['wog_fight_no_hp']);
				
			}
			$sql="select p_name as m_name,p_at as m_at,p_df as m_df,p_mat as m_mat
			 ,p_mdf as m_mdf,p_agl as m_agl,p_lv as m_lv,p_s as m_s,p_sat_name as m_sat_name
			 ,p_hp as m_hp,p_hpmax as m_hpmaxv,p_hp as m_hpmax,p_pid as m_id,i_img as m_img
			 ,p_img_set as m_img_set,p_img_url as m_img_url
			 from wog_cp LIMIT 1 ";
			$m=$DB_site->query_first($sql);
			if($m)//m date check start
			{
				if($m[m_name]==$p[p_name])
				{
					alertWindowMsg($lang['wog_fight_cant_fight_me']);
				}
				if($p[p_img_set]==1)
				{
					$i_img=$p[p_img_url];
				}else
				{
					$i_img=$p[i_img];
				}
				if($m[m_img_set]==1)
				{
					$m[m_img]=$m[m_img_url];
				}
				echo charset();
				echo "<script language=JavaScript >\n";
				echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]',$p[p_img_set],'$i_img','$m[m_at]','$m[m_df]','$m[m_mat]','$m[m_mdf]','$m[m_hp]','$m[m_hpmaxv]','$m[m_s]','$m[m_name]','$m[m_img]',1);\n";
				$wogclass->cp_m_hp=0;
				$wogclass->p_place=$p[p_place];
				echo "fightrow = new Array(\"戰鬥開始\"";
				$cp=$wogclass->fight_count($user_id,$p,$m,-$wog_arry["cp_mmoney"],NULL,NULL,"",time());
				echo ");\n";
				echo "parent.set_fight(fightrow);\n";
				$cp_m_hp=$wogclass->cp_m_hp;
				if($wogclass->win > $wogclass->lost)
				{
					$DB_site->query("update wog_cp set p_name='$cp[p_name]',p_at=$cp[p_at]
					,p_mat=$cp[p_mat],p_df=$cp[p_df],p_mdf=$cp[p_mdf],p_s=$cp[p_s],p_url='$p[p_url]'
					,p_homename='$p[p_homename]',p_str=$cp[p_str],p_life=$cp[p_life],p_agl=$cp[p_agl]
					,p_smart=$cp[p_smart],p_hp=$cp[p_hpmax],p_sat_name='$cp[p_sat_name]'
					,p_hpmax=$cp[p_hpmax],p_win_total=1,p_lv=$cp[p_lv],a_id=$p[a_id],d_body_id=$p[d_body_id]
					,d_head_id=$p[d_head_id],d_hand_id=$p[d_hand_id],d_foot_id=$p[d_foot_id],d_item_id=$p[d_item_id]
					,p_sex=$p[p_sex],p_money=$p[p_money],p_exp=$cp[p_exp],p_nextexp=$cp[p_nextexp]
					,p_win=$cp[p_win]+1,p_lost=$cp[p_lost],i_img=$p[i_img],ch_id=$p[ch_id],p_pid=$user_id
					,p_au=$p[p_au],p_be=$p[p_be],p_ch_s_id=$p[p_ch_s_id],p_vit=$p[p_vit],p_place=$p[p_place],p_birth=$p[p_birth]
					,p_cdate=$p[p_cdate],p_img_set=$p[p_img_set],p_img_url='$p[p_img_url]'
					");
					echo "parent.cp_end('$p[p_name]')\n";
				}else{
					$DB_site->query("update wog_cp set p_hp=$cp_m_hp,p_win_total=p_win_total+1");
					$DB_site->query("update wog_player set p_money=p_money+".$wog_arry["cp_mmoney"]*0.7." where p_id=$m[m_id]");
				}
			}else
			{
				$DB_site->query("insert into wog_cp(p_name,p_at,p_mat,p_df,p_mdf,p_s,p_url,p_homename
				,p_str,p_life,p_vit,p_agl,p_smart,p_hp,p_sat_name,p_hpmax,p_win_total,p_lv,a_id,d_body_id,d_hand_id
				,d_head_id,d_foot_id,d_item_id,p_sex,p_money,p_exp,p_nextexp,p_win,p_lost,ch_id,i_img,p_pid
				,p_au,p_be,p_ch_s_id,p_place,p_birth,p_cdate,p_img_set,p_img_url
				)values('$p[p_name]',$p[p_at],$p[p_mat],$p[p_df],$p[p_mdf],$p[p_s],'$p[p_url]'
				,'$p[p_homename]',$p[p_str],$p[p_life],$p[p_vit],$p[p_agl],$p[p_smart],$p[p_hpmax]
				,'$p[p_sat_name]',$p[p_hpmax],1,$p[p_lv],$p[a_id],$p[d_body_id],$p[d_hand_id]
				,$p[d_head_id],$p[d_foot_id],$p[d_item_id],$p[p_sex],$p[p_money],$p[p_exp],$p[p_nextexp]
				,$p[p_win]+1,$p[p_lost],$p[ch_id],$p[i_img],$user_id,$p[p_au],$p[p_be],$p[p_ch_s_id],$p[p_place]
				,$p[p_birth],$p[p_cdate],$p[p_img_set],'$p[p_img_url]'
				)");
				echo charset();
				echo "<script language=JavaScript >\n";
				echo "parent.cp_end('$p[p_name]')\n";
			}//m date check end
		}else
		{
			alertWindowMsg($wog_arry["f_time"].$lang['wog_fight_cant_fight1']);
		}//check act_time end
		unset($m);
		unset($p);
		unset($cp);
		echo "parent.cd(".$wog_arry["f_time"].")\n";
		echo "parent.p_sat_name='".$_POST["sat_name"]."'\n";
	}
	function fire_pk($user_id)
	{
//		alertWindowMsg("關閉中");
		global $DB_site,$_POST,$wogclass,$wog_arry,$lang;
		$win=0;
		$lost=0;
    		$datecut=time()-$wog_arry["f_time"];
		$sql="select a.p_name,a.p_at,a.p_df,a.p_mat,a.p_mdf,a.p_s,a.p_agl,a.p_hp,a.p_hpmax,a.p_luck,a.p_sat_name,a.p_lv
		,a.p_exp,a.p_nextexp,a.p_life,a.ch_id,a.a_id,a.p_money,a.p_win,a.p_lost,a.i_img,a.p_ch_s_id
		,f.d_g_hp,f.d_name,a.d_item_id,a.p_img_set,a.p_img_url
		from wog_player a left join wog_df f on a.d_item_id=f.d_id  
		where p_id=".$user_id." AND p_act_time < $datecut and p_lock=0
		";
		if($p=$DB_site->query_first($sql))//check act_timt benig
		{
			if(trim($_POST["towho"])=="")
			{
				alertWindowMsg($lang['wog_fight_cant_pk1']);
				
			}
			if($p[p_hp]==0)
			{
				alertWindowMsg($lang['wog_fight_no_hp']);
				
			}
			$sql="select p_name as m_name,p_at as m_at,p_df as m_df,p_mat as m_mat
			,p_mdf as m_mdf,p_agl as m_agl,p_lv as m_lv,p_s as m_s,p_sat_name as m_sat_name
			,p_hpmax as m_hp,p_hpmax as m_hpmax,p_pk_money,p_money,i_img as m_img
			,p_img_set as m_img_set,p_img_url as m_img_url
			from wog_player where p_name='".trim($_POST["towho"])."' and p_pk_s=1 and (p_lv+10 >= $p[p_lv] and p_lv-10 <= $p[p_lv]) ";
	
			$m=$DB_site->query_first($sql);
			if($m)//m date check start
			{
				if($m[m_name]==$p[p_name])
				{
					alertWindowMsg($lang['wog_fight_cant_fight_me']);
					
				}
				if($p[p_money]<$m[p_pk_money])
				{
					alertWindowMsg($lang['wog_fight_pk_money'].$m[p_pk_money]);
					
				}
				if($m[p_money]<$m[p_pk_money])
				{
					$DB_site->query("update wog_player set p_pk_s=0 where p_name='".trim($_POST["towho"])."'");
					alertWindowMsg($lang['wog_fight_cant_pk2']);
					
				}
				if($p[p_img_set]==1)
				{
					$p[i_img]=$p[p_img_url];
				}
				if($m[m_img_set]==1)
				{
					$m[m_img]=$m[m_img_url];
				}
				echo charset();
				echo "<script language=JavaScript >\n";
				echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]',$p[p_img_set],'$p[i_img]','$m[m_at]','$m[m_df]','$m[m_mat]','$m[m_mdf]','$m[m_hp]','$m[m_hpmax]','$m[m_s]','$m[m_name]','$m[m_img]',1);\n";
				echo "fightrow = new Array(\"戰鬥開始\"";
				$cp=$wogclass->fight_count($user_id,$p,$m);
				echo ");\n";
				echo "parent.set_fight(fightrow);\n";
				if($wogclass->win > $wogclass->lost)
				{
					$DB_site->query("update wog_player set p_money=".($p[p_money]+$m[p_pk_money]).",p_pk_win=p_pk_win+1
					where p_id=".$user_id."");
					$DB_site->query("update wog_player set p_money=p_money-".$m[p_pk_money].",p_pk_lost=p_pk_lost+1 
					where p_name='".trim($_POST["towho"])."'");
				}else{
					$DB_site->query("update wog_player set p_money=".($p[p_money]-$m[p_pk_money]).",p_pk_lost=p_pk_lost+1
					where p_id=".$user_id."");
					$DB_site->query("update wog_player set p_money=p_money+".$m[p_pk_money].",p_pk_win=p_pk_win+1
					where p_name='".trim($_POST["towho"])."'");
				}
			}else
			{
				alertWindowMsg($lang['wog_fight_cant_pk3']);
			}//m date check end
		}else
		{
			alertWindowMsg($wog_arry["f_time"].$lang['wog_fight_cant_fight1']);
			
		}//check act_time end
		unset($m);
		unset($p);
		echo "parent.cd(".$wog_arry["f_time"].")\n";
		echo "parent.p_sat_name='".$_POST["sat_name"]."'\n";
	}


	function fire_a($user_id)
	{
		global $DB_site,$_POST,$wogclass,$wog_arry,$HTTP_SESSION_VARS,$lang;
		$win=0;
		$lost=0;
    	$datecut=time()-1;
		if(empty($_POST["p_id"]))
		{
			$_POST["p_id"]="0";
			$_POST["p_lv"]="10";
			$_POST["win"]="0";
			$_POST["s_id"]="0";
			$DB_site->query("update wog_player set p_a_lost=''
			where p_id=".$user_id."");
		}
		$sql="select a.p_name,a.p_at,a.p_df,a.p_mat,a.p_mdf,a.p_s,a.p_agl,a.p_hp,a.p_hpmax,a.p_luck,a.p_sat_name,a.p_lv
		,a.p_exp,a.p_nextexp,a.p_life,a.ch_id,a.a_id,a.p_money,a.p_win,a.p_lost,a.i_img,a.p_ch_s_id
		,f.d_g_hp,f.d_name,a.d_item_id 
		from wog_player a left join wog_df f on a.d_item_id=f.d_id  
		where p_id=".$user_id." AND p_act_time < $datecut and p_a_lost=''
		";
		if($p=$DB_site->query_first($sql))//check act_timt benig
		{
			if($p[p_hp]==0)
			{
				alertWindowMsg($lang['wog_fight_no_hp']);
			}
			$_POST["win"]=(int)$_POST["win"];
			$sql="select p_name as m_name,p_at as m_at,p_df as m_df,p_mat as m_mat
			,p_mdf as m_mdf,p_agl as m_agl,p_lv as m_lv,p_s as m_s,p_sat_name as m_sat_name
			,p_hpmax as m_hp,p_hpmax as m_hpmax,p_id as m_id,i_img as m_img
			from wog_player where p_id>".$_POST["p_id"]." and p_lv>=".$_POST["p_lv"]." and p_id<>".$user_id." order by p_lv,p_id LIMIT 1 ";
			$m=$DB_site->query_first($sql);
			if($m)//m date check start
			{
				$HTTP_SESSION_VARS["act_time"]=time()-$wog_arry["f_time"]+3;
				echo charset();
				echo "<script language=JavaScript >\n";
				echo "parent.fire_date('$p[p_at]','$p[p_df]','$p[p_mat]','$p[p_mdf]','$p[p_hp]','$p[p_hpmax]','$p[p_s]','$p[i_img]','$m[m_at]','$m[m_df]','$m[m_mat]','$m[m_mdf]','$m[m_hp]','$m[m_hpmax]','$m[m_s]','$m[m_name]','$m[m_img]',1);\n";
				echo "fightrow = new Array(\"戰鬥開始\"";
				$cp=$wogclass->fight_count($user_id,$p,$m);
				echo ");\n";
				echo "parent.set_fight(fightrow);\n";
				if($wogclass->win > $wogclass->lost)
				{
					$DB_site->query("update wog_player set p_a_win=".($_POST["win"]+1).",p_a_lost=''
					where p_id=".$user_id."");
					$cm=$DB_site->query_first("select count(p_id) as p_id from wog_player where p_id>".$m[m_id]." and p_lv=".$m[m_lv]." and p_id<>".$user_id." ");
					if($cm["p_id"]<=0)
					{
						$m=$DB_site->query_first("select p_lv as m_lv from wog_player where p_lv>".$m[m_lv]." and p_id<>".$user_id." order by p_lv,p_id LIMIT 1 ");
						$m[m_id]=1;
					}
//					echo "parent.setup_sat_name('".$_POST["sat_name"]."')\n";
					echo "parent.cont_fight(".$m[m_lv].",".$m[m_id].",".($_POST["win"]+1).",".$_POST["at_type"].")\n";
				}else
				{
					$DB_site->query("update wog_player set p_a_lost='".$m[m_name]."'
					where p_id=".$user_id."");
				}
			}else
			{
				alertWindowMsg($lang['wog_fight_no_select']);
			}//m date check end
		}else
		{
			alertWindowMsg($lang['wog_fight_cant_fight2']);
			
		}//check act_time end
		unset($m);
		unset($cm);
		unset($p);
		echo "parent.cd(".$wog_arry["f_time"].")\n";
	}


	function fire_group($user_id)
	{
		global $DB_site,$_POST,$wogclass,$wog_arry,$lang;
		$win=0;
		$lost=0;
		$temp_p="";
		$time=time();
		$g_f_t=date("G",$time);
		if($g_f_t<$wog_arry["g_f_stime"] || $g_f_t>=$wog_arry["g_f_etime"])
		{
			alertWindowMsg($lang['wog_fight_time'].$wog_arry["g_f_stime"].":00-".$wog_arry["g_f_etime"].":00");
		}
		if(empty($_POST["to_group"]))
		{
			alertWindowMsg($lang['wog_fight_select_group']);
		}
		if(empty($_POST["g_a_type"]))
		{
			alertWindowMsg($lang['wog_fight_no_area']);
		}
		$sql="select a.g_a_hp,a.g_a_id,b.g_name,b.g_money from wog_group_area a,wog_group_main b where a.g_id=".$_POST["to_group"]." and a.g_a_type=".$_POST["g_a_type"]." and a.g_id=b.g_id and g_fire=1";
		$p=$DB_site->query_first($sql);
		if(!$p)
		{
			alertWindowMsg($lang['wog_fight_select_error']);
		}
		if($p["g_a_hp"]<=0)
		{
			alertWindowMsg($lang['wog_fight_break_area']);
		}
		$de_hp=$p["g_a_hp"];
		$de_name=$p["g_name"];
		$de_money=$p["g_name"];
		$sql="select a.p_name,a.p_g_morale,a.p_g_number,a.p_g_id,a.p_str,a.p_smart,a.p_s,a.p_act_time,b.g_name from wog_player a,wog_group_main b where a.p_id=".$user_id." and a.p_g_id=b.g_id" ; //己方人物
		$p_group=$DB_site->query_first($sql);
		if(!$p_group)
		{
			alertWindowMsg($lang['wog_fight_no_ch']);
		}
		if($p_group["p_act_time"]>($time-$wog_arry["g_f_time"]))
		{
			alertWindowMsg($wog_arry["g_f_time"].$lang['wog_fight_cant_fight1']);
		}
		if($p_group["p_g_id"]<=0)
		{
			alertWindowMsg($lang['wog_fight_no_join_group']);
		}
		if($p_group["p_g_number"]<=0)
		{
			alertWindowMsg($lang['wog_fight_no_number']);
		}
		$temp_me=$p_group["p_name"].",".$p_group["p_g_number"].",".$p_group["p_g_morale"];
		$sql="select p_name,p_g_morale,p_g_number,p_str,p_smart,p_s,p_g_id,p_id from wog_player where p_g_id=".$_POST["to_group"]." and p_g_a_id=".$p["g_a_id"]." and p_g_number > 0 ORDER BY RAND() LIMIT 1"; //敵方人物
		$de_group=$DB_site->query_first($sql);
		echo charset();
		echo "<script language=JavaScript >\n";
		if($de_group)
		{
			$temp_de=$de_group["p_name"].",".$de_group["p_g_number"].",".$de_group["p_g_morale"];
			echo "parent.group_fire_title('".$_POST["g_a_type"]."','".$de_hp."','".$temp_me."','".$temp_de."');\n";
			$wogclass->fight_group($user_id,$p_group,$de_group,$de_hp,$_POST["g_a_type"]);
		}else
		{
			$temp_de="";
			$de_group["p_g_morale"]=100;
			$de_group["p_smart"]=300;
			$de_group["p_g_id"]=$_POST["to_group"];
			echo "parent.group_fire_title('".$_POST["g_a_type"]."','".$de_hp."','".$temp_me."','".$temp_de."');\n";
			$wogclass->fight_group_de($user_id,$p_group,$de_group,$de_hp,$_POST["g_a_type"]);
		}
		if($wogclass->win > $wogclass->lost)
		{
			$DB_site->query("update wog_group_main set g_win=g_win+1 where g_id=".$p_group[p_g_id]." ");
			$DB_site->query("update wog_group_main set g_lost=g_lost+1 where g_id=".$de_group[p_g_id]." ");
			$DB_site->query("insert into wog_group_event(g_b_id,g_b_body,g_b_dateline)values(".$p_group[p_g_id].",'".$p_group[g_name]."-".$p_group[p_name]." 攻打 ".$de_name." --->".$p_group[p_name]."戰勝',".$time.")");
			$sql="select count(g_a_id) as g_a_id from wog_group_area where g_id=".$_POST["to_group"]." and g_a_hp > 0";
			$p=$DB_site->query_first($sql);
			if($p[g_a_id]>=1)
			{
				$DB_site->query("insert into wog_group_event(g_b_id,g_b_body,g_b_dateline)values(".$de_group[p_g_id].",'".$de_name." 受到 ".$p_group[g_name]."-".$p_group[p_name]." 攻擊--->".$de_group[p_name]."戰敗',".$time.")");
			}else
			{
				$DB_site->query("insert into wog_group_event(g_b_id,g_b_body,g_b_dateline)values(".$p_group[p_g_id].",'".$de_name." 瓦解',".$time.")");
				$sql="select p_id from wog_player where p_g_id=".$_POST["to_group"]." ";
				$p=$DB_site->query($sql);
				while($ps=$DB_site->fetch_array($p))
				{
					$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$ps["p_id"].",'".$de_name." 瓦解',".$time.")");
				}
				$DB_site->free_result($p);
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_g_id=".$_POST["to_group"]);
				$DB_site->query("delete from wog_group_area where g_id=".$_POST["to_group"]);
				$DB_site->query("delete from wog_group_main where g_id=".$_POST["to_group"]);
				$DB_site->query("delete from wog_group_book where g_id=".$_POST["to_group"]."");
				$DB_site->query("delete from wog_group_event where g_b_id=".$_POST["to_group"]."");
			}
		}else{
			$DB_site->query("update wog_group_main set g_win=g_win+1 where g_id=".$de_group[p_g_id]." ");
			$DB_site->query("update wog_group_main set g_lost=g_lost+1 where g_id=".$p_group[p_g_id]." ");
			$DB_site->query("insert into wog_group_event(g_b_id,g_b_body,g_b_dateline)values(".$de_group[p_g_id].",'".$de_name." 受到 ".$p_group[g_name]."-".$p_group[p_name]." 攻擊--->".$de_group[p_name]."戰勝',".$time.")");
			$DB_site->query("insert into wog_group_event(g_b_id,g_b_body,g_b_dateline)values(".$p_group[p_g_id].",'".$p_group[g_name]."-".$p_group[p_name]." 攻打 ".$de_name." --->".$p_group[p_name]."戰敗',".$time.")");
		}
		unset($de_group);
		unset($p_group);
		unset($p);
		echo "parent.cd(".$wog_arry["g_f_time"].")\n";
	}
}
?>