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

class wog_act_chara{
	var $group_id="";
	function chara_make() //創造新增頁面
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$temp_i_id="";
		$img=$DB_site->query("select i_id from wog_img order by i_id asc");
		while($imgs=$DB_site->fetch_array($img))
		{
		  $temp_i_id.=",".$imgs["i_id"];
		}
		$DB_site->free_result($img);
	
		unset($imgs);
		$temp_i_id=substr($temp_i_id,1,strlen($temp_i_id));
		$temp_ch="";
		$ch=$DB_site->query("select ch_id,ch_name from wog_character where ch_mlv=1 ");
		while($chs=$DB_site->fetch_array($ch))
		{
			$temp_ch.=";".$chs["ch_id"].",".$chs["ch_name"];
		}
		$DB_site->free_result($ch);
		unset($chs);
		$temp_ch=substr($temp_ch,1,strlen($temp_ch));
		include("wog_chara_make.php");
		echo charset();
		echo "<script language=JavaScript >\n";
		echo "setup_temp_i_id('$temp_i_id');\n";
		echo "setup_temp_ch('$temp_ch');\n";
		echo "chara_make_view('$wog_arry[total_point]');\n";
		echo "</script>\n";
	}

	function chara_save($bbs_id) //儲存新增角色 
	{
		global $DB_site,$_POST,$wog_arry,$lang,$forum_message;
		$errormessage="";
		if(!isset($_POST["id"]) || !isset($_POST["pass"])  || !isset($_POST["sex"]) || !isset($_POST["s"]) || !isset($_POST["email"]) || !isset($_POST["birth"]))
		{
			$errormessage.=$lang['wog_act_chara_errdata'];
		}
		if(empty($_POST["id"]) || empty($_POST["pass"])  || empty($_POST["sex"]) || empty($_POST["s"]) || empty($_POST["email"]) )
		{
			$errormessage.=$lang['wog_act_chara_errdata'];
		}
		if (eregi("[<>'\", ;]", $_POST["id"]) || eregi("[<>'\", ]", $_POST["pass"]) || eregi("[<>'\", ;]", $_POST["sat_name"])) 
		{
			$errormessage.=$lang['wog_act_errword'];
		}
		if((int)$_POST["str"]<=0 || (int)$_POST["smart"]<=0 || (int)$_POST["agl"]<=0 || (int)$_POST["life"]<=0 )
		{
			$errormessage.=$lang['wog_act_chara_errpoint'];
		}
		if( ((int)$_POST["str"]+(int)$_POST["smart"]+(int)$_POST["agl"]+(int)$_POST["life"]) > $wog_arry["total_point"] )
		{
			$errormessage.=$lang['wog_act_chara_fulpoint'].$wog_arry["total_point"].",";
		}
		if((int)$_POST["ch"] > 8)
		{
			$errormessage.=$lang['wog_act_chara_errjob'];
		}
		if((int)$_POST["birth"] > 3)
		{
			$errormessage.=$lang['wog_act_chara_errdata'];
		}

		if($p=$DB_site->query_first("select p_id from wog_player where p_name='".trim($_POST["id"])."'"))
		{
			$errormessage.=$lang['wog_act_chara_usedid'];
		}
		if(empty($forum_message))
		{
			if($p=$DB_site->query_first("select count(p_id) as p_id from wog_player where p_email='".trim($_POST["email"])."'"))
			{
				if($wog_arry["player_num"] <= $p[0])
				{
					$errormessage.=$lang['wog_act_chara_fulnum'];
				}
			}
		}

		if(!empty($forum_message))
		{
			if($p=$DB_site->query_first("select count(p_bbsid) as p_bbsid from wog_player where p_bbsid=".$bbs_id.""))
			{
				if($wog_arry["player_num"] <= $p[0])
				{
					$errormessage.=$lang['wog_act_chara_fulnum'];
				}
			}
		}

		if(empty($errormessage))
		{
//  	     srand ((float) microtime() * 10000000); //php 4.2 以上可以不用
			$luck=rand(1,10);
			$DB_site->query("insert into wog_player(p_name,p_at,p_df,p_mat,p_mdf,p_s
			,p_url,p_homename,p_str,p_life,p_vit,p_smart,p_agl,p_au,p_be,p_hp,p_luck,p_sat_name
			,p_hpmax,ch_id,p_money,p_lv,p_exp,p_nextexp,p_sex
			,p_password,i_img,p_cdate,p_email,p_online_time,p_bbsid,p_birth
			)values('".htmlspecialchars(trim($_POST["id"]))."',".($_POST["str"]+8).",".($_POST["life"]+8).
			",".($_POST["smart"]+8).",".($_POST["smart"]+8).",".$_POST["s"].",'".$_POST["url"]."','".$_POST["site"]."'
			,".($_POST["str"]+8).",".($_POST["life"]+8).",8,".($_POST["smart"]+8).",".($_POST["agl"]+8).",8,8
			,45,".$luck.",'".htmlspecialchars(trim($_POST["sat_name"]))."',45,".$_POST["ch"].",2000,1
			,0,1000,'".$_POST["sex"]."','".$_POST["pass"]."'
			,".$_POST["i_id"].",".time().",'".htmlspecialchars(trim($_POST["email"]))."',".time().",".$bbs_id.",".$_POST["birth"]."
			)");
			$user_id=$DB_site->insert_id();
			$DB_site->query("insert into wog_item(p_id,a_id,d_body_id,d_foot_id,d_hand_id,d_head_id,d_item_id
			)values(".$user_id.",'','','','','','')");
		    $DB_site->query("insert into wog_ch_exp(p_id)values(".$user_id.")");
		}else
		{
			alertWindowMsg($errormessage);
			
		}
		unset($errormessage);
		setcookie("wog_cookie",$user_id);
		setcookie("wog_key",$key);
		setcookie("wog_cookie_name",trim($_POST["id"]));
		setcookie("wog_bbs_id",$bbs_id);
		setcookie("wog_cookie_debug",md5($user_id.$bbs_id.$wog_arry[cookie_debug]));
		$this->show_chara($user_id,$bbs_id,1);
		showscript("parent.peolist.document.location.reload()");
	}

	function login($bbs_id,$p_ip)
	{
	
		global $DB_site,$_POST,$wog_arry,$lang,$forum_message;
		if (eregi("[<>'\", ]", $_POST["id"]) || eregi("[<>'\", ]", $_POST["pass"]))  
		{
			alertWindowMsg($lang['wog_act_errword']);
		}
		$p=$DB_site->query("select p_id from wog_player where p_online_time < ".(time()-($wog_arry["del_day"]*24*60*60))." and p_st <= 0"); //刪除角色
		while($ps=$DB_site->fetch_array($p))
		{
			$this->kill_sub($ps["p_id"]);
		}
		$p=$DB_site->query_first("select p_id,p_name,p_lock,p_bbsid,p_st,p_lock_time from wog_player where p_name='".$_POST["id"]."' and p_password='".$_POST["pass"]."' ");
		if($p)
		{
				if($p[p_lock]==1)
				{
					$lock_time=$p[p_lock_time]+($wog_arry["unfreeze"]*60*60);
					if($lock_time>time())
					{
						alertWindowMsg($lang['wog_act_chara_nologin']);
					}else
					{
						$sql="update wog_player set p_key='',p_lock=0,p_attempts=0 where p_id=".$p[p_id];
						$DB_site->query($sql);
					}
				}
				if(!empty($forum_message))
				{
					if($p[p_bbsid]!=$bbs_id)
					{
						alertWindowMsg($lang['wog_act_chara_error_creatid']);
					}
					$datecut = time() - $wog_arry["offline_time"];
					$check_time=$DB_site->query_first("select p_online_time from wog_player where p_bbsid=".$bbs_id." and p_online_time > $datecut and p_id<>".$p[p_id]."");
					if($check_time)
					{
						alertWindowMsg($lang['wog_act_chara_sameid']);
					}
				}
				if($p[p_st]==0)
				{
					$datecut = time() - $wog_arry["offline_time"];
					$online=$DB_site->query_first("select count(p_name) as num from wog_player where p_online_time > $datecut");
					if($online[num]>=$wog_arry["online_limit"])
					{
						showscript("parent.incd(".$wog_arry["login_time"].")");
					}
				}
				$m_item=$DB_site->query_first("select a.m_id,a.m_area_id from wog_mission_main a,wog_mission_book b where b.p_id=".$p[p_id]." and b.m_status=0 and a.m_id=b.m_id");
				setcookie("wog_cookie",$p[p_id]);
				setcookie("wog_cookie_name",$p[p_name]);
				setcookie("wog_bbs_id",$bbs_id);
				setcookie("wog_cookie_debug",md5($p[p_id].$bbs_id.$wog_arry[cookie_debug]));
				setcookie("wog_cookie_mission_id",$m_item["m_id"]);
				setcookie("wog_cookie_mission_area",$m_item["m_area_id"]);
				$this->show_chara($p[p_id],$bbs_id,1);
				$sql="update wog_player set p_ipadd='".$p_ip."' where p_id=".$p[p_id];
				$DB_site->query($sql);
				showscript("parent.peolist.document.location.reload()");
		}else
		{
			alertWindowMsg($lang['wog_act_chara_errlogin']);
		}
		unset($p);
	}

	function revive($user_id)
	{
		global $DB_site,$wog_arry,$lang;
		$DB_site->query("update wog_player set p_hp=p_hpmax,p_exp=p_exp*0.8 where p_id=".$user_id);
		showscript("parent.job_end(19)");
	}

	function logout($user_id)
	{
		global $DB_site,$wog_arry,$lang;
		$DB_site->query("update wog_player set p_online_time=".(time() - $wog_arry["offline_time"])." where p_id=".$user_id);
		cookie_clean();
		showscript("parent.document.URL='".$wog_arry["logout_url"]."';");
	}

	function show_chara($user_id,$bbs_id,$s)
	{
		global $DB_site,$lang,$wog_arry;
		if(empty($user_id))
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		if($s<3)
		{
			$sql="select w.p_name,w.p_at,w.p_df,w.p_mat
			,w.p_mdf,w.p_at,w.p_df,w.p_s,w.p_url
			,w.p_homename,w.p_str,w.p_life,w.p_smart,w.p_agl
			,w.p_au,w.p_be,w.p_place,w.p_vit,w.p_birth,w.p_img_set,w.p_img_url
			,w.p_hp,w.p_hpmax,w.p_money,w.p_lv,w.p_exp,w.p_cdate
			,w.p_nextexp,w.p_win,w.p_lost,w.p_url,w.p_homename
			,w.p_sex,w.i_img,w.p_sat_name,wog_character.ch_name,a.d_name as a_name,s.ch_name as s_ch_name
			,b.d_name as body_name,e.d_name as head_name,d.d_name as hand_name,c.d_name as foot_name,f.d_name as item_name,g.g_name,g.g_id
			from wog_player w left join wog_character on w.ch_id=wog_character.ch_id 
			left join wog_group_main g on w.p_g_id=g.g_id 
			left join wog_character s on w.p_ch_s_id=s.ch_id 
			left join wog_df a on w.a_id=a.d_id 
			left join wog_df b on w.d_body_id=b.d_id 
			left join wog_df e on w.d_head_id=e.d_id 
			left join wog_df d on w.d_hand_id=d.d_id 
			left join wog_df c on w.d_foot_id=c.d_id 
			left join wog_df f on w.d_item_id=f.d_id 
			where w.p_id=".$user_id."";
		}else
		{
			$sql="select w.p_name,w.p_at,w.p_df,w.p_mat
			,w.p_mdf,w.p_at,w.p_df,w.p_s,w.p_url
			,w.p_homename,w.p_str,w.p_life,w.p_smart,w.p_agl
			,w.p_au,w.p_be,w.p_place,w.p_vit,w.p_img_set,w.p_img_url
			,w.p_hp,w.p_hpmax,w.p_money,w.p_lv,w.p_exp
			,w.p_nextexp,w.p_win,w.p_lost,w.p_url,w.p_homename
			,w.p_sex,w.i_img,w.p_sat_name,g.g_name,g.g_id
			from wog_player w left join wog_group_main g on w.p_g_id=g.g_id 
			where w.p_id=".$user_id."";
		}
		echo charset();
		echo "<script language=JavaScript >\n";
		$p=$DB_site->query_first($sql);
		echo "parent.p_group='".$p["g_name"]."';\n";
		$p[p_cdate]=player_age($p[p_cdate],$wog_arry["player_age"]);
		if($p[p_img_set]==1)
		{
			$p[i_img]=$p[p_img_url];
		}
		if($s==1)
		{
			echo "parent.login_view($p[p_win],$p[p_lost],$p[p_img_set],'$p[i_img]','$p[p_name]','$p[p_sex]','$p[ch_name]','$p[p_s]','$p[p_lv]','$p[p_exp]','$p[p_nextexp]','$p[p_money]','$p[p_hp]','$p[p_hpmax]','$p[p_str]','$p[p_smart]','$p[p_agl]','$p[p_life]','$p[p_vit]','$p[p_au]','$p[p_be]','$p[p_at]','$p[p_mat]','$p[p_df]','$p[p_mdf]','$p[a_name]','$p[body_name]','$p[head_name]','$p[hand_name]','$p[foot_name]','$p[item_name]','$p[p_url]','$p[p_homename]','$p[s_ch_name]','$p[p_sat_name]',$p[p_place],$p[p_birth],$p[p_cdate],'$bbs_id');\n";
		}elseif($s==2)
		{
			echo "parent.cp_view($p[p_win],$p[p_lost],$p[p_img_set],'$p[i_img]','$p[p_name]','$p[p_sex]','$p[ch_name]','$p[p_s]','$p[p_lv]','$p[p_exp]','$p[p_nextexp]','$p[p_money]','$p[p_hp]','$p[p_hpmax]','$p[p_str]','$p[p_smart]','$p[p_agl]','$p[p_life]','$p[p_vit]','$p[p_au]','$p[p_be]','$p[p_at]','$p[p_mat]','$p[p_df]','$p[p_mdf]','$p[a_name]','$p[body_name]','$p[head_name]','$p[hand_name]','$p[foot_name]','$p[item_name]',$p[p_place],$p[p_birth],$p[p_cdate],'$p[p_url]','$p[p_homename]','$p[s_ch_name]');\n";
		}elseif($s==3)
		{
			echo "parent.show_status($p[p_win],$p[p_lost],$p[p_img_set],'$p[i_img]','$p[p_sex]','$p[p_s]','$p[p_lv]','$p[p_exp]','$p[p_nextexp]','$p[p_money]','$p[p_hp]','$p[p_hpmax]','$p[p_str]','$p[p_smart]','$p[p_agl]','$p[p_life]','$p[p_vit]','$p[p_au]','$p[p_be]','$p[p_at]','$p[p_mat]','$p[p_df]','$p[p_mdf]',$p[p_place]);\n";
		}
		$this->group_id=$p["g_id"];
		echo "</script>\n";
		unset($p);
	}

	function cp_view()
	{
		global $DB_site,$lang,$wog_arry;
		$p=$DB_site->query_first("select cp.p_name,cp.p_at,cp.p_df,cp.p_mat
		,cp.p_mdf,cp.p_at,cp.p_df,cp.p_s,cp.p_url,cp.p_birth,cp.p_cdate
		,cp.p_homename,cp.p_str,cp.p_life,cp.p_vit,cp.p_smart,cp.p_agl,cp.p_au,cp.p_be
		,cp.p_hp,cp.p_hpmax,cp.p_money,cp.p_lv,cp.p_exp,cp.p_url,cp.p_homename,cp.p_img_set,cp.p_img_url
		,cp.p_nextexp,cp.p_win,cp.p_lost,cp.p_sex,cp.i_img,cp.p_win_total,cp.p_place
		,wog_character.ch_name,a.d_name as a_name ,b.d_name,e.d_name as e_name,d.d_name as dd_name
		,c.d_name as c_name,f.d_name as item_name,s.ch_name as s_ch_name,g.g_name
		from wog_cp cp left join wog_character on cp.ch_id=wog_character.ch_id 
		left join wog_group_main g on cp.p_g_id=g.g_id 
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
		$a_act=$DB_site->query("select p_name,p_a_win from wog_player order by p_a_win desc limit 3");
		$p[p_cdate]=player_age($p[p_cdate],$wog_arry["player_age"]);
		showscript("parent.p_group='".$p["g_name"]."';parent.cp_view($p[p_win],$p[p_lost],$p[p_img_set],'$p[i_img]','$p[p_name]','$p[p_sex]','$p[ch_name]','$p[p_s]','$p[p_lv]','$p[p_exp]','$p[p_nextexp]','$p[p_money]','$p[p_hp]','$p[p_hpmax]','$p[p_str]','$p[p_smart]','$p[p_agl]','$p[p_life]','$p[p_vit]','$p[p_au]','$p[p_be]','$p[p_at]','$p[p_mat]','$p[p_df]','$p[p_mdf]','$p[a_name]','$p[d_name]','$p[e_name]','$p[dd_name]','$p[c_name]','$p[item_name]',$p[p_place],$p[p_birth],$p[p_cdate],'$p[p_url]','$p[p_homename]','$p[s_ch_name]','$p[p_win_total]','')");
		unset($p);
	}

	function kill()
	{
		global $DB_site,$_POST,$lang;
		$sql="select p_id from wog_player where p_name='".trim($_POST["id"])."' and p_password='".$_POST["password"]."'";
		$p=$DB_site->query_first($sql);
		if($p)
		{
			$this->kill_sub($p["p_id"]);
			showscript("parent.job_end(1)");
		}else
		{
			alertWindowMsg($lang['wog_act_kill']);
		}
		unset($p);
	}

	function kill_sub($p_id)
	{
		global $DB_site,$lang;
		$group_main=$DB_site->query_first("select a.g_id,a.g_adm_id1,a.g_adm_id2 from wog_group_main a,wog_player b where a.g_id=b.p_g_id and b.p_id=".$p_id);
		if($group_main)
		{
			if($p_id==$group_main["g_adm_id1"])
			{
				$DB_site->query("delete from wog_group_main where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_area where g_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_event where g_b_id=".$group_main["g_id"]."");
				$DB_site->query("delete from wog_group_book where g_id=".$group_main["g_id"]."");
				$DB_site->query("update wog_player set p_g_id=0,p_g_a_id=0,p_g_number=0,p_g_morale=0 where p_g_id=".$group_main["g_id"]."");
			}else
			{
				$DB_site->query("update wog_group_main set g_peo=g_peo-1 where g_id=".$group_main["g_id"]."");
			}
		}
		$DB_site->query("delete from wog_player where p_id=".$p_id."");
		$DB_site->query("delete from wog_item where p_id=".$p_id."");
		$DB_site->query("delete from wog_ch_exp where p_id=".$p_id."");
		$DB_site->query("delete from wog_sale where p_id=".$p_id."");
		$DB_site->query("delete from wog_pet where pe_p_id=".$p_id."");
		$DB_site->query("delete from wog_mission_book where p_id=".$p_id."");
		unset($group_main);
	}

	function system_view2($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$towho=trim($_POST["towho"]);
		if($towho=="")
		{
			alertWindowMsg($lang['wog_act_sysview_noselect']);
			
		}
		$have_price=$DB_site->query_first("select p_money from wog_player where p_id=".$user_id."");
		if($have_price[p_money] < $wog_arry["view2_money"])
		{
			alertWindowMsg(sprintf($lang['wog_act_nomoney_must'], $wog_arry["view2_money"]));
			
		}else
		{
			$DB_site->query("update wog_player set p_money=p_money-".$wog_arry["view2_money"]." where p_id=".$user_id."");
		}
		$p=$DB_site->query_first("select p_id from wog_player where p_name='".$towho."'");
		if($p)
		{
			$this->show_chara($p["p_id"],$userid,2);
		}else
		{
			alertWindowMsg($lang['wog_act_noid']);
			
		}
		unset($have_price);
		unset($p);
	}

	function get_password($email)
	{
		global $DB_site,$lang;
		$p=$DB_site->query_first("SELECT p_email FROM wog_player WHERE p_email='".addslashes(htmlspecialchars($email))."'");
		if($p){
			$temp_s=$lang['wog_etc_email_body1']."\r\n";
			$get_p=$DB_site->query("SELECT p_name,p_password from wog_player where p_email='".addslashes(htmlspecialchars($email))."'");
			while($get_ps=$DB_site->fetch_array($get_p))
			{
				$temp_s.=sprintf($lang['wog_etc_email_body2'],$get_ps[p_name])."\r\n";
				$temp_s.=sprintf($lang['wog_etc_email_body3'],$get_ps[p_password])."\r\n";
			}
			mail($p[p_email],$lang['wog_etc_email_subject'],$temp_s,"From: \"Online FF Battle - WOG\" <iqstar@pchome.com.tw>\r\n"."Reply-To: iqstar@pchome.com.tw\r\n"."X-Mailer: PHP/" . phpversion());
			alertWindowMsg($lang['wog_etc_email_send']);
		}
		else
		{
			alertWindowMsg($lang['wog_etc_email_error']);
		}
	}
}
?>