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

class wog_act_arm{
	function arm_view($user_id)
	{
		global $DB_site,$_POST,$lang;
	//	check_type($_POST["temp_id"]);
		$sql="select ".$_POST["temp_id"]." from wog_item where p_id=".$user_id."  ";
		$pack=$DB_site->query_first($sql);
		if($pack[0]=="N/A" || empty($pack[0]))
		{
				alertWindowMsg($lang['wog_act_arm_view']);
		}else
		{
			$temp_item="";
			if($_POST["temp_id"]=="d_item_id")
			{
				$item_1=array();
				$item_2=array();
				$packs=split(",",$pack[0]);
				for($i=0;$i<count($packs);$i++)
				{
					$packss=split("\*",$packs[$i]);
					$item_1[]=$packss[0];
					$item_2[]=$packss[1];
					$temp_item.=",".$packss[0];
					
				}
				$temp_item=substr($temp_item,1,strlen($temp_item));
			}else
			{
				$temp_item=$pack[0];
			}
			
			
			$temp_str=$DB_site->query("select a.d_id,a.d_df,a.d_mdf,a.d_agl,a.d_money,a.d_name,a.d_at,a.d_mat,a.d_mstr,a.d_magl,a.d_msmart,b.ch_name,a.d_send,a.d_s
					from wog_df a left join wog_character b on b.ch_id=a.ch_id where a.d_id in ($temp_item)");
			$s="";
			while($temp_strs=$DB_site->fetch_array($temp_str))
			{
				$s.=";".$temp_strs[d_id].",".$temp_strs[d_df].",".$temp_strs[d_mdf].",".$temp_strs[d_agl].",".$temp_strs[d_money].",".$temp_strs[d_name].",".$temp_strs[d_at].",".$temp_strs[d_mat].",".$temp_strs[d_mstr].",".$temp_strs[d_magl].",".$temp_strs[d_msmart].",".$temp_strs[ch_name].",".$temp_strs[d_send].",".$temp_strs[d_s];
			}
			$DB_site->free_result($temp_str);
			unset($temp_strs);
			$s=substr($s,1,strlen($s));
			showscript("parent.arm_view('$s','$pack[0]','".$_POST["temp_id"]."')");
		}
		unset($pack);
		unset($temp);
	}

	function arm_setup($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_item_tool;
		$adds=$_POST["adds"];
		if(empty($adds))
		{
				alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		check_type($adds);
		$sql="select ".$a_id." from wog_item where p_id=".$user_id."  ";
		$item=$DB_site->query_first($sql);
		if($item[0]=="N/A" || $item[0]=="")
		{
			alertWindowMsg($lang['wog_act_errwork']);
		}else
		{
			$sql="select a.ch_pro,a.ch_id,a.d_df,a.d_mdf,a.d_agl,a.d_at,a.d_mat,a.d_name,a.d_type,a.d_g_str,a.d_g_smart,a.d_g_agl,a.d_g_life,a.d_g_vit,a.d_g_au,a.d_g_be,a.d_g_exp,a.d_g_bag
				 from wog_df a,wog_player b where a.d_id=".$adds." and b.p_id=".$user_id." and (a.ch_id=b.ch_id or a.ch_id=0) and b.p_agl>=a.d_magl and b.p_str>=a.d_mstr and b.p_smart>=a.d_msmart ";
			$pack=$DB_site->query_first($sql);
			if($pack)
			{
				$sql="select a.d_df,a.d_mdf,a.d_agl,a.d_at,a.d_mat,a.d_id from wog_df a,wog_player b where b.".$a_id."=a.d_id and b.p_id=".$user_id." ";
				$pack2=$DB_site->query_first($sql);
				if($pack[d_type]==6)
				{
					$items=array();
					if(!empty($item[0]))
					{
						$items=split(",",$item[0]);
					}
					$items=$wog_item_tool->item_out($user_id,$adds,1,$items);
					$DB_site->query("update wog_item set ".$a_id."='".implode(',',$items)."' where p_id=".$user_id." ");
					unset($items);
					if($pack[d_g_bag]==0)
					{
						$DB_site->query("update wog_player set p_df=p_df+".$pack[d_df]."
						,p_mdf=p_mdf+".$pack[d_mdf].",p_agl=p_agl+".$pack[d_agl].",p_at=p_at+".$pack[d_at].",p_mat=p_mat+".$pack[d_mat]."
						,p_str=p_str+".$pack[d_g_str].",p_smart=p_smart+".$pack[d_g_smart].",p_life=p_life+".$pack[d_g_life]."
						,p_vit=p_vit+".$pack[d_g_vit].",p_au=p_au+".$pack[d_g_au].",p_be=p_be+".$pack[d_g_be].",p_exp=p_exp+".$pack[d_g_exp]."
						where p_id=".$user_id." ");
						showscript("parent.lv_up2($pack[d_g_str],$pack[d_g_agl],$pack[d_g_smart],$pack[d_g_life],$pack[d_g_vit],$pack[d_g_au],$pack[d_g_be],$pack[d_g_exp])");
					}else
					{
						$DB_site->query("update wog_player set p_bag=".$pack[d_g_bag]."
						where p_id=".$user_id." ");
						showscript("parent.bag_up($pack[d_g_bag])");
					}
				}else
				{
					if($a_id=="d_item_id")
					{
						$s=$this->arm_item($item[0],$adds,$pack2);
					}else
					{
						$s=$this->arm_equit($item[0],$adds,$pack2);
					}

					if($pack[ch_id]>0)
					{
						$sql="select ch_".$pack[ch_id]." from wog_ch_exp where p_id=".$user_id;
						$ch=$DB_site->query_first($sql);
						if($ch[0] < $pack[ch_pro]){alertWindowMsg($lang['wog_act_arm_nosetup2']);}
						unset($ch);
					}
					if($pack2)
					{
						$DB_site->query("update wog_item set ".$a_id."='".$s."' where p_id=".$user_id." ");
						$DB_site->query("update wog_player set ".$a_id."=".$adds.",p_df=p_df-".$pack2[d_df]."+".$pack[d_df]."
						,p_mdf=p_mdf-".$pack2[d_mdf]."+".$pack[d_mdf].",p_agl=p_agl-".$pack2[d_agl]."+".$pack[d_agl]."
						,p_at=p_at-".$pack2[d_at]."+".$pack[d_at].",p_mat=p_mat-".$pack2[d_mat]."+".$pack[d_mat]."
						where p_id=".$user_id." ");
					}else
					{
						$DB_site->query("update wog_item set ".$a_id."='".$s."' where p_id=".$user_id." ");
						$DB_site->query("update wog_player set ".$a_id."=".$adds.",p_df=p_df+".$pack[d_df]."
						,p_mdf=p_mdf+".$pack[d_mdf].",p_agl=p_agl+".$pack[d_agl]."
						,p_at=p_at+".$pack[d_at].",p_mat=p_mat+".$pack[d_mat]."
						where p_id=".$user_id." ");
					}
					showscript("parent.arm_setup('".$a_id."','".$pack[d_name]."');parent.arm_end(1)");
				}
			}else
			{
				alertWindowMsg($lang['wog_act_arm_nosetup']);
			}
		}
		unset($pack);
		unset($packs);
		unset($pack2);
		unset($adds);
		unset($s);
		unset($item);
		unset($a_id);
	}

	function arm_move($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_arry,$temp_ss,$wog_item_tool;
		if(empty($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_noid']);
		}
		if(eregi("[<>'\", ;]", $_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_errword']);
		}
		$_POST["pay_id"]=trim($_POST["pay_id"]);
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		$adds=$_POST["temp_id2"];
		check_type($adds);
				$temp_ss=$wog_item_tool->item_out($user_id,$adds,$_POST["temp_id"]);
				$sql="select p_id,p_bag from wog_player where p_name='".htmlspecialchars($_POST["pay_id"])."'  ";
				$pay_id=$DB_site->query_first($sql);
				if(!$pay_id)
				{
					alertWindowMsg($lang['wog_act_arm_nomove']);
				}
				if($pay_id[0]==$user_id)
				{
					alertWindowMsg($lang['wog_act_arm_nomove_me']);
				}

				$sql="select d_name,d_send from wog_df where d_id=".$adds." ";
				$pay=$DB_site->query_first($sql);

				if($pay[1]==1)
				{
					alertWindowMsg($lang['wog_act_arm_nosend']);
				}

				$d_name=$pay[0];
				$sql="select p_name from wog_player where p_id=".$user_id." ";
				$pay=$DB_site->query_first($sql);
				$p_name=$pay[0];
				$sql="select ".$a_id." from wog_item where p_id=".$pay_id[0]."  ";
				$pay=$DB_site->query_first($sql);
				$temp_pack=array();
				if(!empty($pay[0]))
				{
					$temp_pack=split(",",$pay[0]);
				}
				$adds=$wog_item_tool->item_in($temp_pack,$adds,$_POST["temp_id"]);
				if($a_id=="d_item_id")
				{
					$bag=$wog_arry["item_limit"]+$pay_id[1];
				}else
				{
					$bag=$wog_arry["item_limit"];
				}

				if(count($adds) > $bag)
				{
					alertWindowMsg($lang['wog_act_bid_full']);
				}

				$DB_site->query("update wog_item set ".$a_id."='".implode(',',$adds)."' where p_id=".$pay_id[0]." ");
				$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_ss)."' where p_id=".$user_id." ");
				$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$pay_id[0].",'從 ".$p_name." 收到 ".$d_name." ',".time().")");
				showscript("parent.arm_end(2)");
		unset($pay);
		unset($items);
		unset($adds);
		unset($s);
		unset($s2);
		unset($item);
		unset($pay_id);
		unset($d_name);
		unset($p_name);
		unset($a_id);
	}

	function arm_sale($user_id)
	{
		global $DB_site,$_POST,$a_id,$temp_ss,$lang,$wog_item_tool;
		if(empty($_POST["temp_id2"]))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		$items=split(",",$_POST["temp_id2"]);
		check_type($items[0]);
		$temp_ss=$wog_item_tool->item_out($user_id,$items[0],$_POST["temp_id"]);
		$sql="select sum(d_money) as d_money  from wog_df where d_id in(".$items[0].") ";
		$pay=$DB_site->query_first($sql);
		$d_money=(isset($_POST["temp_id"]))?$pay[0]*0.5*$_POST["temp_id"]:$pay[0]*0.5;
		$DB_site->query("update wog_player set p_money=p_money+".$d_money." where p_id=".$user_id." ");
		$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_ss)."' where p_id=".$user_id." ");
		showscript("parent.arm_select()");
		unset($items);
		unset($d_money);
		unset($pay);
		unset($s2);
	}

	function arm_item($item,$adds,$pack2)
	{
		global $lang;
		$packs=split(",",$item);
		$s="";
		$chks=false;
		$chks2=true;
		for($i=count($packs)-1;$i>-1;$i--)
		{
			$packss=split("\*",$packs[$i]);
			if(($packss[0]!=$adds || $chks) && !empty($packss[0]))
			{
				if($pack2)
				{
					if($packss[0] == $pack2[d_id] && $chks2)
					{
						if($packss[1] >= 9)
						{
							$s.=",".$packss[0]."*".$packss[1];
						}else
						{
							$s.=",".$packss[0]."*".($packss[1]+1);
							$chks2=false;
						}
					}else
					{
						$s.=",".$packss[0]."*".$packss[1];
					}
				}else
				{
					$s.=",".$packss[0]."*".$packss[1];
				}
			}else
			{
				if($packss[1]>1)
				{
					$s.=",".$packss[0]."*".($packss[1]-1);
				}
				$chks=true;
			}
		}
		if($chks2 && $pack2)
		{
			$s.=",".$pack2[d_id]."*1";
		}
		if(!$chks)
		{
			alertWindowMsg($lang['wog_act_arm_noarm']);
		}
		$s=substr($s,1,strlen($s));
		return $s;
	}

	function arm_equit($item,$adds,$pack2)
	{
		global $lang;
		$packs=split(",",$item);
		$s="";
		$chks=false;
		for($i=0;$i<count($packs);$i++)
		{
			if(($packs[$i]!=$adds || $chks) && !empty($packs[$i]))
			{
				$s.=",".$packs[$i];
			}else
			{
				$chks=true;
			}
		}
		if(!$chks)
		{
			alertWindowMsg($lang['wog_act_arm_noarm']);
		}
		if($pack2)
		{
			$s.=",".$pack2[d_id];
		}
		$s=substr($s,1,strlen($s));
		return $s;
	}

}
?>