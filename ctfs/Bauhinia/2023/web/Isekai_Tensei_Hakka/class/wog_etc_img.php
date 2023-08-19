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

class wog_etc_img{

	function img_view()
	{
		global $DB_site,$wog_arry;
		echo '<body bgcolor="#000000" text="#EFEFEF" link="#EFEFEF" vlink="#EFEFEF" alink="#EFEFEF">';
		echo '<table width="95%" border="1" cellspacing="0" cellpadding="0" align="center">';
		$img123=$DB_site->query("select * from wog_img ");
		$sum=0;
		while(is_array($img123s=$DB_site->fetch_array($img123)))
		{
			$sum ++;
			if(($sum%3)==1){echo "<tr>";}
			echo "<td align=center ><img src=http://chat.2233.idv.tw/images/wog/img/".$img123s[i_filename]."><br>no. ".$img123s[i_id]."</td>";
		}
		$DB_site->free_result($img123);
		unset($img123s);
		$DB_site->close();
		echo "</table>";
		echo "</body>";
		compress_exit();
	}
}	
?>