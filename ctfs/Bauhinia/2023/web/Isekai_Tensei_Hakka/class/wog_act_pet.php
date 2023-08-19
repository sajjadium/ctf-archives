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

class wog_act_pet{
	var $f_count=0;
	var	$win=0;
	var	$lost=0;

	function pet_fight($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		$money=(int)$_POST["pay_id"];
		if($money<500 ||  $money>2000 || !is_numeric($money) )
		{
			alertWindowMsg($lang['wog_act_errmoney']);
		}
		$p_money=$DB_site->query_first("select p_money from wog_player where p_id=".$user_id );
		if($p_money)
		{
			if($p_money["p_money"]<$money)
			{
				alertWindowMsg($lang['wog_act_nomoney']);
			}
		}else
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$p=$DB_site->query_first("select pe_id,pe_name,pe_mname,pe_at,pe_mt,pe_def,pe_fi,pe_type,pe_b_old,pe_f_dateline from wog_pet where pe_p_id=".$user_id." and pe_st=0");
		if($p)
		{
			$check_time=time()-$p["pe_f_dateline"];
			if($check_time < $wog_arry["pet_f_time"])
			{
				alertWindowMsg(sprintf($lang['wog_act_pet_gofight'],round(($wog_arry["pet_f_time"]-$check_time)/60)));
			}
			switch ($_POST["temp_id2"])
			{
				case "1":
					if($p["pe_b_old"] > 3)
					{
						alertWindowMsg($lang['wog_act_pet_errage']);
					}
					$p_hp=200;
					$m_hp=200;
					$sold="0";
					$lold="3";
				break;
				case "2":
					if($p["pe_b_old"] > 7 || $p["pe_b_old"] < 4 )
					{
						alertWindowMsg($lang['wog_act_pet_errage']);
					}
					$p_hp=400;
					$m_hp=400;
					$sold="4";
					$lold="7";
				break;
				case "3":
					if($p["pe_b_old"] < 8 || $p["pe_b_old"] > 12 )
					{
						alertWindowMsg($lang['wog_act_pet_errage']);
					}
					$p_hp=800;
					$m_hp=800;
					$sold="8";
					$lold="12";
				break;
				case "4":
					if($p["pe_b_old"] < 13 || $p["pe_b_old"] > 18 )
					{
						alertWindowMsg($lang['wog_act_pet_errage']);
					}
					$p_hp=800;
					$m_hp=800;
					$sold="13";
					$lold="18";
				break;
				default:
						alertWindowMsg($lang['wog_act_pet_noselect']);
				break;
			}
			$m=$DB_site->query_first("select pe_id,pe_name,pe_mname,pe_at,pe_mt,pe_def,pe_fi,pe_type from wog_pet where pe_st=0 and pe_p_id<>".$user_id." and pe_b_old between $sold and $lold  ORDER BY RAND() LIMIT 1");
			if($m)
			{
				$p["pe_hp"]=$p_hp;
				$m["pe_hp"]=$m_hp;
				echo charset();
				echo "<script language=JavaScript >\n";
				echo "parent.pet_fview('$p[pe_name],$p[pe_mname],$p[pe_at],$p[pe_mt],$p[pe_def],$p[pe_fi],$p[pe_type],$p[pe_hp]','$m[pe_name],$m[pe_mname],$m[pe_at],$m[pe_mt],$m[pe_def],$m[pe_fi],$m[pe_type],$m[pe_hp]')\n";
				$this->win=0;
				$this->lost=0;
				$this->f_count=$wog_arry["f_count"];
				$this->fight_count($p,$m);
				if($this->win > $this->lost)
				{
					$DB_site->query("update wog_player set p_money=p_money+".($money*1.5)." where p_id=".$user_id);
					$DB_site->query("update wog_pet set pe_hu=pe_hu+".rand(5,10).",pe_he=pe_he-".rand(4,6).",pe_dateline=".time().",pe_f_dateline=".time()." where pe_id=".$p["pe_id"]);
				}else
				{
					$DB_site->query("update wog_player set p_money=p_money-".$money." where p_id=".$user_id);
					$DB_site->query("update wog_pet set pe_hu=pe_hu+".rand(8,15).",pe_he=pe_he-".rand(8,15).",pe_dateline=".time().",pe_f_dateline=".time()." where pe_id=".$p["pe_id"]);
				}
				echo "</script>";
			}else
			{
				alertWindowMsg($lang['wog_act_pet_nopet']);
			}
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
	}

	function pet_leave($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		showscript("parent.job_end(18)");
	}

	function pet_sale($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		$money=$_POST["temp_id"];
		if(empty($money) || (int)$money <=0 || !is_numeric($money))
		{
			alertWindowMsg($lang['wog_act_nomoney']);
		}
		$sale_time=3600*24*10;
		$DB_site->query("update wog_pet set pe_money=".$money.",pe_st=1,pe_s_dateline=".(time()+$sale_time)." where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]);
		showscript("parent.job_end(9)");
	}

	function pet_chg_st($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet'].$_POST["pay_id"]."555");
		}
		if($_POST["temp_id"]=="0")
		{
			$p=$DB_site->query_first("select pe_id from wog_pet where pe_p_id=".$user_id." and pe_st=0");
			if($p)
			{
				alertWindowMsg($lang['wog_act_pet_noget']);
			}
		}
		$DB_site->query("update wog_pet set pe_st=".$_POST["temp_id"]." where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		showscript("parent.job_end(3)");
	}

	function pet_rename($user_id)
	{
		global $DB_site,$_POST,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_noname']);
		}
		$DB_site->query("update wog_pet set pe_name='".trim($_POST["temp_id"])."' where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		$_POST["temp_id"]=$_POST["pay_id"];
		$this->pet_index($user_id);
	}

	function pet_eat($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_noselect']);
		}
		$p=$DB_site->query_first("select pe_fu,pe_dateline from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		if($p)
		{
			if((time()-$p["pe_dateline"]) < $wog_arry["pet_ac_time"])
			{
				alertWindowMsg($wog_arry["pet_ac_time"].$lang['wog_act_pet_noeat']);
			}
			if($p["pe_fu"] >= 100)
			{
				alertWindowMsg($lang['wog_act_pet_eatmax']);
			}
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		$at="+0";$mt="+0";$def="+0";$fi="+0";
		switch ($_POST["temp_id"])
		{
			case "1":
				$at="+1";
			break;
			case "2":
				$mt="+1";
			break;
			case "3":
				$def="+1";
			break;
			case "4":
				$fi="+1";
			break;
		}
		$hu=rand(5,20);
		$he=rand(2,6);
		$fu=rand(10,20);
		$DB_site->query("update wog_pet set pe_at=pe_at".$at.",pe_mt=pe_mt".$mt.",pe_def=pe_def".$def.",pe_fi=pe_fi".$fi.",pe_hu=pe_hu-".$hu.",pe_he=pe_he+".$he.",pe_fu=pe_fu+".$fu.",pe_dateline=".time()." where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		$DB_site->query("update wog_player set p_money=p_money-".$wog_arry["pet_eat_money"]." where p_id=".$user_id);
		if($p)
		{
			showscript("parent.pet_detail('$at','$mt','$def','-$hu','+$fu','+$he','$fi');");
	//		pet_index($user_id);
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		unset($p);
	}
	
	function pet_ac($user_id)
	{
		global $DB_site,$_POST,$wog_arry,$lang;
		if(!isset($_POST["pay_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		if(empty($_POST["temp_id"]))
		{
			alertWindowMsg($lang['wog_act_pet_noselect']);
		}
		$p=$DB_site->query_first("select pe_hu,pe_he,pe_dateline from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		if($p)
		{
			if((time()-$p["pe_dateline"]) < $wog_arry["pet_ac_time"])
			{
				alertWindowMsg($wog_arry["pet_ac_time"].$lang['wog_act_pet_noac']);
			}
			if($p["pe_hu"] >= 100)
			{
				alertWindowMsg($lang['wog_act_pet_humax']);
			}
			if($p["pe_hu"] >= 80 && $p["pe_hu"] < 90)
			{
				if(rand(1,20) <= 1)
				{
					$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]);
					showscript("parent.job_end(16)");
				}
			}
			if($p["pe_hu"] >= 90)
			{
				if(rand(1,10) <= 1)
				{
					$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]);
					showscript("parent.job_end(16)");
				}
			}
			$leave=90-$p["pe_he"];
			if(rand(1,100) < (90-$p["pe_he"]))
			{
				$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]);
				showscript("parent.job_end(17)");
			}
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		$at="+0";$mt="+0";$def="+0";$fi="+0";$fu="+0";
		switch ($_POST["temp_id"])
		{
			case "1":
				$at="+3";$mt="-1";$def="-1";
			break;
			case "2":
				$at="-1";$mt="+3";$fi="-1";
			break;
			case "3":
				$at="-1";$mt="-1";$def="+3";
			break;
			case "4":
				$fi="+2";$def="-2";
			break;
		}
		$hu=rand(5,9);
		$he=rand(0,3);
		$DB_site->query("update wog_pet set pe_at=pe_at".$at.",pe_mt=pe_mt".$mt.",pe_def=pe_def".$def.",pe_fi=pe_fi".$fi.",pe_hu=pe_hu+".$hu.",pe_he=pe_he-".$he.",pe_dateline=".time()." where pe_p_id=".$user_id." and pe_id=".$_POST["pay_id"]." ");
		if($p)
		{
			showscript("parent.pet_detail('$at','$mt','$def','+$hu','$fu','-$he','$fi')");
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		unset($p);
	}	

	function pet_index($user_id)
	{
		global $DB_site,$wog_arry,$lang,$_POST;
		if(!empty($_POST["temp_id"]) && is_numeric($_POST["temp_id"]))
		{
			$sql=" and pe_id=".$_POST["temp_id"];
		}else
		{
			$sql="";
		}
		$p=$DB_site->query_first("select * from wog_pet where pe_p_id=".$user_id." ".$sql." and pe_st in (0,2) LIMIT 1");
		if($p)
		{
			$old=round((time()-$p[pe_b_dateline])/$wog_arry["pet_age"]);
			if($old >= 5 && $old < 7 && rand(1,95) <= 1)
			{
				$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_st=0");
				alertWindowMsg($lang['wog_act_pet_die']);
			}
			if($old >= 7 && $old < 12 && rand(1,80) <= 1)
			{
				$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_st=0");
				alertWindowMsg($lang['wog_act_pet_die']);
			}
			if($old >= 12 && $old < 18 && rand(1,70) <= 1)
			{
				$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_st=0");
				alertWindowMsg($lang['wog_act_pet_die']);
			}
			if($old >= 18 && rand(1,30) <= 1)
			{
				$DB_site->query("delete from wog_pet where pe_p_id=".$user_id." and pe_st=0");
				alertWindowMsg($lang['wog_act_pet_die']);
			}
			$DB_site->query("update wog_pet set pe_b_old=".$old." where pe_id=".$p["pe_id"]." ");

			$pe_list=$DB_site->query("select pe_name,pe_id from wog_pet where pe_p_id=".$user_id." and pe_st in (0,2) ");
			$temp_s="";
			while($pe_lists=$DB_site->fetch_array($pe_list))
			{
				$temp_s.=";".$pe_lists[0].",".$pe_lists[1];
			}
			$DB_site->free_result($pe_list);
			unset($pe_lists);
			showscript("parent.pet_index('$p[pe_name]','$p[pe_mname]','$p[pe_id]','$p[pe_at],$p[pe_mt],$p[pe_def],$p[pe_fu],$p[pe_hu],$p[pe_type],$old,$p[pe_he],$p[pe_fi],$p[pe_st]','$temp_s')");
		}else
		{
			alertWindowMsg($lang['wog_act_pet_nopet']);
		}
		unset($p);
	}

	function fight_count($p,$m)
	{
		global $_POST;
		$sum=0;
		$fight_type=0;
		$dmg=0;
		while($p["pe_hp"]!=0 || $m["pe_hp"]!=0)
		{
			if(rand(1,3)<3)
			{
				$fight_type=rand(1,3);
				if($fight_type==1)
				{
					$dmg=$this->dmg_c($p["pe_at"],$m["pe_def"],$fight_type);
					$m["pe_hp"]=$m["pe_hp"]-$dmg;
				}elseif($fight_type==2)
				{
					$dmg=$this->dmg_c($p["pe_mt"],$m["pe_def"],$fight_type);
					$m["pe_hp"]=$m["pe_hp"]-$dmg;
				}elseif($fight_type==3)
				{
					$dmg=$this->dmg_c(($p["pe_at"]+$p["pe_mt"])*1.5,$m["pe_def"],$fight_type);
					$m["pe_hp"]=$m["pe_hp"]-$dmg;
				}
				if($_POST["a_mode"]=="2")
				{
					echo "parent.pet_pact('$dmg','$fight_type');\n";
				}
			}else
			{
				if($_POST["a_mode"]=="2")
				{
					echo "parent.pet_miss_date('$p[pe_name]-$p[pe_mname]',".rand(0,3).");\n";
				}
			}
			if($m["pe_hp"]<=0)
			{
				$this->win=1;
				$this->lost=0;
				echo "parent.pet_end_date('$p[pe_name]-$p[pe_mname]','1');\n";
				break;
			}
			if(rand(1,3)<3)
			{
				$fight_type=rand(1,3);
				if($fight_type==1)
				{
					$dmg=$this->dmg_c($m["pe_at"],$p["pe_def"],$fight_type);
					$p["pe_hp"]=$p["pe_hp"]-$dmg;
				}elseif($fight_type==2)
				{
					$dmg=$this->dmg_c($m["pe_mt"],$p["pe_def"],$fight_type);
					$p["pe_hp"]=$p["pe_hp"]-$dmg;
				}elseif($fight_type==3)
				{
					$dmg=$this->dmg_c(($m["pe_at"]+$m["pe_mt"])*1.5,$p["pe_def"],$fight_type);
					$p["pe_hp"]=$p["pe_hp"]-$dmg;
				}
				if($_POST["a_mode"]=="2")
				{
					echo "parent.pet_mact('$dmg','$fight_type');\n";
				}
			}else
			{
				if($_POST["a_mode"]=="2")
				{
					echo "parent.pet_miss_date('$m[pe_name]-$m[pe_mname]',".rand(0,3).");\n";
				}
			}
			if($p["pe_hp"]<=0)
			{
				$this->win=0;
				$this->lost=1;
				echo "parent.pet_end_date('$p[pe_name]-$p[pe_mname]','0');\n";
				break;
			}
			$sum++;
			if($sum>=$this->f_count)
			{
				echo "parent.pet_end_date('$p[pe_name]-$p[pe_mname] ".sprint($lang['wog_fight_over_time'],$this->f_count)." ','0');\n";
				$this->win=0;
				$this->lost=1;
				break;
			}
		}
	}
	function dmg_c($f,$d)
	{
		global $_POST;
		$dmg=round(($f-$d)*(0.65*rand(1,3)));
		if($dmg<0)
		{
			$dmg=0;
		}
		return $dmg;
	}
}
?>