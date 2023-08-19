<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/02/08
 URL : http://www.2233.idv.tw

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

class wog{
	var $f_count=0;
	var	$win=0;
	var	$temp_win=0;
	var	$lost=0;
	var	$temp_lost=0;
	var	$cp_m_hp=0;

//########## group ##########

	function fight_group_dms($p,$m,$d_s,$type) //屬性傷害比例function
	{
		$temp_d=0;
		if($type==0)
		{
			$temp_d=380+rand($p["p_str"]*0.02,$p["p_str"]*0.07);
		}elseif($type==1)
		{
			$smart=$p["p_smart"]-$m["p_smart"];
			if($smart<=0){$smart=1;}
			$temp_d=150+rand($p["p_smart"]*0.05,$p["p_smart"]*0.3);
		}
		$temp_d=$temp_d*($p["p_g_morale"]/100);
		$temp_d=$temp_d+($temp_d*((100-$m["p_g_morale"])/100));
		$temp_s=$m["p_s"]-$d_s;
		switch($temp_s)
		{
			case 1:
				$temp_s=1.4;
			break;
			case -5:
				$temp_s=1.4;
			break;
			case 0:
				$temp_s=0.6;
			break;
			default:
				$temp_s=1;
			break;
		}
		$temp_d=$temp_d*$temp_s;
		return round($temp_d);
	}
	function fight_group_exdms($p,$m) //城堡傷害比例
	{
		$temp_d=0;
		$smart=$p["p_smart"]-$m["p_smart"];
		if($smart<=0){$smart=1;}
		$temp_d=7+rand($p["p_smart"]*0.002,$p["p_smart"]*0.01);
		$temp_d=round($temp_d*($p["p_g_morale"]/100));
		echo "parent.group_exm2_act('$temp_d');\n";
		return $temp_d;
	}
	function fight_group_morale($p,$temp_d,$s)
	{
		$morale=($temp_d/$p[p_g_number])*$p["p_g_morale"];
		$morale=round($p["p_g_morale"]-$morale);
		if($s==0)
		{
			echo "parent.group_p_act('$temp_d','$morale','".($p[p_g_number]-$temp_d)."');\n";
		}elseif($s==1)
		{
			echo "parent.group_m_act('$temp_d','$morale','".($p[p_g_number]-$temp_d)."');\n";
		}elseif($s==2)
		{
			echo "parent.group_exm_act('$temp_d','$morale','".($p[p_g_number]-$temp_d)."');\n";
		}
		return $morale;
	}
	function fight_group($user_id,$p,$m,$de_hp,$de_s)
	{
		global $DB_site,$_POST;
		while($p[p_g_number]!=0 || $m[p_g_number]!=0 || $de_hp!=0)
		{
			//######### pact ##########(己方攻擊開始)
			$temp_d=$this->fight_group_dms($p,$m,$de_s,0);//傷害計算
			$m["p_g_morale"]=$this->fight_group_morale($m,$temp_d,0);//士氣計算
			$m[p_g_number]=$m[p_g_number]-$temp_d;
			if($m[p_g_number]<=0)//判斷是否戰勝
			{
				echo "parent.end_date('$p[p_name]','1','0',0,'$p[p_hp]');\n";
				$this->win=1;
				$this->lost=0;
				break;
			}
			//######### mact ##########(敵方攻擊開始)
			$temp_d=$this->fight_group_dms($m,$p,$de_s,0);//傷害計算
			$p["p_g_morale"]=$this->fight_group_morale($p,$temp_d,1);//士氣計算
			$p[p_g_number]=$p[p_g_number]-$temp_d;
			if($p[p_g_number]<=0)//判斷是否戰敗
			{
				echo "parent.end_date('$p[p_name]','0','0',0,'$p[p_hp]');\n";
				$this->win=0;
				$this->lost=1;
				break;
			}
			//######### exact ##########(城堡受到破壞)
			if(rand(1,5)==1)
			{
				$temp_d=$this->fight_group_exdms($p,$m);//傷害計算
				$de_hp=$de_hp-$temp_d;
				if($de_hp<=0)//判斷是否戰勝
				{
					echo "parent.end_date('$p[p_name]','1','0',0,'$p[p_hp]');\n";
					$this->win=1;
					$this->lost=0;
					break;
				}
			}
			//######### exact ##########(城堡攻擊開始)
			if(rand(1,3)==1)
			{
				$temp_d=$this->fight_group_dms($m,$p,$de_s,1);//傷害計算
				$p["p_g_morale"]=$this->fight_group_morale($p,$temp_d,2);//士氣計算
				$p[p_g_number]=$p[p_g_number]-$temp_d;
				if($p[p_g_number]<=0)//判斷是否戰敗
				{
					echo "parent.end_date('$p[p_name]','0','0',0,'$p[p_hp]');\n";
					$this->win=0;
					$this->lost=1;
					break;
				}
			}
			$sum++;
			if($sum>=$this->f_count)//判斷戰鬥是否超過回合數設定
			{
				echo "parent.end_date('$p[p_name] 戰鬥超過".$this->f_count."回合 ','0','$exp',0,'$p[p_hp]');\n";
				$this->win=0;
				$this->lost=1;
				break;
			}
		}
		$DB_site->query("update wog_player set p_g_number=".$p[p_g_number].",p_g_morale=".$p[p_g_morale].",p_act_time ='".time()."',p_online_time=".time()."  where p_id=".$user_id." ");
		$DB_site->query("update wog_player set p_g_number=".$m[p_g_number].",p_g_morale=".$m[p_g_morale]." where p_id=".$m[p_id]." ");
		$DB_site->query("update wog_group_area set g_a_hp=".$de_hp." where g_id=".$m["p_g_id"]." and g_a_type=".$de_s." ");
	}

	function fight_group_de($user_id,$p,$m,$de_hp,$de_s)
	{
		global $DB_site,$_POST;
		while($de_hp!=0)
		{
			//######### exact ##########(城堡受到破壞)
			$temp_d=$this->fight_group_exdms($p,$m);//傷害計算
			$de_hp=$de_hp-$temp_d;
			if($de_hp<=0)//判斷是否戰勝
			{
				echo "parent.end_date('$p[p_name]','1','0',0,'$p[p_hp]');\n";
				$this->win=1;
				$this->lost=0;
				break;
			}
			//######### exact ##########(城堡攻擊開始)
			$temp_d=$this->fight_group_dms($m,$p,$de_s,1);//傷害計算
			$p["p_g_morale"]=$this->fight_group_morale($p,$temp_d,2);//士氣計算
			$p[p_g_number]=$p[p_g_number]-$temp_d;
			if($p[p_g_number]<=0)//判斷是否戰敗
			{
				echo "parent.end_date('$p[p_name]','0','0',0,'$p[p_hp]');\n";
				$this->win=0;
				$this->lost=1;
				break;
			}
			$sum++;
			if($sum>=$this->f_count)//判斷戰鬥是否超過回合數設定
			{
				echo "parent.end_date('$p[p_name] 戰鬥超過".$this->f_count."回合 ','0','$exp',0,'$p[p_hp]');\n";
				$this->win=0;
				$this->lost=1;
				break;
			}
		}
		$DB_site->query("update wog_player set p_g_number=".$p[p_g_number].",p_g_morale=".$p[p_g_morale].",p_act_time ='".time()."',p_online_time=".time()."  where p_id=".$user_id." ");
		$DB_site->query("update wog_group_area set g_a_hp=".$de_hp." where g_id=".$m["p_g_id"]." and g_a_type=".$de_s." ");
	}

}
?>