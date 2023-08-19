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

class wog_fight_event{
//########## get_item begin   ##########
	function get_item($user_id,$m_d_id,$p_st,$p_bag)
	{
		global $DB_site,$a_id,$wog_arry,$wog_item_tool;
		$sql="select d_id,d_name,d_type,d_vip from wog_df where d_id=".$m_d_id."";
		$item=$DB_site->query_first($sql);
		check_type($item[d_type],1);
		$sql="select ".$a_id." from wog_item where p_id=".$user_id."";
		$pack=$DB_site->query_first($sql);
		$pack[0]=trim($pack[0]);
		$temp_pack=array();
		if(!empty($pack[0]))
		{
			$temp_pack=split(",",$pack[0]);
		}
		if($a_id=="d_item_id")
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$m_d_id,1);
			$bag=$wog_arry["item_limit"]+$p_bag;
		}else
		{
			$temp_pack=$wog_item_tool->item_in($temp_pack,$m_d_id);
			$bag=$wog_arry["item_limit"];
		}
		if(count($temp_pack) <= $bag)
		{
			$pack[0]=implode(',', $temp_pack);
			$DB_site->query("update wog_item set ".$a_id."='".$pack[0]."' where p_id=".$user_id."");
			echo ",\"parent.get_item('$item[d_name]',1)\"";
		}else
		{
			echo ",\"parent.get_item('$item[d_name]',0)\"";
		}
		unset($item);
		unset($temp_pack);
		unset($pack);
		unset($a_id);
	}
//########## event_start  ##########
	
	function event_start($user_id,$p_attempts)
	{
		global $DB_site,$wog_arry,$lang;
		if($p_attempts>$wog_arry["attempts"])
		{
			$DB_site->query("update wog_player set p_lock=1,p_lock_time=".time()." where p_id=".$user_id."");
			cookie_clean();
			alertWindowMsg(sprintf($lang['wog_fight_event_lock'],$wog_arry["unfreeze"]));
		}else
		{
			$get_key=$this->gen_key(); 
			$DB_site->query("update wog_player set p_key='".$get_key."',p_attempts=p_attempts+1 where p_id=".$user_id.""); 
		}
		showscript("parent.event();");
	}
	
//########## event_creat  ##########
	
	function event_creat($user_id)
	{
		global $DB_site,$wog_arry; 
		$get_key=$this->gen_key(); 
		$DB_site->query("update wog_player set p_key='".$get_key."',p_attempts=0  where p_id=".$user_id.""); 
		showscript("parent.event();");
	}
	
	//Gen Key. 
	function gen_key() 
	{ 
		global $wog_arry; 
//		$key = ""; 
		//u can add your own image below here. 
		$confirm_chars = array('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',  'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9');

		list($usec, $sec) = explode(' ', microtime()); 
		mt_srand($sec * $usec); 

		$max_chars = count($confirm_chars) - 1;
		$key = '';
		for ($i = 0; $i < $wog_arry["keylen"]; $i++)
		{
			$key .= $confirm_chars[mt_rand(0, $max_chars)];
		}
/*
		$count = count($chars) - 1; 
		srand((double)microtime()*1000000); 
		for($i = 0; $i < $wog_arry["keylen"]; $i++) 
		{
			$key .= $chars[rand(0, $count)]; 
		}
*/
		return($key);
	}
	

//########## pet_stats  ##########
	
	function pet_stats()
	{
		$pet[pe_at]=rand(1,10);
		$pet[pe_mt]=rand(1,10);
		$pet[pe_def]=rand(1,10);
		$pet[pe_type]=rand(1,4);
		return $pet;
	}
/*
//####################   Gen Image with GD   #################### 
	//####################   GD JPEG   #################### 
	function img_gd_jpeg($name,$words){ 
		$words_size=strlen($words); 
		for($i=0;$i<$words_size;$i++) 
		{ 
			$this_number[$i]=substr($words,$i,1); 
			$this_size_temp=getimagesize("anti-bot/validation_".$this_number[$i].".jpg"); 
			$this_width[$i]=$this_size_temp[0]; 
			$this_height[$i]=$this_size_temp[1]; 
			$image_width+=$this_size_temp[0]; 
		} 
		$image_height=max($this_height); 
	
		$base=@imagecreate($image_width,$image_height); 
		if(!$base){header("location:anti-bot/error2.jpg");exit;} 
	
		for($i=0;$i<$words_size;$i++) 
		{ 
			$image=imagecreatefromjpeg("anti-bot/validation_".$this_number[$i].".jpg") or die("false 2"); 
			imagecopyresized($base,$image,0+$sum_width,0,0,0,$this_width[$i],$this_height[$i],$this_width[$i],$this_height[$i]) or die("false 3"); 
			$sum_width+=$this_width[$i]; 
			imagedestroy($image); 
		} 
		imagejpeg($base,"${name}.jpg"); 
		imagedestroy($base); 
	}
	
//####################   GD GIF   #################### 
	function img_gd_gif($name,$words){ 
		$words_size=strlen($words); 
	
		for($i=0;$i<$words_size;$i++) 
		{ 
			$this_number[$i]=substr($words,$i,1); 
			$this_size_temp=getimagesize("anti-bot/validation_".$this_number[$i].".gif"); 
			$this_width[$i]=$this_size_temp[0]; 
			$this_height[$i]=$this_size_temp[1]; 
			$image_width+=$this_size_temp[0]; 
		} 
		$image_height=max($this_height); 
	
		$base=@imagecreate($image_width,$image_height); 
		if(!$base){header("location:anti-bot/error2.gif");exit;} 
	
		for($i=0;$i<$words_size;$i++) 
		{ 
			$image=imagecreatefromgif("anti-bot/validation_".$this_number[$i].".gif") or die("false 2"); 
			imagecopyresized($base,$image,0+$sum_width,0,0,0,$this_width[$i],$this_height[$i],$this_width[$i],$this_height[$i]) or die("false 3"); 
			$sum_width+=$this_width[$i]; 
			imagedestroy($image); 
		} 
		imagegif($base,"${name}.gif"); 
		imagedestroy($base); 
	}
//####################   Gen Image without GD   #################### 
	function img_no_gd($words) 
	{ 
		global $antibot; 
		$words_size=strlen($words); 
		for($i = 0; $i < $words_size; $i++) 
		{ 
		   $validation_images .= "<img src=http://www.233.idv.tw/wog/" . 'anti-bot/validation_' . $words{$i} .".". $wog_arry["file_type"] . '>'; 
		} 
		return $validation_images; 
	} 
*/
}

?>