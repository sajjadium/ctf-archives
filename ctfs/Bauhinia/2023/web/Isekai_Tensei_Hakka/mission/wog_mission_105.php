<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/11/01
 URL : http://www.2233.idv.tw
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */
function mission_start($user_id,$m_id)
{
}
function mission_body($user_id,$m_id)
{
}
function mission_end($user_id,$m_id)
{
	global $DB_site,$_POST,$a_id,$lang,$wog_item_tool,$wog_mission_tool;
	$m_book=$wog_mission_tool->mission_check($user_id,$m_id);
	$wog_mission_tool->mission_money($user_id,1500);

	$wog_mission_tool->mission_status_update($user_id,$m_id,$m_book["m_end_message"],$m_book["m_lv"]);
}
?>