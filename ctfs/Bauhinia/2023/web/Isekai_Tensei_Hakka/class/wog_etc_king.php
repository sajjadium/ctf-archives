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

class wog_etc_king{
	function king_view()
	{
		global $DB_site,$wog_arry,$lang;
		echo charset();
		echo "<script language=JavaScript >\n";
		echo "parent.message_cls();\n";
		//######################## WIN ##############################
		
		$sql="select p_name,p_win,i_img,p_img_set,p_img_url from wog_player order by p_win desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$ps["p_win"]." WIN";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_win']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## LV ##############################
		
		$sql="select p_name,p_lv,i_img,p_img_set,p_img_url from wog_player order by p_lv desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$lang['wog_etc_king_lv']." ".$ps["p_lv"]."";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_lv']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## HP ##############################
	
		$sql="select p_name,p_hpmax,i_img,p_img_set,p_img_url from wog_player order by p_hpmax desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$lang['wog_etc_king_hp']." ".$ps["p_hpmax"]."";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_hp']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## AT ##############################
	
		$sql="select p_name,p_at,i_img,p_img_set,p_img_url from wog_player order by p_at desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$lang['wog_etc_king_ac']." ".$ps["p_at"]."";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_ac']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## MAT ##############################
	
		$sql="select p_name,p_mat,i_img,p_img_set,p_img_url from wog_player order by p_mat desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$lang['wog_etc_king_mc']." ".$ps["p_mat"]."";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_mc']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## AGL ##############################
	
		$sql="select p_name,p_agl,i_img,p_img_set,p_img_url from wog_player order by p_agl desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].",".$lang['wog_etc_king_agl']." ".$ps["p_agl"]."";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_agl']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## pk ##############################
	
		$sql="select p_name,p_pk_win,i_img,p_img_set,p_img_url from wog_player order by p_pk_win desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].", ".$ps["p_pk_win"]." WIN";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('PK WIN TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## race ##############################
	
		$sql="select p_name,p_cho_win,i_img,p_img_set,p_img_url from wog_player order by p_cho_win desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].", ".$ps["p_cho_win"]." WIN";
		}
		$s=substr($s,1,strlen($s));
		echo "parent.king_view('".$lang['wog_etc_king_race']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
	
		//######################## money ##############################
	
		$sql="select p_name,p_money,i_img,p_img_set,p_img_url from wog_player order by p_money desc LIMIT 5 ";
		$p=$DB_site->query($sql);
		$s="";
		while($ps=$DB_site->fetch_array($p))
		{
			if($ps["p_img_set"]==1)
			{
				$ps["i_img"]=$ps["p_img_url"];
			}
			$s.=";".$ps["i_img"].",".$ps["p_name"].", ".$ps["p_money"]." money";
		}
		$s=substr($s,1,strlen($s));
		$DB_site->free_result($p);
		$DB_site->close();
		echo "parent.king_view('".$lang['wog_etc_king_money']." TOP','$s');\n";
		echo "parent.wog_view.document.write('<hr size=1 color=#A2A9B8>');\n";
		echo "</script>\n";
		compress_exit();
	}

}
?>