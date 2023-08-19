<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/09/17
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

class wog_act_syn{
	function syn_view($user_id) 
	{
		global $DB_site,$_POST,$lang; 
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

			$temp_str=$DB_site->query("select d_id,d_df,d_mdf,d_agl,d_mstr,d_magl,d_msmart,d_money,d_name,d_at,d_mat from wog_df where d_id in ($temp_item)"); 
			$s=""; 
			while($temp_strs=$DB_site->fetch_array($temp_str)) 
			{ 
				$s.=";".$temp_strs[d_id].",".$temp_strs[d_df].",".$temp_strs[d_mdf].",".$temp_strs[d_agl].",".$temp_strs[d_money].",".$temp_strs[d_name].",".$temp_strs[d_at].",".$temp_strs[d_mat].",".$temp_strs[d_mstr].",".$temp_strs[d_magl].",".$temp_strs[d_msmart]; 
			} 
			$DB_site->free_result($temp_str); 
			unset($temp_strs); 
			$s=substr($s,1,strlen($s)); 
			showscript("parent.syn_view('$s','$pack[0]')"); 
		}
		unset($pack); 
		unset($temp); 
	}
	function syn_purify($user_id) 
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_item_tool,$wog_arry;
		if(empty($_POST["syn_way"])){alertWindowMsg($lang['wog_act_syn_noway']);} 
		if(count($_POST["syn"])<=1){alertWindowMsg($lang['wog_act_syn_error']);} 
		$syn=$_POST["syn"];
		$syn_debug=0;
		check_type($_POST["syn"][0]);
		$sql="select ".$a_id." from wog_item where p_id=".$user_id.""; 
		$item=$DB_site->query_first($sql); 
		if($item[0]=="N/A" || $item[0]=="") 
		{alertWindowMsg($lang['wog_act_syn_error2']);} 
		else
		{
			$items=split(",",$item[0]);
			for($a=0;$a<count($_POST["syn"]);$a++) 
			{
				$syn_debug++;
				$items=$wog_item_tool->item_out($user_id,$syn[$a],1,$items);
			}
			if($syn_debug!=count($_POST["syn"])){alertWindowMsg($lang['wog_act_syn_error3']);} 
			$chang_d_type=$a_id;
			switch($_POST["syn_way"]) 
			{
				case "1":##########normal synthetic########## 
					$syn_tatal=0; 
					$sql="select sum(d_money) as id,sum(d_lv) as id2 from wog_df where d_id in (".implode(',',$_POST["syn"]).")";
					$item_money=$DB_site->query_first($sql);
//					if(rand(1,500) > 1)
//					{
						$item_money[0]=$item_money[0]+(rand(-80,80)*$item_money[1]);
						$sql="select d_id,d_name from wog_df where d_money<".$item_money[0]." and d_dbst=0 ORDER BY d_money desc limit 1";
						$new_arm=$DB_site->query_first($sql);
/*					}else
//					{
						$item_money[0]=$item_money[0]+(rand(1000,1500)*$item_money[1]);
						$sql="select d_id,d_name from wog_df where d_money<".$item_money[0]." and d_lv > 0 and d_lv <= ".(($item_money[1]/$syn_debug)+1)." ORDER BY RAND() limit 1";
						$new_arm=$DB_site->query_first($sql);
					}*/
				break;

				case "2":##########random synthetic########## 
					$syn_num=0;
					for($a=0;$a<count($_POST["syn"]);$a++)
					{$syn_num+=$_POST["syn"][$a];} 
					$get_type=$DB_site->query_first("select d_type,d_lv from wog_df where d_id=".$_POST["syn"][0].""); 
					$syn_id=floor(($syn_num/3)*1.1); 
					$sql="select d_id,d_name from wog_df where d_id<".$syn_id." and d_dbst=0 and d_type=".$get_type[0]." and d_lv <= ".$get_type[1]." ORDER BY RAND() LIMIT 1";
					$new_arm=$DB_site->query_first($sql); 
				break;

/*
				case "3":##########special synthetic########## 
					if(count($_POST["syn"])>5){alertWindowMsg($lang['wog_act_syn_error4']);} 
					for($ch=0;$ch<5;$ch++) 
					{if(!$_POST["syn"][$ch] || empty($_POST["syn"])){$_POST["syn"][$ch]=0;}} 
					$new_arm=$DB_site->query_first("select a.syn_result,b.d_name from wog_syn a,wog_df b where a.syn_ele1=".$_POST["syn"][0]." and a.syn_ele2=".$_POST["syn"][1]." and a.syn_ele3=".$_POST["syn"][2]." and a.syn_ele4=".$_POST["syn"][3]." and a.syn_ele5=".$_POST["syn"][4]." and b.d_id=a.syn_result"); 
				break;
*/
				default:##########error########## 
					alertWindowMsg($lang['wog_act_syn_error5']); 
				break;
			}
			if(rand(1,4)==1)
			{
				$DB_site->query("update wog_item set ".$chang_d_type."='".implode(',',$items)."' where p_id=".$user_id." "); 
				showscript("parent.syn_end('no',3)"); 
			}elseif($new_arm[0]) 
			{
				$p=$DB_site->query_first("select p_bag from wog_player where p_id=".$user_id.""); 
				check_type($new_arm[0]);
				if($a_id==$chang_d_type)
				{
					if($a_id=="d_item_id")
					{
						$bag=$wog_arry["item_limit"]+$p["p_bag"];
					}else
					{
						$bag=$wog_arry["item_limit"];
					}
					if((count($items)) > $bag)
					{
						showscript("parent.syn_end('no',4)"); 
						unset($temp_pack); 
					}
					$items=$wog_item_tool->item_in($items,$new_arm[0],1);
				}else
				{
					$new_blank=$DB_site->query_first("select ".$a_id." from wog_item where p_id=".$user_id.""); 
					$temp_pack=array();
					if(!empty($new_blank[0]))
					{
						$temp_pack=split(",",$new_blank[0]);
					}
					$temp_pack=$wog_item_tool->item_in($temp_pack,$new_arm[0],1);
					if($a_id=="d_item_id")
					{
						$bag=$wog_arry["item_limit"]+$p["p_bag"];
					}else
					{
						$bag=$wog_arry["item_limit"];
					}
					if((count($temp_pack)) > $bag)
					{
						showscript("parent.syn_end('no',4)"); 
						unset($temp_pack); 
					}
					$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_pack)."' where p_id=".$user_id." "); 
				}
				$DB_site->query("update wog_item set ".$chang_d_type."='".implode(',',$items)."' where p_id=".$user_id." "); 
				showscript("parent.syn_end('$new_arm[1]',1)"); 
			}else
			{
				$DB_site->query("update wog_item set ".$chang_d_type."='".implode(',',$items)."' where p_id=".$user_id." "); 
				showscript("parent.syn_end('no',2)"); 
			}
		}
	}

	function syn_list($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang;
		if(empty($_POST["type"]) || !is_numeric($_POST["type"]))
		{
			$_POST["type"]="0";
		}
		if(empty($_POST["page"]) || !is_numeric($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$d_type=$_POST["type"];
		if($d_type=="5"){$d_type="5,6";}
		$syn_total=$DB_site->query_first("select count(a.syn_id) as syn_id  from wog_syn a,wog_df c where a.syn_result=c.d_id and c.d_type in (".$d_type.") order by syn_id ");
		$spage=((int)$_POST["page"]*8)-8;
		$temp_s="";
		$syn=$DB_site->query("select c.d_name,c.d_at,c.d_mat,c.d_df,c.d_mdf,c.d_agl,c.d_mstr,c.d_magl,c.d_msmart,a.syn_id,d.ch_name,c.d_s,c.ch_pro,c.d_send  from wog_syn a,wog_df c left join wog_character d on d.ch_id=c.ch_id where a.syn_result=c.d_id and c.d_type in (".$d_type.")  LIMIT ".$spage.",8 ");
		while($syns=$DB_site->fetch_array($syn))
		{
			$temp_s.=";".$syns[0].",".$syns[1].",".$syns[2].",".$syns[3].",".$syns[4].",".$syns[5].",".$syns[6].",".$syns[7].",".$syns[8].",".$syns[9].",".$syns[10].",".$syns[11].",".$syns[12].",".$syns[13];
		}
		$DB_site->free_result($syn);
		unset($syns);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.syn_view_special($syn_total[0],".$_POST["page"].",'$temp_s',".$_POST["type"].")");
		unset($temp_s);
		unset($syn_total);
	}

	function syn_detail($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang;
		if(empty($_POST["syn_id"])){alertWindowMsg($lang['wog_act_syn_error6']);}
		$syn_item=$DB_site->query_first("select syn_ele1,syn_ele2,syn_ele3,syn_ele4,syn_ele5,syn_result from wog_syn where syn_id=".$_POST["syn_id"]);
		if(!$syn_item){alertWindowMsg($lang['wog_act_syn_error6']);}
		$syn=$DB_site->query("select d_name from wog_df where d_id in (".$syn_item["syn_ele1"].",".$syn_item["syn_ele2"].",".$syn_item["syn_ele3"].",".$syn_item["syn_ele4"].",".$syn_item["syn_ele5"].") ");
		$temp_s="";
		while($syns=$DB_site->fetch_array($syn))
		{
			$temp_s.=",".$syns[0];
		}
		$DB_site->free_result($syn);
		unset($syns);
		unset($syn_item);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		$syn_item2=$DB_site->query_first("select b.d_name from wog_syn a,wog_df b where a.syn_id=".$_POST["syn_id"]." and b.d_id=a.syn_result ");
		showscript("parent.syn_detail('$temp_s',".$_POST["syn_id"].",'".$syn_item2[0]."')");
		unset($syn_item2);
		unset($temp_s);
	}

	function syn_special($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_arry,$syn_debug,$syn_item,$wog_item_tool;
		if(empty($_POST["syn_id"])){alertWindowMsg($lang['wog_act_syn_error6']);}
		$p=$DB_site->query_first("select a.p_money,a.p_bag from wog_player a where a.p_id=".$user_id);
		if($p[0]<2000){alertWindowMsg($lang['wog_act_syn_error8']);}
		$syn_item=$DB_site->query_first("select a.syn_ele1,a.syn_ele2,a.syn_ele3,a.syn_ele4,a.syn_ele5,a.syn_result,b.d_name from wog_syn a left join wog_df b on b.d_id=a.syn_result where a.syn_id=".$_POST["syn_id"]." ");
		if(!$syn_item){alertWindowMsg($lang['wog_act_syn_error6']);}

		$syn_debug2=0;
		for($iii=0;$iii<5;$iii++)
		{
			if($syn_item[$iii] > 0)
			{
				$syn_debug2++;
			}
		}

		$syn=$DB_site->query("select DISTINCT d_type from wog_df where d_id in (".$syn_item["syn_ele1"].",".$syn_item["syn_ele2"].",".$syn_item["syn_ele3"].",".$syn_item["syn_ele4"].",".$syn_item["syn_ele5"].") ");
		$temp_s="";
		$temp_ss=array();
		while($syns=$DB_site->fetch_array($syn))
		{
			$temp_ss[]=type_name($syns["d_type"]);
		}
		$DB_site->free_result($syn);
		unset($syns);
		$syn_debug=0;
		$syn_item2=$DB_site->query_first("select ".implode(',',$temp_ss)." from wog_item where p_id=".$user_id);
		if($syn_item2)
		{
			for($i=0;$i<count($temp_ss);$i++)
			{
				$items=split(",",$syn_item2[$i]);
				if($items[0]=="N/A" || $items[0]=="") 
				{alertWindowMsg($lang['wog_act_syn_error7']);} 
				$a_id=$temp_ss[$i];

				for($ii=0;$ii<5;$ii++)
				{
					if($syn_item[$ii]>0)
					{
						$items=$wog_item_tool->item_syn_special_out($user_id,$ii,1,$items);
					}
				}
				$syn_item2[$i]=implode(',',$items);
			}
		}else
		{
			alertWindowMsg($lang['wog_act_syn_error5']);
		}
		if($syn_debug!=$syn_debug2){alertWindowMsg($lang['wog_act_syn_error7']);}
		$temp_sql="";
		for($i=0;$i<count($temp_ss);$i++)
		{
			if(strlen($syn_item2[$i]) > 0)
			{
				$temp_sql.=",".$temp_ss[$i]."='".$syn_item2[$i]."'";
			}else
			{
				$temp_sql.=",".$temp_ss[$i]."=''";
			}
		}
		$temp_sql=substr($temp_sql,1,strlen($temp_sql));
		unset($syn_item2);
		if(rand(1,25)==1)
		{
			$DB_site->query("update wog_item set ".$temp_sql." where p_id=".$user_id." ");
			showscript("parent.syn_end('no',3)"); 
		}else
		{
			$DB_site->query("update wog_player set p_money=p_money-2000 where p_id=".$user_id." ");
			$DB_site->query("update wog_item set ".$temp_sql." where p_id=".$user_id." ");
			check_type($syn_item["syn_result"]);
			if($a_id=="d_item_id")
			{
				$bag=$wog_arry["item_limit"]+$p["p_bag"];
			}else
			{
				$bag=$wog_arry["item_limit"];
			}
			$new_blank=$DB_site->query_first("select ".$a_id." from wog_item where p_id=".$user_id.""); 
			$temp_pack=array();
			if(!empty($new_blank[0]))
			{
				$temp_pack=split(",",$new_blank[0]);
			}
			$temp_pack=$wog_item_tool->item_in($temp_pack,$syn_item["syn_result"],1);
			if((count($temp_pack)+1) > $bag)
			{
				showscript("parent.syn_end('no',4)"); 
				unset($temp_pack); 
			}
			$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_pack)."' where p_id=".$user_id." "); 
			showscript("parent.syn_end('".$syn_item["d_name"]."',1)"); 
		}
		unset($syn_item);
	}
}
?>