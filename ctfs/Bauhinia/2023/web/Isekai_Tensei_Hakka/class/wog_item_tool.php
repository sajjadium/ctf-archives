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

class wog_item_tool{
//################## item_out ################
function item_out($user_id,$item_id,$item_num=0,$item_now=NULL)
{
	global $DB_site,$lang,$a_id;
	if($item_now != NULL)
	{
		$item[0]=$item_now;
	}else
	{
		$sql="select ".$a_id." from wog_item where p_id=".$user_id."  ";
		$item=$DB_site->query_first($sql);
	}
	if($item[0]=="N/A" || $item[0]=="")
	{
		alertWindowMsg($lang['wog_act_errwork']);
	}else
	{
		if(is_array($item[0]))
		{
			$temp_pack=$item[0];
		}else
		{
			$temp_pack=split(",",$item[0]);
		}
		$temp_pack2 = array();
		if($a_id=="d_item_id")
		{
			$adds=$item_id;
			if($item_num==0)
			{
				$item_num=1;
			}
			$buy_num=$item_num;
			if($item_num < 0 || $item_num >30)
			{
				alertWindowMsg($lang['wog_act_errdate']);
			}
			for($i=count($temp_pack)-1;$i>-1;$i--)
			{
				$temp_packs=split("\*",$temp_pack[$i]);
				if($temp_packs[0]==$adds)
				{
					if(($temp_packs[1]-$buy_num) < 1)
					{
						$buy_num=$buy_num-$temp_packs[1];
					}else
					{
						$temp_pack2[]=$temp_packs[0]."*".($temp_packs[1]-$buy_num);
						$buy_num=0;
					}
				}else
				{
					$temp_pack2[]=$temp_packs[0]."*".$temp_packs[1];
				}
			}
			if($buy_num > 0)
			{
				alertWindowMsg($lang['wog_act_errnum']."--".$buy_num);
			}
//			$temp_ss=$temp_pack2;
//			$temp_ss=implode(',', $temp_pack2);//扣掉選擇後剩下的東西
			return $temp_pack2;
		}else
		{
			if($item_num < 0 || $item_num > 1)
			{
				alertWindowMsg($lang['wog_act_errdate']);
			}
			$adds=split(",",$item_id);
			$s="";
			$s2="";
			if(is_array($item[0]))
			{
				$items=$item[0];
			}else
			{
				$items=split(",",$item[0]);
			}
			for($i=0;$i<count($adds);$i++)
			{
				$s="";
				$chks=false;
				for($j=0;$j<count($items);$j++)
				{
					if($adds[$i]!=$items[$j] || $chks)
					{
						$temp_pack2[]=$items[$j];
					}else
					{
						$s2.=",".$adds[$i];
						$chks=true;
					}
				}
			}
			if($s2=="" || !$chks)
			{
				alertWindowMsg($lang['wog_act_errnum']);
			}
			$s2=substr($s2,1,strlen($s2));//所選擇的東西
//			$temp_ss=$temp_pack2;//扣掉選擇後剩下的東西
			return $temp_pack2;
		}
	}
	unset($temp_pack);
	unset($temp_pack2);
	unset($items);
	unset($adds);
	unset($s);
	unset($s2);
	unset($item);
}

//################## item_syn_special_out ################
function item_syn_special_out($user_id,$item_id,$item_num=0,$item_now)
{
	global $DB_site,$lang,$a_id,$syn_debug,$syn_item;
	$chks=false;
	if(isset($item_now))
	{
		$item[0]=$item_now;
	}else
	{
		$sql="select ".$a_id." from wog_item where p_id=".$user_id."  ";
		$item=$DB_site->query_first($sql);
	}
	if($item[0]=="N/A" || $item[0]=="")
	{
		alertWindowMsg($lang['wog_act_errwork']);
	}else
	{
		if(is_array($item[0]))
		{
			$temp_pack=$item[0];
		}else
		{
			$temp_pack=split(",",$item[0]);
		}
		$temp_pack2 = array();
		$adds=$syn_item[$item_id];
		if($a_id=="d_item_id")
		{
			if($item_num==0)
			{
				$item_num=1;
			}
			$buy_num=$item_num;
			if($item_num < 0 || $item_num > 9)
			{
				alertWindowMsg($lang['wog_act_errdate']);
			}
			for($i=0;$i<count($temp_pack);$i++)
			{
				$temp_packs=split("\*",$temp_pack[$i]);
				if($temp_packs[0]==$adds)
				{
					if(($temp_packs[1]-$buy_num) < 1)
					{
						$buy_num=$buy_num-$temp_packs[1];
					}else
					{
						$temp_pack2[]=$temp_packs[0]."*".($temp_packs[1]-$buy_num);
						$buy_num=0;
					}
					if(!$chks)
					{
						$syn_debug++;
						$chks=true;
						$syn_item[$item_id]=0;
					}
				}else
				{
					$temp_pack2[]=$temp_packs[0]."*".$temp_packs[1];
				}
			}
//			$temp_ss=$temp_pack2;
//			$temp_ss=implode(',', $temp_pack2);//扣掉選擇後剩下的東西
			return $temp_pack2;
		}else
		{
			$s="";
			$s2="";
			if(is_array($item[0]))
			{
				$items=$item[0];
			}else
			{
				$items=split(",",$item[0]);
			}
				$s="";
				for($j=0;$j<count($items);$j++)
				{
					if($adds!=$items[$j] || $chks)
					{
						$temp_pack2[]=$items[$j];
					}else
					{
						if(!$chks)
						{
							$chks=true;
							$syn_debug++;
							$syn_item[$item_id]=0;
						}
					}
				}
//			$s2=substr($s2,1,strlen($s2));//所選擇的東西
//			$temp_ss=$temp_pack2;//扣掉選擇後剩下的東西
			return $temp_pack2;
		}
	}
	unset($temp_pack);
	unset($temp_pack2);
	unset($items);
	unset($adds);
	unset($s);
	unset($s2);
	unset($item);
}

//################## item_in ################
function item_in($temp_pack,$adds,$buy_num=0)
{
	global $a_id;
	if($a_id=="d_item_id")
	{
		for($i=0;$i<count($temp_pack);$i++)
		{
			$temp_packs=split("\*",$temp_pack[$i]);
			if($temp_packs[0]==$adds)
			{
				$temp_packs[1]=$temp_packs[1]+$buy_num;
				if($temp_packs[1] > 9)
				{
					$buy_num=$temp_packs[1]-9;
					$temp_packs[1]=9;
				}else
				{
					$buy_num=0;
				}
			}
			$temp_pack[$i]=$temp_packs[0]."*".$temp_packs[1];
		}
		if($buy_num > 0)
		{
			$temp_pack[]=$adds."*".$buy_num;
		}
		return $temp_pack;
	}else
	{
		$temp_pack[]=$adds;
		return $temp_pack;
	}
}

}
