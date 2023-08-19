<?
/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/01/30
 URL : http://www.2233.idv.tw

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

//no forum
define('USER_TABLE','wog_player');
define('MONEY_FIELB','p_money');
define('BANK_FIELB','p_bank');
define('USER_ID','p_id');
$forum_check="\$bbs_id=1;";
$forum_message="";
/*
//vbb2.X support
define('USER_TABLE','user');
define('MONEY_FIELB','money');
define('BANK_FIELB','bank');
define('USER_ID','userid');
$forum_check="include_once('./forum_support/function_vbb2.php');\$bbuserinfo=vbb_check();\$bbs_id=\$bbuserinfo[userid];";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->vbb_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

//vbb3.0.X support
define('USER_TABLE','user');
define('MONEY_FIELB','money');
define('BANK_FIELB','bank');
define('USER_ID','userid');
$forum_check="include_once('./forum_support/function_vbb3.php');\$bbuserinfo=vbb3_check();\$bbs_id=\$bbuserinfo[userid];";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->vbb3_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

//DISCUZ! 2.5 support
define('USER_TABLE','cdb_members');
define('MONEY_FIELB','money');
define('BANK_FIELB','bank');
define('USER_ID','uid');
$forum_check="include_once('./forum_support/function_dz2.php');\$bbs_id=dz_check();";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->dz_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

//phpbb support
define('USER_TABLE','phpbb_users');
define('MONEY_FIELB','user_money');
define('BANK_FIELB','user_bank');
define('USER_ID','user_id');
$forum_check="include_once('./forum_support/function_phpbb.php');\$bbs_id=phpbb_check(\$p_ip);";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->phpbb_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

//DISCUZ! 4.1.0 support
define('USER_TABLE','cdb_members');
define('MONEY_FIELB','money');
define('BANK_FIELB','bank');
define('USER_ID','uid');
$forum_check="include_once('./forum_support/function_dz4.php');\$bbs_id=dz_check();";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->dz_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

//vbb3.5.X support
define('USER_TABLE','user');
define('MONEY_FIELB','money');
define('BANK_FIELB','bank');
define('USER_ID','userid');
$forum_check="include_once('./forum_support/function_vbb35.php');\$bbs_id=vbb35_check();";
$forum_message="\$wog_act_class = new wog_act_message;";
$forum_message.="\$wog_act_class->vbb3_message(\$HTTP_COOKIE_VARS[\"wog_cookie\"],\$HTTP_COOKIE_VARS[\"wog_cookie_name\"],\$HTTP_COOKIE_VARS[\"wog_bbs_id\"]);";

*/

$root_path = './../';//論壇主程式路徑
$wog_arry["cookie_debug"]="fewf_De&Ghdf32"; //驗證碼,請修改內容,請勿使用預設值
$wog_arry["del_day"]=720; //幾天沒玩刪除角色
$wog_arry["total_point"]=10; //創造角色所給予的點數
$wog_arry["offline_time"]=600;//幾秒後沒執行判斷為離線
$wog_arry["player_num"]=3;//創造角色數目限制
$wog_arry["sale_day"]=10;//限制能拍賣幾天
$wog_arry["view2_money"]=1500;//查看對手費用
$wog_arry["chang_face"]=300000;//改變圖像費用
$wog_arry["creat_group"]=200000;//創造工會費用
$wog_arry["chang_sex"]=1000000;//變性費用
$wog_arry["item_limit"]=15;//道具數量上限,建議值15
$wog_arry["player_age"]=30;//多少天一歲

$wog_arry["hotel_money"]=10;//住宿所需要的金額
$wog_arry["hotel_time"]=5;//住宿所需要等待秒數
$wog_arry["hotel_die_time"]=20;//hp=0 住宿所需要等待秒數

$wog_arry["etc_dely_time"]=3;//wog_etc.php延遲時間
$wog_arry["act_dely_time"]=3;//wog_act.php延遲時間
//$wog_arry["fight_dely_time"]=15;//wog_fight.php延遲時間
$wog_arry["online_limit"]=100;//線上人數
$wog_arry["login_time"]=18;//等待登入時間
$wog_arry["gzip_compress"]=1;//gzip設定 1開 0關

$wog_arry["cp_mmoney"]=5000;//挑冠軍需要多少金額
$wog_arry["f_time"]=15;//每一場戰鬥間隔時間
$wog_arry["f_count"]=40;//每一場戰鬥回合限制
$wog_arry["f_hp"]=15;//每一場戰鬥低於多少HP自動使用恢復劑

$wog_arry["g_f_count"]=30;//工會戰鬥回合限制
$wog_arry["g_f_stime"]=0;//工會戰鬥開始時間 24時制
$wog_arry["g_f_etime"]=24;//工會戰鬥結束時間 24時制
$wog_arry["g_f_time"]=20;//工會戰間格時間
$wog_arry["g_ea_time"]=20;//領土復建所須時間(單位分鐘)
$wog_arry["g_a_peo"]=3;//駐守領土人數上限

$wog_arry["t_peo"]=5;//隊伍人數上限
$wog_arry["t_lv_limit"]=50;//組隊等級限制
$wog_arry["t_time"]=3;//支援及經驗值分享有效時間(單位分鐘)

$wog_arry["pet_ac_time"]=30;//寵物特訓餵食間隔時間
$wog_arry["pet_f_time"]=28800;//寵物競技間隔時間(預設8小時)
$wog_arry["pet_fu_time"]=15;//寵物飢餓間隔時間(單位分鐘)
$wog_arry["pet_age"]=864000;//寵物幾秒一歲(預設10天)
$wog_arry["pet_eat_money"]=50;//寵物餵食金額

$wog_arry["event_ans"]=1;//隨機問答 1開 0關
$wog_arry["event_ans_max"]=200;//隨機問答出現機率 預設值150,表示機率1/150
//$wog_arry["USE_GD"]= "YES";//使用GD YES開啟 NO關閉
//$wog_arry["file_name"]="key";//圖檔名稱
//$wog_arry["file_type"]="gif";//圖檔類型
$wog_arry["keylen"]=5;//驗證碼長度
$wog_arry["attempts"]=8;//允許回答次數
$wog_arry["unfreeze"]=48;//多久解開帳號，預設48小時

$wog_arry["logout_url"]="http://chat.2233.idv.tw/images/wog/black.htm";//登出後連結的網址
?>