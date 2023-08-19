===================================================== 
 WOG V3.0.0
 Copyright (C)  ETERNAL <iqstar@ms24.hinet.net>
 Modify : 2006/04/22
 URL : http://www.2233.idv.tw

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
===================================================== 

Online FF Battle-WOG官方聯盟推廣處 http://www.2233.idv.tw/viewforum.php?f=36
測試站台 http://www.2233.idv.tw/wog/

----------------------WOG V3(2006/04/22) ------------------------
1.新增職業限制武器 
2.新增合成功能 
3.新增寵物協助戰鬥 
4.每位角色可以養三隻寵物 
5.新增組隊功能 
6.新增武器屬性 
7.新增任務功能 
8.新增支援Discuz 4.0，VBB3.5.X 
9.其他更新內容(http://www.2233.idv.tw/viewtopic.php?t=19248) 
-------------------------------------------------------------------
環境需求：
MySQL 版本 4.0以上
PHP 版本 4.3以上 
空間必須支援GD(http://tw.php.net/manual/tw/function.gd-info.php)
______________________________________________________________
安裝:
角色圖檔下載點 http://iqstar.myweb.hinet.net/wog_img.exe
sql資料檔下載點 http://iqstar.myweb.hinet.net/wog3_sql_utf8.rar (UTF-8版)
sql資料檔下載點 http://iqstar.myweb.hinet.net/wog3_sql_big5.rar (big5版)
1.請修改/forum_support/config/config.php 檔案內容
2.把圖檔解壓縮放在圖都放在 /wog下面(壓縮檔會自動產生img目錄)
4.解開sql檔，將sql檔匯入資料庫裡
______________________________________________________________
注意事項:
1.想與論壇共用請記得修改 /wog/wog_act_config.php 中的$root_path變數
(預設值 $root_path = './../';)表示wog這個目錄在論壇主目錄下面

2.遊戲參數設定在wog_act_config.php

3.使用vbb3.5.X請注意!!!!
請修改/inculudes/class_core.php
###尋找###
$userinfo = fetch_userinfo($session['userid'], $useroptions, (!empty($languageid) ? $languageid : $session['languageid']));
###改成###
$userinfo = fetch_userinfo($session['userid'], $useroptions, (!empty($languageid) ? $languageid : $session['languageid']),$this->registry);

###尋找###
$userinfo = fetch_userinfo($userid, $useroptions, $languageid);
###改成###
$userinfo = fetch_userinfo($userid, $useroptions, $languageid,$this->registry);

請修改/inculudes/functions.php
###尋找###
function fetch_userinfo(&$userid, $option = 0, $languageid = 0)
###改成###
function fetch_userinfo(&$userid, $option = 0, $languageid = 0,$db=null)
###尋找###
	global $vbulletin, $usercache, $vbphrase, $permissions, $phrasegroups;
###後面加上###
	if(empty($vbulletin)){$vbulletin=$db;}
	
4.與論壇共用皆須安裝銀行hack
phpbb銀行
http://www.phpbb-tw.net/phpbb/viewtopic.php?t=19509
DISCUZ銀行
http://www.freediscuz.net/bbs/viewthread.php?tid=34739&fpage=1
VBB3銀行
http://www.vbulletin-china.com/showthread.php?t=1845&highlight=bank
______________________________________________________________
感謝事項：
v2到v3斷斷續續開發了將近一年多，感謝多位網友的支持以及不斷提供意見
特別感謝涅魂、唐沁、New-TypeChobits、~木林森~、小剎、cku100 長期以來不斷的支持整理意見
還有很多沒提到的朋友，謝謝您們的支持
______________________________________________________________
贊助：
開發遊戲以及維持網站運作，需要投入時間以及資金
若您覺得這遊戲不錯，願意贊助開發
請使用Paypal贊助，進入Paypal的首頁(http://www.paypal.com)
選擇Send Money，輸入帳號：iqstar@ms24.hinet.net 
您的支持是開發的源動力
______________________________________________________________
補充說明:
1.
防從別端直接執行戰鬥程式練攻方法..
檔案wog_act.php,wog_fight.php
/*
if(substr(getenv("HTTP_REFERER"),0,26)!="http://bbs.2233.idv.tw/wog")
{
	alertWindowMsg("請重http://www.2233.idv.tw/wog/ 進入遊戲");
}
*/
把http://www.2233.idv.tw/wog改成你程式的位子
並計算長度把26改成你的長度
然後把註解拿掉就可以使用

2.
怪物圖檔的預設目錄在img/monster下面,預設圖是no_img.jpg
欲改變怪物圖檔或新增怪物圖片
在資料表 wog_monster 裡面 m_img 輸入圖片檔名
把圖片放入img/monster下面
圖片的size 150*158 為佳

3.
WOG推薦外掛:
WOG 聊天程式(php版)(作者 龍神王)
http://www.phpbb-tw.net/phpbb/viewtopic.php?t=18980
WOG 聊天程式(asp版)(作者 lansea)
http://www.2233.idv.tw/viewtopic.php?t=7619

