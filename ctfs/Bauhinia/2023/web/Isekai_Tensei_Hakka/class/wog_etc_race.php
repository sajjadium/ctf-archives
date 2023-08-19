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

class wog_etc_race{

	function race_view($userid)
	{
		global $DB_site;
		$race=$DB_site->query("select p_name,p_sat_name,p_id from wog_player ORDER BY RAND() LIMIT 8 ");
		$temp_s="";
		$temp_ss="";
		while($races=$DB_site->fetch_array($race))
		{
			$temp_s.=";".$races[0].",".$races[1].",".$races[2];
			$temp_ss.=",".$races[2];
		}
		$DB_site->free_result($race);
		unset($races);
		$temp_s=substr($temp_s,1,strlen($temp_s));
		$temp_ss=substr($temp_ss,1,strlen($temp_ss));
		$DB_site->query("delete from wog_race where p_id=".$userid."");
		$DB_site->query("insert into wog_race(p_id,r_str,dateline)values(".$userid.",'".$temp_ss."',".time().")");
		$p=$DB_site->query_first("select p_name,p_money from wog_player where p_id=".$userid."");
		showscript("parent.race_view('$temp_s','$p[p_name]','$p[p_money]')");
		unset($temp_s);
	}

	function race_end($userid)
	{
		global $DB_site,$_POST,$lang;
		$p=$DB_site->query_first("select a.p_money,a.p_name,b.r_str from wog_player a,wog_race b where a.p_id=".$userid." and a.p_id=b.p_id");
		$money=(int)trim(addslashes($_POST["money"]));
		if(!eregi("[0-9]",$money))
		{
		    alertWindowMsg($lang['wog_act_nomoney']);
			
		}
		if(!isset($_POST["yourchoose"]))
		{
		    alertWindowMsg($lang['wog_etc_race_nobird']);
			
		}
		if($p[0]<100 || $p[0]<$money || $money > 100000 || $money < 100)
		{
		    alertWindowMsg($lang['wog_act_nomoney']);
			
		}
//		$_POST["temp_id"]=
		$temp_id=split(",",$p[r_str]);
		$r_str=$p[r_str];
		$temp_count=count($temp_id);
		if($temp_count!=8)
		{
		    alertWindowMsg($lang['wog_etc_race_errorbird']);
		}
		$fff=0;
		$temp_tol="";
		$temp_name="";
		for ($intj=0;$intj<count($temp_id);$intj++)
		{
			if($temp_id[$intj]=="undefined" || !is_numeric($temp_id[$intj]))
			{
			    alertWindowMsg($lang['wog_etc_race_rerace']);
				
			}
			$temp_tol_num="";
			for ($i=0;$i<30;$i++)
			{
				$intnum=pack(c,rand(0,10)+48);
				$intnum1=$intnum1+$intnum*3;
				$temp_tol_num.=",".$intnum1;
			}
			$temp_tol_num=substr($temp_tol_num,1,strlen($temp_tol_num));
			if($intnum1 > $fff){$fff=$intnum1;$no=$temp_id[$intj];}
			$intnum1=0;
			$temp_tol.=";".$temp_tol_num;
		}
		$temp_tol=substr($temp_tol,1,strlen($temp_tol));
		$fff=$fff-15;
		$race=$DB_site->query("select p_name,p_id from wog_player where p_id in (".$r_str.")");
		$temp_s="";
		$i=0;
		while($races=$DB_site->fetch_array($race))
		{
			$i++;
			if($no==$races[1])
			{
				$winer=$races[0];
			}
			$temp_id=split(",",$r_str);
			$temp_s="";
			for($i=0;$i<count($temp_id);$i++)
			{
				if($temp_id[$i]==$races[1])
				{
					$temp_s.=",".$races[0];
				}else
				{
					$temp_s.=",".$temp_id[$i];
				}
			}
			$temp_s=substr($temp_s,1,strlen($temp_s));
			$r_str=$temp_s;
		}
		if($i!=8)
		{
		    alertWindowMsg($lang['wog_etc_race_errorbird']);
		}
		$DB_site->free_result($race);
		unset($races);
		if((int)$_POST["yourchoose"]==$no)
		{
			$DB_site->query("update wog_player set p_money=p_money+".($money*5)." where p_id=".$userid."");
			$message=sprintf($lang['wog_etc_race_win'],$p[p_name],($money*5));
		}else
		{
			$DB_site->query("update wog_player set p_money=p_money-".$money." where p_id=".$userid."");
			$message=$lang['wog_etc_race_lost'];
		}
		$DB_site->query("update wog_player set p_cho_win=p_cho_win+1 where p_id=".$no."");
		$DB_site->query("delete from wog_race where p_id=".$userid."");
		showscript("parent.race_end('$r_str','$temp_tol','$message','$fff','$winer')");
		unset($temp_s);
		unset($p);
	}
}
?>