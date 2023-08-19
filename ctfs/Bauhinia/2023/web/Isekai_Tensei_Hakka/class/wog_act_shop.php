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

class wog_act_shop{
	function shop($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang;
		check_type($_POST["temp_id"],1);
		$sql="select p_agl,p_lv,p_str,p_smart,p_life,ch_id,p_money,".$a_id." 
		from wog_player where  p_id=".$user_id." 
		";
		$p=$DB_site->query_first($sql);
		if(empty($p))
		{
			alertWindowMsg($lang['wog_act_relogin']);
		}

		switch($_POST["temp_id2"])
		{
			case "1":
				$dlv=1;
			break;
			case "2":
				$dlv=2;
			break;
			case "3":
				$dlv=3;
			break;
			case "4":
				$dlv=4;
			break;
			case "5":
				$dlv=5;
			break;
			case "6":
				$dlv=6;
			break;
			case "7":
				$dlv=7;
			break;
			default:
				$dlv=1;
			break;
		}

		$temp_where="((a.d_mstr >= $slv or a.d_msmart >= $slv or a.d_magl >= $slv) and (a.d_mstr <= $hlv and a.d_msmart <= $hlv and a.d_magl <= $hlv)) and a.d_msmart<=".$p[p_smart]." and a.d_magl<=".$p[p_agl]." and a.d_mstr<=".$p[p_str]." ";
		$temp_where=" a.d_lv=$dlv";

		$df_total=$DB_site->query_first("select count(a.d_id) as d_id from wog_df a where  d_type in (".$_POST["temp_id"].") and ".$temp_where." and a.d_dbst=0");
		if(empty($_POST["page"]))
		{
			$_POST["page"]="1";
		}
		$spage=((int)$_POST["page"]*8)-8;

		$sql="select a.d_id,a.d_df,a.d_mdf,a.d_agl,a.d_money,a.d_name,a.d_at,a.d_mat,a.d_mstr,a.d_magl,a.d_msmart,b.ch_name
			from wog_df a left join wog_character b on b.ch_id=a.ch_id
			where  a.d_type in (".$_POST["temp_id"].") and ".$temp_where." and a.d_dbst=0 LIMIT ".$spage.",8 ";

		$pack=$DB_site->query($sql);
		$s="";
		while($packs=$DB_site->fetch_array($pack))
		{
			if($packs[ch_name]==null){$packs[ch_name]="";}
			$s=$s.";".$packs[d_id].",".$packs[d_df].",".$packs[d_mdf].",".$packs[d_agl].",".$packs[d_money].",".$packs[d_name].",".$packs[d_at].",".$packs[d_mat].",".$packs[d_mstr].",".$packs[d_magl].",".$packs[d_msmart].",".$packs[ch_name];
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($pack);

		$packs=$DB_site->query_first("select d_df,d_mdf,d_agl,d_name,d_at,d_mat from wog_df where d_id=$p[7]");
		$ss=$packs[d_df].",".$packs[d_mdf].",".$packs[d_agl].",".$packs[d_name].",".$packs[d_at].",".$packs[d_mat].",".$p[p_money];
		unset($packs);
		unset($temp_where);
		unset($temp);
//		echo "<script language='JavaScript' src='http://www.acer.net/back/ming/wog_shop_cache_".$_POST["temp_id"]."_".$_POST["temp_id2"].".js'></script>";
//		showscript("parent.shop_home_view(s,'".$_POST["act"]."','".$_POST["temp_id"]."','".$ss."','".$_POST["temp_id2"]."')");
		showscript("parent.shop_home_view('$s','".$_POST["act"]."','".$_POST["temp_id"]."','".$ss."','".$_POST["temp_id2"]."',".$df_total[0].",".$_POST["page"].")");
		unset($s);
		unset($ss);
		unset($p);
		unset($a_id);
		unset($df_total);
	}

	function buy($user_id)
	{
		global $DB_site,$_POST,$a_id,$lang,$wog_arry,$wog_item_tool;
		$temp["money"]="d_money";
		$temp["table"]="wog_df";
		if(!isset($_POST["adds"]))
		{
			alertWindowMsg($lang['wog_act_buy_noitem']);
		}
		if($_POST["buy_num"] > 9)
		{
			alertWindowMsg($lang['wog_act_buy_errornum']);
		}
		check_type($_POST["temp_id"],1);
		$sql="select ".$a_id." from wog_item where p_id=".$user_id." ";
		$pack=$DB_site->query_first($sql);
		$pack[0]=trim($pack[0]);
		$temp_pack=array();
		if(!empty($pack[0]))
		{
			$temp_pack=split(",",$pack[0]);
		}
		$buy_num=$_POST["buy_num"];
		
		$check_tiem=$DB_site->query_first("select d_id from ".$temp["table"]." where d_id=".$_POST["adds"]."  and d_dbst=1");
		if($check_tiem)
		{
			alertWindowMsg($lang['wog_act_errwork']);
			unset($check_tiem);
		}
		$must_price=$DB_site->query_first("select ".$temp["money"]." from ".$temp["table"]." where d_id=".$_POST["adds"]." ");
		$have_price=$DB_site->query_first("select p_money,p_bag from wog_player where p_id=".$user_id."");
		if($a_id=="d_item_id")
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$_POST["adds"],$buy_num);
			$must_price[0]=$must_price[0]*$buy_num;
			$bag=$wog_arry["item_limit"]+$have_price["p_bag"];
		}else
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$_POST["adds"]);
			$bag=$wog_arry["item_limit"];
		}
		if($must_price[0]>$have_price[0]){
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		if(count($temp_pack) > $bag)
		{
			alertWindowMsg(sprintf($lang['wog_act_buy_tenitem'],$wog_arry["item_limit"]));
			unset($temp_pack);
		}

		$DB_site->query("update wog_player set p_money=p_money-".$must_price[0]." where p_id=".$user_id."");
		if($pack)
		{
			$pack[0]=implode(',', $temp_pack);
			$DB_site->query("update wog_item set ".$a_id."='".$pack[0]."' where p_id=".$user_id."");
		}else
		{
			$pack[0]=implode(',', $temp_pack);
			$DB_site->query("insert into wog_item(".$a_id.",p_id)values('".$pack[0]."',".$user_id.")");
		}
		unset($pack);
		unset($temp_add);
		unset($must_price);
		unset($have_price);
		unset($temp);
		unset($a_id);
		showscript("parent.job_end(6)");
	}
}

?>