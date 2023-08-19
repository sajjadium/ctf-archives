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
	var $f_hp=0.15;
	var	$win=0;
	var	$temp_win=0;
	var	$lost=0;
	var	$temp_lost=0;
	var	$cp_m_hp=0;
	var $petact=1;
	var $pe_def=0;
	var $money=0;
	var $p_place=0;
	var $skill_money_up=1;
	function fight($f_a,$f_lv,$d_d,$d_lv,$temp_s) //屬性傷害比例function
	{
		if($d_d == 0){$d_d=1;}
		if($f_a == 0){$f_a=1;}
		$temp_at=($f_a/$d_d);
		$temp_lv=$f_lv-$d_lv;
		if($temp_at < 0){$temp_at=1;}
		if($temp_lv < 0){$temp_lv=1;}
		$temp_d=(($f_a*$temp_at)-$d_d)*$temp_s;
		if($temp_d<=0){$temp_d=1;}
		$temp_rd=$temp_d/$f_a;
		$temp_d=$temp_d+($temp_rd*rand(1,$temp_lv));
		return round($temp_d);
	}

	function m_type($m_at,$m_mat)//判斷敵攻擊模式function
	{
		$temp_mtype=rand(1,10);
		$m_type=0;
		if(($m_at>=$m_mat) && ($temp_mtype <= 8))
		{
			$m_type=1;
		}elseif(($m_at<$m_mat) && ($temp_mtype <= 8))
		{
			$m_type=2;
		}else
		{
			if($m_type==0)
			{
				if($temp_mtype >=5 )
				{
					$m_type=1;
				}else
				{
					$m_type=2;
				}
			}
		}
		return $m_type;
	}

	function get_exp($m_hp,$m_hpmax,$m_at,$m_mat,$m_lv,$p_lv,$s)//get經驗直function
	{
		if($p_lv<=100)
		{
			$exp_at=rand($m_at,$m_mat)*1.3;
		}else
		{
			$exp_at=rand($m_at,$m_mat);
		}
		if($m_lv >= 450)
		{
			$exp_at=$exp_at*0.6;
		}
		$exp_at=$m_lv*$exp_at*($m_lv/$p_lv);
		$exp=$exp_at*($m_hp/$m_hpmax)*0.18;
		if($s==0)
		{
			$exp=$exp*($m_hp/$m_hpmax);
		}
		if($p_lv<=15)
		{
			$exp=$exp*2.5;
		}
		return round($exp);
	}

	function get_money($m_hp,$m_at,$m_mat,$m_lv)//get金錢function
	{
		$at_total=($m_at+$m_mat)/$m_lv;
		$at_total2=($m_hp/($m_at+$m_mat))*0.8;
		return rand(($m_lv/2.5),$m_lv)*(rand($at_total,$at_total2)*0.6);
	}

	function lv_up($user_id,$p,$money)//升級function
	{
		global $DB_site;
		$p_str=0;
		$p_agl=0;
		$p_smart=0;
		$p_life=0;
		$p_be=0;
		$p_au=0;
		$p_vit=0;
		$lv=$DB_site->query_first("select ch_str,ch_agl,ch_life,ch_vit,ch_smart,ch_au,ch_be from wog_character where ch_id=".$p[ch_id]."");
		while($p[p_exp]>$p[p_nextexp])
		{
			$p[p_lv]+=1;
			$p[p_exp]-=$p[p_nextexp];
			$temp_lv=($p[p_lv]/50)*250+1000;
			$p[p_nextexp]=round(($p[p_lv]+(($p[p_lv]/6)*1.25))*$temp_lv);
			$m=split(",",$lv[ch_str]);
			$p_str+=rand($m[0],$m[1]);
			$m=split(",",$lv[ch_agl]);
			$p_agl+=rand($m[0],$m[1]);
			$m=split(",",$lv[ch_life]);
			$p_life+=rand($m[0],$m[1]);
			$p[p_hpmax]=$p[p_hpmax]+(($p[p_life]+$p_life)*0.4);
			$m=split(",",$lv[ch_vit]);
			$p_vit+=rand($m[0],$m[1]);
			$m=split(",",$lv[ch_smart]);
			$p_smart+=rand($m[0],$m[1]);
			$m=split(",",$lv[ch_be]);
			$p_be+=rand($m[0],$m[1]);
			$m=split(",",$lv[ch_au]);
			$p_au+=rand($m[0],$m[1]);
		}
		echo ",\"parent.lv_up('$p_str','$p_agl','$p_smart','$p_life','$p_vit','$p_au','$p_be')\"";
		$DB_site->query("update wog_player set p_at=p_at+".$p_str.",p_df=p_df+".$p_vit.",p_mat=p_mat+".$p_smart."
		,p_mdf=p_mdf+".$p_be.",p_str=p_str+".$p_str.",p_smart=p_smart+".$p_smart.",p_agl=p_agl+".$p_agl."
		,p_life=p_life+".$p_life.",p_vit=p_vit+".$p_vit.",p_au=p_au+".$p_au.",p_be=p_be+".$p_be.",p_lv=".$p[p_lv].",p_exp=".$p[p_exp].",p_nextexp=".$p[p_nextexp].",p_hp=".$p[p_hp]."
		,p_hpmax=".$p[p_hpmax].",p_money=p_money+".$money.",p_win=p_win+".$this->temp_win.",p_lost=p_lost+".$this->temp_lost.",p_act_time ='".time()."',p_place=".$this->p_place."
		,p_online_time=".time().",d_item_id=".$p[d_item_id]." 
		 where p_id=".$user_id." ");
		 unset($lv);
	}
	function fight_p_dm($p,$m,$me_skill,$act_type,$ss,$temp_s,$support=0)//玩家攻擊function
	{
		global $_POST;
		$agll=($p[p_agl]*$me_skill["s_agl"])+($m[m_agl]*$me_skill["s_m_agl"]);
		$aglll=($p[p_agl]*$me_skill["s_agl"])/$agll;
		$temp_agl=($aglll*100)+$me_skill["s_r"];
//		$temp_agl=(((($p[p_agl]*$me_skill["s_agl"]))/(($p[p_agl]*$me_skill["s_agl"])+($m[m_agl]*$me_skill["s_m_agl"])))*100)+$me_skill["s_r"];
		$temp_r=rand(1,100);
		$s="";
		if($act_type=="1")
		{
			if($temp_agl<50){$temp_agl=50;}
			if($temp_agl < $temp_r)
			{
				$temp_d=0;
			}else
			{
				if((rand(1,100)+$me_skill["s_s"]) > 80)
				{
					$temp_d=$this->fight($p[p_at]*2*$me_skill["s_at"],$p[p_lv],$m[m_df]*$me_skill["s_m_df"],$m[m_lv],$temp_s);
					$s.="+".$p[p_sat_name];
				}else
				{
					$temp_d=$this->fight($p[p_at]*$me_skill["s_at"],$p[p_lv],$m[m_df]*$me_skill["s_m_df"],$m[m_lv],$temp_s);
				}
				$temp_aa=40+round(($p[p_agl]*$me_skill["s_agl"])/($m[m_agl]*$me_skill["s_m_agl"]));
				if($temp_aa>90){$temp_aa=90;}
				if(($p[p_agl]*$me_skill["s_agl"])>($m[m_agl]*$me_skill["s_m_agl"]) && rand(1,100) <= ($temp_aa) )
				{
					$temp_hit=(((($p[p_agl]*$me_skill["s_agl"])-($m[m_agl]*$me_skill["s_m_agl"]))/($m[m_agl]*$me_skill["s_m_agl"]))*8)+1+$me_skill["s_a"];
					$temp_d=round(($temp_d*0.75)*$temp_hit);
					$s.="+"."連續攻擊 ".round($temp_hit)."hit";
				}
			}
		}elseif($act_type=="2")
		{
			$sss=1;
			if(rand(1,100) > 80)
			{
				$sss=(($p[p_mat]-$m[m_mat])/$m[m_mdf])/2;
				if($sss < 1)
				{
					$sss=1;
				}
				$sss=round($sss);
				$s.="+"."連續攻擊 ".$sss."hit";
			}
			if((rand(1,100)+$me_skill["s_s"]) > 90)
			{
				$temp_d=$this->fight($p[p_mat]*$me_skill["s_mat"]*2.5*$sss,$p[p_lv],$m[m_mdf]*$me_skill["s_m_mdf"],$m[m_lv],$temp_s);
				$s.="+".$p[p_sat_name];
			}else
			{
				$temp_d=$this->fight($p[p_mat]*$me_skill["s_mat"]*$sss,$p[p_lv],$m[m_mdf]*$me_skill["s_m_mdf"],$m[m_lv],$temp_s);
			}
		}
		if(strlen($s)>1){$s=substr($s,1,strlen($s));}
		if($_POST["temp_id2"]=="2")//a_mode判斷
		{
			if($temp_d==0)
			{
				echo ",\"parent.miss_date('$p[p_name]','$m[m_name]')\"";
			}else
			{
				echo ",\"parent.pact_date('$temp_d','$s','$ss',$support)\"";
			}
		}
		return $temp_d;
	}

	function fight_m_dm($m,$p,$me_skill,$act_type,$pet,$temp_s)//敵人攻擊function
	{
		$temp_agl=((($m[m_agl]*$me_skill["s_m_agl"]))/(($p[p_agl]*$me_skill["s_agl"])+($m[m_agl]*$me_skill["s_m_agl"])))*100;
		$temp_r=rand(1,100)+$me_skill["s_o"];
		$s="";
		if($act_type=="1")
		{
			if($temp_agl<50){$temp_agl=50;}
			if($temp_agl < $temp_r)
			{
				$temp_d=0;
			}else
			{
				if(rand(1,100) > 80)
				{
					$temp_d=$this->fight($m[m_at]*2*$me_skill["s_m_at"],$m[m_lv],$p[p_df]*$me_skill["s_df"],$p[p_lv],$temp_s);
					$s.="+".$m[m_sat_name];
				}else
				{
					$temp_d=$this->fight($m[m_at]*$me_skill["s_m_at"],$m[m_lv],$p[p_df]*$me_skill["s_df"],$p[p_lv],$temp_s);
				}
				$temp_aa=40+round(($p[p_agl]*$me_skill["s_agl"])/($m[m_agl]*$me_skill["s_m_agl"]));
				if($temp_aa>90){$temp_aa=90;}
				if(($m[m_agl]*$s_m_agl)>($p[p_agl]*$me_skill["s_agl"]) && rand(1,100) >= ($temp_aa) )
				{
					$temp_hit=(((($m[m_agl]*$me_skill["s_m_agl"])-($p[p_agl]*$me_skill["s_agl"]))/($p[p_agl]*$me_skill["s_agl"]))*10)+1;
					$temp_d=round(($temp_d*0.75)*$temp_hit);
					$s.="+"."連續攻擊 ".round($temp_hit)."hit";
				}
			}
		}else
		{
			$sss=1;
			if(rand(1,100) > 80)
			{
				$sss=(($m[m_mat]-$p[p_mat])/$p[p_mdf])/2;
				if($sss < 1)
				{
					$sss=1;
				}
				$sss=round($sss);
				$s.="+"."連續攻擊 ".round($sss)."hit";
			}
			if(rand(1,10) > 9)
			{
				$temp_d=$this->fight($m[m_mat]*$me_skill["s_m_mat"]*2.5*$sss,$m[m_lv],$p[p_mdf]*$me_skill["s_mdf"],$p[p_lv],$temp_s);
			}else
			{
				$temp_d=$this->fight($m[m_mat]*$me_skill["s_m_mat"]*$sss,$m[m_lv],$p[p_mdf]*$me_skill["s_mdf"],$p[p_lv],$temp_s);
			}
		}
		if(strlen($s)>1){$s=substr($s,1,strlen($s));}
		if($_POST["temp_id2"]=="2")//a_mode判斷
		{
			if($temp_d==0)
			{
				echo ",\"parent.miss_date('$m[m_name]','$p[p_name]')\"";
			}else
			{
				if($pet!=null)//寵物抵擋敵人攻擊開始
				{
					if(rand(1,100) < $this->petact && $pet[pe_def] > 0)
					{
						$this->pe_def=1;
						if($pet[pe_def]<=$temp_d)
						{
							echo ",\"parent.pet_def_date('$temp_d','$s','$pet[pe_img]','1')\"";
						}else
						{
							echo ",\"parent.pet_def_date('$temp_d','$s','$pet[pe_img]','')\"";
						}
					}else
					{
						echo ",\"parent.mact_date('$temp_d','$s','')\"";
					}
				}else
				{
					echo ",\"parent.mact_date('$temp_d','$s','')\"";
				}
			}
		}
		return $temp_d;
	}

	function fight_pet_dm($pet_f,$pe_name,$m,$pet_img,$s)//玩家寵物攻擊function
	{
		global $_POST;
		if(rand(1,3)<3) //玩家寵物攻擊
		{
			$temp_d=$this->fight($pet_f,1,$m[m_df],$m[m_lv],1);
		}
		else
		{
			$temp_d=0;
		}
		if($_POST["temp_id2"]=="2")//a_mode判斷
		{
			if($temp_d==0)
			{
				echo ",\"parent.pet_miss_date('$pe_name',".rand(0,3).")\"";
			}else
			{
				echo ",\"parent.pet_act_date('$temp_d','$s','$pet_img')\"";
			}
		}
		return $temp_d;
	}

	function fight_count($user_id,$p,$m,$cp=0,$pet=null,$p_support=null,$my_member="",$datecut=0)
	{
		global $DB_site,$_POST;
		$temp_pd=0;
		$exp=0;
		$s="";
		$sum=0;
		$s_start=0;
		$m[m_hpmax]=$m[m_hp];
		$me_skill=array();
		$me_skill2=array();
		$me_skill["s_at"]=1;$me_skill["s_df"]=1;$me_skill["s_mat"]=1;
		$me_skill["s_mdf"]=1;$me_skill["s_agl"]=1;$me_skill["s_money"]=1;
		$me_skill["s_r"]=0;$me_skill["s_o"]=0;$me_skill["s_s"]=1;
		$me_skill["s_m_at"]=1;$me_skill["s_m_mat"]=1;$me_skill["s_m_mdf"]=1;
		$me_skill["s_m_agl"]=1;$me_skill["s_m_df"]=1;
		$me_skill2=$me_skill;
		$s_kill=$DB_site->query_first("select s_at,s_df,s_mat,s_mdf,s_agl,s_money,s_r,s_o,s_s,s_a,s_m_at,s_m_mat,s_m_df,s_m_mdf,s_m_agl,s_hp from wog_character where ch_id=".$p[p_ch_s_id]."");

		if($p_support!=null)
		{
			$support_skill=array();
//			$support_skill2=array();
/*
			$support_skill["s_at"]=1;$support_skill["s_df"]=1;$support_skill["s_mat"]=1;
			$support_skill["s_mdf"]=1;$support_skill["s_agl"]=1;$support_skill["s_money"]=1;
			$support_skill["s_r"]=0;$support_skill["s_o"]=0;$support_skill["s_s"]=1;
			$support_skill["s_m_at"]=1;$support_skill["s_m_mat"]=1;$support_skill["s_m_mdf"]=1;
			$support_skill["s_m_agl"]=1;$support_skill["s_m_df"]=1;
*/
			$support_skill=$me_skill;
//			$support_skill2=$me_skill;
//			$support_skill2=$support_skill;
			$s2_kill=$DB_site->query_first("select s_at,s_df,s_mat,s_mdf,s_agl,s_money,s_r,s_o,s_s,s_a,s_m_at,s_m_mat,s_m_df,s_m_mdf,s_m_agl,s_hp from wog_character where ch_id=".$p_support[p_ch_s_id]."");
		}

		if($pet!=null)//寵物個性判斷
		{
			switch($pet[pe_type])
			{
				case 1:
					$pet[pe_at]=$pet[pe_at]*1.2;
				break;
				case 2:
					$pet[pe_mt]=$pet[pe_mt]*1.2;
				break;
				case 3:
					$pet[pe_def]=$pet[pe_def]*1.2;
				break;
				case 4:
					$pet[pe_fi]=$pet[pe_fi]*1.5;
				break;
			}
			$petact=((($pet[pe_he]-$pet[pe_hu])/255)*10)+(($pet[pe_fi]/255)*10)+round($p[au]/300);
			if($petact>35)
			{
				$petact=35;
			}
			$this->petact=$petact;
		}
		if($p[d_s]!=NULL)
		{
			$temp_ps=$this->s_check($p[d_s]-$m[m_s]); //屬性判斷
		}else
		{
			$temp_ps=$this->s_check($p[p_s]-$m[m_s]); //屬性判斷
		}
		$temp_ms=$this->s_check($m[m_s]-$p[p_s]); //屬性判斷
			while($p[p_hp]!=0 || $m[m_hp]!=0)
			{
				//srand ((float) microtime() * 10000000); //php 4.2 以上可以不用
				$ss="";
				$p_fast=50;
				$m_fast=50;
				if(rand(1,100) < 10 && $s_kill)//判斷奧義是否發動
				{
					$s_start=1;
					if($s_kill["s_hp"] > 0)
					{
						$bhp=$p[p_hp];
						$up_hp=(($p[p_life]+($p[p_smart]*2))*$s_kill["s_hp"]*10);
						$p[p_hp]=$p[p_hp]+$up_hp;
						echo ",\"parent.fight_event('奧義 $bhp-->$p[p_hp]',$up_hp)\"";
					}
					$this->skill_money_up=$s_kill["s_money"];
					if($p[p_hp]>$p[p_hpmax]){$p[p_hp]=$p[p_hpmax];}
					$ss="1";
					$me_skill=$s_kill;
				}
				if($p[p_agl] > $m[p_agl])
				{
					$p_fast=$p_fast+20;
					$m_fast=$m_fast-20;
				}else
				{
					$p_fast=$p_fast-20;
					$m_fast=$m_fast+20;
				}
				if(rand(1,100) < $p_fast) //己先攻
				{
					//######### pact ##########(己方攻擊開始)
					$temp_d=$this->fight_p_dm($p,$m,$me_skill,$_POST["at_type"],$ss,$temp_ps);//傷害計算
					if(($m[m_hp]-$temp_d)<=0)//判斷是否戰勝
					{
						$exp=$this->win_check($user_id,$p,$m,$my_member,$datecut);
						break;
					}else
					{
						$m[m_hp]=$m[m_hp]-$temp_d;
						$temp_pd+=$temp_d;
					}
					//(己方攻擊結束)

					//######### mact ##########(敵方攻擊開始)
					$temp_d=0;
					$m_type=$this->m_type($m[m_at],$m[m_mat]);//判斷敵方攻擊模式
					$temp_d=$this->fight_m_dm($m,$p,$me_skill,$m_type,$pet,$temp_ms);//傷害計算
					if($this->pe_def)
					{
						$pet[pe_def]=$pet[pe_def]-$temp_d;
						$temp_d=0;
					}
					$this->pe_def=0;
					if(($p[p_hp]-$temp_d)<=0)//判斷是否戰敗
					{
						$p[p_hp]=0;
						if((int)$_POST["act"]>=20)
						{
//							$exp=$this->get_exp(0,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv]*0.2,$p[p_lv],1);
							$exp=0;
						}else
						{
							$exp=$this->get_exp($temp_pd,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv],$p[p_lv],0);
							$DB_site->query("update wog_ch_exp set ch_".$p[ch_id]."=ch_".$p[ch_id]."+1 where p_id=".$user_id." ");
							$this->temp_win=0;
							$this->temp_lost=1;
						}
						$money=0;
						echo ",\"parent.end_date('$p[p_name]','0','$exp',0,'$p[p_hp]')\"";
						$this->win=0;
						$this->lost=1;
						break;
					}else
					{
						$p[p_hp]=$p[p_hp]-$temp_d;
					}
				//(敵方攻擊結束)

				}else //怪先攻
				{
					//######### mact ##########(敵方攻擊開始)
					$temp_d=0;
					$m_type=$this->m_type($m[m_at],$m[m_mat]);//判斷敵方攻擊模式
					$temp_d=$this->fight_m_dm($m,$p,$me_skill,$m_type,$pet,$temp_ms);//傷害計算
					if($this->pe_def)
					{
						$pet[pe_def]=$pet[pe_def]-$temp_d;
						$temp_d=0;
					}
					$this->pe_def=0;
					if(($p[p_hp]-$temp_d)<=0)//判斷是否戰敗
					{
						$p[p_hp]=0;
						if((int)$_POST["act"]>=20)
						{
//							$exp=$this->get_exp(0,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv]*0.2,$p[p_lv],1);
							$exp=0;
						}else
						{
							$exp=$this->get_exp($temp_pd,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv],$p[p_lv],0);
							$DB_site->query("update wog_ch_exp set ch_".$p[ch_id]."=ch_".$p[ch_id]."+1 where p_id=".$user_id." ");
							$this->temp_win=0;
							$this->temp_lost=1;
						}
						$money=0;
						echo ",\"parent.end_date('$p[p_name]','0','$exp',0,'$p[p_hp]')\"";
						$this->win=0;
						$this->lost=1;
						break;
					}else
					{
						$p[p_hp]=$p[p_hp]-$temp_d;
					}
					//(敵方攻擊結束)

					//######### pact ##########(己方攻擊開始)
					$temp_d=$this->fight_p_dm($p,$m,$me_skill,$_POST["at_type"],$ss,$temp_ps);//傷害計算
					if(($m[m_hp]-$temp_d)<=0)//判斷是否戰勝
					{
						$exp=$this->win_check($user_id,$p,$m,$my_member,$datecut);
						break;
					}else
					{
						$m[m_hp]=$m[m_hp]-$temp_d;
						$temp_pd+=$temp_d;
					}
					//(己方攻擊結束)

				}
				//######### p_support ##########(隊友攻擊開始)
				$temp_d=0;
				if($p_support!=null)
				{
					if(rand(1,100) < 15 && $p_support["p_hp"] > ($p_support["p_hpmax"]*0.1))
					{
						if(rand(1,100) < 10)
						{
							$temp_d=$this->fight_p_dm($p_support,$m,$s2_kill,rand(1,2),$ss,$temp_ps,1);//傷害計算
						}else
						{
							$temp_d=$this->fight_p_dm($p_support,$m,$support_skill,rand(1,2),$ss,$temp_ps,1);//傷害計算
						}
						
						if(($m[m_hp]-$temp_d)<=0)//判斷是否戰勝
						{
							$exp=$this->win_check($user_id,$p,$m,$my_member,$datecut);
							break;
						}else
						{
							$m[m_hp]=$m[m_hp]-$temp_d;
							$temp_pd+=$temp_d;
						}
					}
				}
				//(隊友攻擊結束)

				//######### petact ##########(寵物攻擊開始)
				$temp_d=0;
				if($pet!=null)
				{
					if(rand(1,100) < $this->petact && $pet[pe_def] > 0)
					{
						$fight_type=rand(1,3);
						if($fight_type==1)
						{
							$temp_d=$this->fight_pet_dm($pet[pe_at],$pet[pe_name],$m,$pet[pe_mimg],"1");//傷害計算
						}elseif($fight_type==2)
						{
							$temp_d=$this->fight_pet_dm($pet[pe_mt],$pet[pe_name],$m,$pet[pe_mimg],"2");//傷害計算
						}elseif($fight_type==3)
						{
							$temp_d=$this->fight_pet_dm(($pet[pe_at]+$pet[pe_mt])*1.5,$pet[pe_name],$m,$pet[pe_mimg],"3");//傷害計算
						}
						$pet[pe_mimg]="";
					}
					if(($m[m_hp]-$temp_d)<=0)//判斷是否戰勝
					{
						$exp=$this->win_check($user_id,$p,$m,$my_member,$datecut);
						break;
					}else
					{
						$m[m_hp]=$m[m_hp]-$temp_d;
						$temp_pd+=$temp_d;
					}
				}
				//(寵物攻擊結束)
				
				$sum++;
				if($sum>=$this->f_count)//判斷戰鬥是否超過回合數設定
				{
					if((int)$_POST["act"]>=20)
					{
//						$exp=$this->get_exp($temp_pd,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv]*0.2,$p[p_lv],0);
						$exp=0;
					}else
					{
						$exp=$this->get_exp($temp_pd,$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv]*0.6,$p[p_lv],0);
					}
					$money=0;
					echo ",\"parent.end_date('$p[p_name] ".sprint($lang['wog_fight_over_time'],$this->f_count)." ','0','$exp',0,'$p[p_hp]')\"";
					$this->win=0;
					$this->lost=1;
					break;
				}
				//(敵方攻擊結束)
				if($s_start==1)//結束奧義狀態
				{
					$s_start=0;
					$me_skill=$me_skill2;
				}
				if($p[p_hpmax]*$this->f_hp > $p[p_hp] && $p[d_item_id]>0 && $p[d_g_hp] > 0)
				{
					$bhp=$p[p_hp];
					$p[p_hp]=$p[p_hp]+$p[d_g_hp];
					if($p[p_hp]>$p[p_hpmax]){$p[p_hp]=$p[p_hpmax];}
					$p[d_item_id]=0;
					echo ",\"parent.fight_event('$p[d_name] $bhp-->$p[p_hp]',$p[d_g_hp])\"";
					echo ",\"parent.d_item_name=''\"";
				}
			}
			$this->cp_m_hp=$m[m_hp];//冠軍的hp,若在冠軍挑戰模式下,冠軍hp將會被寫入db
			unset($m);
			unset($s_kill);
			unset($me_skill);
			unset($me_skill2);
			unset($s2_kill);
			unset($support_skill);
