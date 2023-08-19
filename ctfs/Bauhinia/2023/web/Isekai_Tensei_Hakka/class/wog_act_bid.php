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

class wog_act_bid{
	function bid($user_id)
	{
		global $DB_site,$_POST,$a_id,$temp_ss,$wog_arry,$lang,$wog_item_tool;
		$money=(int)$_POST["money"];
		$day=(int)$_POST["day"];
		if(empty($_POST["item_id"]))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		if(empty($day) || empty($money))
		{
			alertWindowMsg($lang['wog_act_bid_nodate']);
		}
		if($money<0 || $day<0 || !is_numeric($_POST["money"]) || !is_numeric($_POST["day"]) )
		{
			alertWindowMsg($lang['wog_act_bid_nodate']);
		}
		if($day>$wog_arry["sale_day"])
		{
			alertWindowMsg(sprintf($lang['wog_act_bid_limitday'],$wog_arry["sale_day"]));
		}
		$total=$DB_site->query_first("select count(s_id) as s_id from wog_sale where p_id=".$user_id." ");
		if($total[0]>=5)
		{
			alertWindowMsg($lang['wog_act_bid_limit_item']);
		}
		$sql="select d_send from wog_df where d_id=".$_POST["item_id"]." ";
		$pay=$DB_site->query_first($sql);
		if($pay[0]==1)
		{
			alertWindowMsg($lang['wog_act_arm_nosend']);
		}

		check_type($_POST["item_id"]);
		$temp_ss=$wog_item_tool->item_out($user_id,$_POST["item_id"]);
		$have_price=$DB_site->query_first("select p_money from wog_player where p_id=".$user_id." and p_lock=0");
		if($have_price)
		{
			if($have_price["p_money"]<$money*0.03)
			{
				alertWindowMsg(sprintf($lang['wog_act_bid_procedures'],$money*0.03));
			}
			$DB_site->query("update wog_player set p_money=p_money-".$money*0.03." where p_id=".$user_id." ");
		}else
		{
			alertWindowMsg($lang['wog_act_nologin']);
		}
		$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_ss)."' where p_id=".$user_id." ");
		$DB_site->query("insert wog_sale(p_id,d_id,s_money,dateline)values(".$user_id.",".$_POST["item_id"].",".$money.",".(time()+($day*24*60*60)).")");
		showscript("parent.arm_select()");
		unset($d_money);
		unset($pay);
		unset($s2);
		unset($a_id);
	}

	function sale_buy_item($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_arry,$wog_item_tool;
		$temp["money"]="d_money";
		$temp["table"]="wog_df";
		if(!isset($_POST["s_id"]))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		$pack=$DB_site->query_first("select b.d_type,b.d_id,a.p_id,a.s_money,b.d_name from wog_sale a,wog_df b where a.s_id=".$_POST["s_id"]." and a.d_id=b.d_id ");
		if(!$pack)
		{
			alertWindowMsg($lang['wog_act_bid_buyed']);
		}
		check_type($pack[0],1);
		$temp_add=$pack[1];
		$temp["user_id"]=$pack[2];
		$temp["d_name"]=$pack[4];
		$must_price=$pack[3];
		$sql="select ".$a_id." from wog_item where p_id=".$user_id."  ";
		$pack=$DB_site->query_first($sql);
		$pack[0]=trim($pack[0]);
		$temp_pack=array();
		if(!empty($pack[0]))
		{
			$temp_pack=split(",",$pack[0]);
		}

		if(empty($temp_add))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		$have_price=$DB_site->query_first("select p_money,p_name,p_lv,p_bag from wog_player where p_id=".$user_id);
		if($must_price>$have_price[0]){
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		if($have_price[2] < 15 )
		{
			alertWindowMsg(sprintf($lang['wog_act_cant_bid'],15));
		}

		if($a_id=="d_item_id")
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$temp_add,1);
			$bag=$wog_arry["item_limit"]+$have_price["p_bag"];
		}else
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$temp_add);
			$bag=$wog_arry["item_limit"];
		}
		if(count($temp_pack) > $bag)
		{
			alertWindowMsg($lang['wog_act_bid_full']);
			unset($temp_pack);
		}

		$DB_site->query("update wog_player set p_money=p_money-".$must_price." where p_id=".$user_id);
		$DB_site->query("update wog_player set p_money=p_money+".$must_price." where p_id=".$temp["user_id"]);
		$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$temp["user_id"].",'".sprintf($lang['wog_act_bid_message'],$temp["d_name"],$have_price["p_name"])."',".time().")");
		if($pack)
		{
			$pack[0]=implode(',', $temp_pack);
			$DB_site->query("update wog_item set ".$a_id."='".$pack[0]."' where p_id=".$user_id);
		}else
		{
			$pack[0]=implode(',', $temp_pack);
			$DB_site->query("insert into wog_item(".$a_id.",p_id)values('".$temp_add."',".$user_id.")");
		}
		$DB_site->query("delete from wog_sale where s_id=".$_POST["s_id"]);
		unset($pack);
		unset($temp_add);
		unset($must_price);
		unset($have_price);
		unset($temp);
		unset($a_id);
		showscript("parent.job_end(6)");
	}

	function sale_buy_pet($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(!isset($_POST["s_id"]))
		{
			alertWindowMsg($lang['wog_act_arm_noselect']);
		}
		$pack=$DB_site->query_first("select pe_money,pe_p_id,pe_name from wog_pet where pe_id=".$_POST["s_id"]." and pe_st=1 ");
		if(!$pack)
		{
			alertWindowMsg($lang['wog_act_bid_buyed']);
		}
		$temp["money"]=$pack["pe_money"];
		$temp["user_id"]=$pack["pe_p_id"];
		$temp["d_name"]=$pack["pe_name"];
		$sql="select count(pe_id) as num from wog_pet where pe_p_id=".$user_id." and pe_st in (0,2) ";
		$pack=$DB_site->query_first($sql);
		if($pack["num"]>2)
		{
			alertWindowMsg($lang['wog_act_bid_one']);
		}
		$have_price=$DB_site->query_first("select p_money,p_name from wog_player where p_id=".$user_id."");
		if($temp["money"]>$have_price[0]){
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$DB_site->query("update wog_player set p_money=p_money-".$temp["money"]." where p_id=".$user_id);
		$DB_site->query("update wog_player set p_money=p_money+".$temp["money"]." where p_id=".$temp["user_id"]);
		$DB_site->query("update wog_pet set pe_p_id=".$user_id.",pe_st=2,pe_he=0 where pe_id=".$_POST["s_id"]);
		$DB_site->query("insert into wog_message(p_id,title,dateline)values(".$temp["user_id"].",'您拍賣的 ".$temp["d_name"]." 被 ".$have_price["p_name"]." 買走',".time().")");
		unset($pack);
		unset($have_price);
		unset($temp);
		unset($a_id);
		showscript("parent.job_end(6)");
	}

	function bid_view()
	{
		global $DB_site,$_GET,$a_id,$wog_arry,$wog_item_tool;
		$ttime=time();
		$pack=$DB_site->query("select b.d_type,b.d_id,a.p_id from wog_sale a,wog_df b where a.dateline < ".$ttime." and a.d_id=b.d_id ");
		while($packs=$DB_site->fetch_array($pack))
		{
			check_type($packs[0],1);
			$sql="select ".$a_id." from wog_item where p_id=".$packs[2]."  ";
			$pack2=$DB_site->query_first($sql);
			$temp_pack=array();
			if(!empty($pack2[0]))
			{
				$temp_pack=split(",",$pack2[0]);
			}

			if($a_id=="d_item_id")
			{
				$temp_pack=$wog_item_tool->item_in($temp_pack,$packs["d_id"],1);
				$sql="select p_bag from wog_player where p_id=".$packs[2]."  ";
				$bag=$DB_site->query_first($sql);
				$bbag=$wog_arry["item_limit"]+$bag[0];
			}else
			{
				$temp_pack=$wog_item_tool->item_in($temp_pack,$packs["d_id"]);
				$bbag=$wog_arry["item_limit"];
			}
			if(count($temp_pack) < $bbag)
			{
				$DB_site->query("update wog_item set ".$a_id."='".implode(',',$temp_pack)."' where p_id=".$packs[2]."");
			}
			
		}
		$DB_site->free_result($pack);
		unset($temp_pack);
		unset($pack);
		unset($packs);
		unset($pack2);
		$DB_site->query("delete from wog_sale where dateline < ".$ttime." ");
		$DB_site->query("delete from wog_pet where pe_st=1 and pe_s_dateline < ".$ttime." ");
		if(empty($_GET["type"]) || !is_numeric($_GET["type"]))
		{
			$_GET["type"]="0";
		}
		$d_type=$_GET["type"];
		if($_GET["type"] < 6)
		{
			if($d_type=="5"){$d_type="5,6";}
			$sale_total=$DB_site->query_first("select count(a.s_id) as s_id from wog_sale a,wog_player b,wog_df c where a.p_id=b.p_id and a.d_id=c.d_id and c.d_type in (".$d_type.")");
		}else
		{
			$sale_total=$DB_site->query_first("select count(a.pe_id) as pe_id from wog_pet a,wog_player b where a.pe_p_id=b.p_id and a.pe_st=1");
		}
		if(empty($_GET["page"]) || !is_numeric($_GET["page"]))
		{
			$_GET["page"]="1";
		}
		$spage=((int)$_GET["page"]*8)-8;
		$temp_s="";
		if($_GET["type"] < 6)
		{
			$sale=$DB_site->query("select b.p_name,c.d_name,c.d_at,c.d_mat,c.d_df,c.d_mdf,c.d_agl,c.d_mstr,c.d_magl,c.d_msmart,c.d_money,a.s_id,a.s_money,a.dateline,d.ch_name from wog_sale a,wog_player b,wog_df c left join wog_character d on d.ch_id=c.ch_id where a.p_id=b.p_id and a.d_id=c.d_id and c.d_type in (".$d_type.") ORDER BY a.s_money,a.dateline LIMIT ".$spage.",8 ");
			while($sales=$DB_site->fetch_array($sale))
			{
				$temp_s.=";".$sales[0].",".$sales[1].",".$sales[2].",".$sales[3].",".$sales[4].",".$sales[5].",".$sales[6].",".$sales[7].",".$sales[8].",".$sales[9].",".$sales[10].",".$sales[11].",".$sales[12].",".$sales[13].",".$sales[14];
			}
		}else
		{
			$pet_age=3600*24*10;
			$sale=$DB_site->query("select b.p_name,a.pe_id,a.pe_name,a.pe_mname,a.pe_at,a.pe_mt,a.pe_def,a.pe_type,a.pe_b_dateline,a.pe_fi,a.pe_money,a.pe_s_dateline from wog_pet a,wog_player b where a.pe_p_id=b.p_id and a.pe_st=1 ORDER BY a.pe_money,a.pe_s_dateline desc LIMIT ".$spage.",8 ");
			while($sales=$DB_site->fetch_array($sale))
			{
				$temp_s.=";".$sales[0].",".$sales[1].",".$sales[2].",".$sales[3].",".$sales[4].",".$sales[5].",".$sales[6].",".$sales[7].",".round((time()-$sales[8])/$pet_age).",".$sales[9].",".$sales[10].",".$sales[11];
			}
		}
		$DB_site->free_result($sale);
		unset($sales);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		showscript("parent.sale_view($sale_total[0],".$_GET["page"].",'$temp_s',".$_GET["type"].")");
		unset($temp_s);
		unset($sale_total);
	}
}
?>