//			unset($support_skill2);
			unset($pet);
			unset($my_member);
			$p[p_exp]+=$exp;
			$money=$this->money;
			if($p[d_item_id]==""){$p[d_item_id]=0;}
			if($p[p_exp]>$p[p_nextexp])//判斷是否升級
			{
				$this->lv_up($user_id,$p,$money);
			}else
			{
				$DB_site->query("update wog_player set p_exp=".$p[p_exp].",p_money=p_money+".($money+$cp).",p_hp=".$p[p_hp].",p_win=p_win+".$this->temp_win.",p_lost=p_lost+".$this->temp_lost.",p_act_time ='".time()."',p_online_time=".time()."
				,p_sat_name='".htmlspecialchars(stripslashes(trim($_POST["sat_name"])))."',d_item_id=".$p[d_item_id].",p_place=".$this->p_place."
				where p_id=".$user_id." ");
			}
			return $p;
			unset($p);
	}

	function win_check($user_id,$p,$m,$my_member,$datecut)
	{
		global $DB_site,$_POST;
		if((int)$_POST["act"]>=20)
		{
//			$exp=$this->get_exp($m[m_hpmax],$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv]*0.2,$p[p_lv],1);
			$exp=0;
			$money=0;
		}else
		{
			$exp=$this->get_exp($m[m_hpmax],$m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv],$p[p_lv],1);
			$money=$this->get_money($m[m_hpmax],$m[m_at],$m[m_mat],$m[m_lv])*$this->skill_money_up;
			$DB_site->query("update wog_ch_exp set ch_".$p[ch_id]."=ch_".$p[ch_id]."+1 where p_id=".$user_id." ");
			$this->temp_win=1;
			$this->temp_lost=0;
		}
		$this->win=1;
		$this->lost=0;
		$this->money=round($money);

		$member_exp=0;
		if(!empty($my_member["members"]) && $exp > 0)
		{
			$member_exp=round(($exp*0.3)/$my_member["members"]);
			$exp=$exp*0.7;
		}
		if(!empty($my_member["members"]) && $exp > 0)
		{
			$DB_site->query("update wog_player set p_exp=p_exp+".$member_exp."	where p_id<>".$user_id." and t_id=".$p["t_id"]." and p_act_time > $datecut and p_place=".$this->p_place." and p_lock=0 ");
		}
		$exp=round($exp);
		echo ",\"parent.end_date('$p[p_name]','1','$exp','$this->money','$p[p_hp]')\"";
		return $exp;
	}
	function s_check($temp_s)
	{
		switch($temp_s)
		{
			case -1:
				$temp_s=1.3;
			break;
			case 1:
				$temp_s=0.7;
			break;
			case 5:
				$temp_s=1.3;
			break;
			case -5:
				$temp_s=0.7;
			break;
			default:
				$temp_s=1;
			break;
		}
		return $temp_s;
	}
}
?>