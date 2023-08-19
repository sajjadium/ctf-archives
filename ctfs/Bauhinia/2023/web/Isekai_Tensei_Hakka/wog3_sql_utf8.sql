# MySQL-Front 3.2  (Build 13.39)


# Host: 127.0.0.1    Database: test123
# ------------------------------------------------------
# Server version 4.0.26-nt

#
# Table structure for table wog_ch_exp
#

DROP TABLE IF EXISTS `wog_ch_exp`;
CREATE TABLE `wog_ch_exp` (
  `p_id` int(10) unsigned NOT NULL default '0',
  `ch_6` smallint(4) unsigned NOT NULL default '0',
  `ch_7` smallint(4) unsigned NOT NULL default '0',
  `ch_8` smallint(4) unsigned NOT NULL default '0',
  `ch_9` smallint(4) unsigned NOT NULL default '0',
  `ch_10` smallint(4) unsigned NOT NULL default '0',
  `ch_11` smallint(4) unsigned NOT NULL default '0',
  `ch_12` smallint(4) unsigned NOT NULL default '0',
  `ch_13` smallint(4) unsigned NOT NULL default '0',
  `ch_14` smallint(4) unsigned NOT NULL default '0',
  `ch_15` smallint(4) unsigned NOT NULL default '0',
  `ch_16` smallint(4) unsigned NOT NULL default '0',
  `ch_17` smallint(4) unsigned NOT NULL default '0',
  `ch_18` smallint(4) unsigned NOT NULL default '0',
  `ch_19` smallint(4) unsigned NOT NULL default '0',
  `ch_20` smallint(4) unsigned NOT NULL default '0',
  `ch_21` smallint(4) unsigned NOT NULL default '0',
  `ch_22` smallint(4) unsigned NOT NULL default '0',
  `ch_23` smallint(4) unsigned NOT NULL default '0',
  `ch_24` smallint(4) unsigned NOT NULL default '0',
  `ch_25` smallint(4) unsigned NOT NULL default '0',
  `ch_26` smallint(4) unsigned NOT NULL default '0',
  `ch_27` smallint(4) unsigned NOT NULL default '0',
  `ch_28` smallint(4) unsigned NOT NULL default '0',
  `ch_29` smallint(4) unsigned NOT NULL default '0',
  `ch_30` smallint(4) unsigned NOT NULL default '0',
  `ch_31` smallint(4) unsigned NOT NULL default '0',
  `ch_32` smallint(4) unsigned NOT NULL default '0',
  `ch_33` smallint(4) unsigned NOT NULL default '0',
  `ch_34` smallint(4) unsigned NOT NULL default '0',
  `ch_35` smallint(4) unsigned NOT NULL default '0',
  `ch_36` smallint(4) unsigned NOT NULL default '0',
  `ch_37` smallint(5) unsigned NOT NULL default '0',
  `ch_38` smallint(5) unsigned NOT NULL default '0',
  PRIMARY KEY  (`p_id`),
  KEY `p_id` (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_ch_exp
#

INSERT INTO `wog_ch_exp` VALUES (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

#
# Table structure for table wog_character
#

DROP TABLE IF EXISTS `wog_character`;
CREATE TABLE `wog_character` (
  `ch_id` int(11) NOT NULL auto_increment,
  `ch_name` varchar(30) NOT NULL default '',
  `ch_str` char(3) NOT NULL default '0',
  `ch_agl` char(3) NOT NULL default '0',
  `ch_life` char(3) NOT NULL default '0',
  `ch_vit` char(3) NOT NULL default '0',
  `ch_smart` char(3) NOT NULL default '0',
  `ch_mstr` smallint(5) unsigned NOT NULL default '0',
  `ch_magl` smallint(5) unsigned NOT NULL default '0',
  `ch_msmart` smallint(5) unsigned NOT NULL default '0',
  `ch_mlv` smallint(5) unsigned NOT NULL default '0',
  `ch_mlife` smallint(5) unsigned NOT NULL default '0',
  `ch_au` char(3) NOT NULL default '0',
  `ch_be` char(3) NOT NULL default '0',
  `s_at` float unsigned NOT NULL default '1',
  `s_df` float unsigned NOT NULL default '1',
  `s_mat` float unsigned NOT NULL default '1',
  `s_mdf` float unsigned NOT NULL default '1',
  `s_agl` float unsigned NOT NULL default '1',
  `s_money` float unsigned NOT NULL default '1',
  `s_r` tinyint(2) unsigned NOT NULL default '0',
  `s_o` tinyint(2) unsigned NOT NULL default '0',
  `s_s` tinyint(2) unsigned NOT NULL default '0',
  `s_a` tinyint(2) unsigned NOT NULL default '0',
  `s_m_at` float unsigned NOT NULL default '1',
  `s_m_df` float unsigned NOT NULL default '1',
  `s_m_mdf` float unsigned NOT NULL default '1',
  `s_m_mat` float unsigned NOT NULL default '1',
  `s_m_agl` float unsigned NOT NULL default '1',
  `s_hp` float unsigned NOT NULL default '0',
  PRIMARY KEY  (`ch_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_character
#

INSERT INTO `wog_character` VALUES (6,'戰士','1,4','0,1','0,2','0,1','0,1',0,0,0,1,0,'0,1','0,1',1,1.2,1,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (7,'術士','0,1','0,1','0,2','0,1','1,4',0,0,0,1,0,'0,1','0,2',1,1,1.2,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (8,'盜賊','0,3','1,3','0,2','0,1','0,1',0,0,0,1,0,'0,1','0,1',1,1,1,1,1,1.2,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (9,'武道家','1,4','0,2','0,2','0,1','0,1',20,10,10,10,0,'0,1','0,1',1,1,1,1,1,1,0,0,10,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (10,'法師','0,2','1,2','0,2','0,1','1,4',8,10,20,10,0,'0,1','1,2',1,1,1,1,1,1,0,0,0,0,1,1,0.8,1,1,0);
INSERT INTO `wog_character` VALUES (11,'弓箭手','1,3','1,3','0,2','0,1','1,2',15,20,10,10,0,'0,1','0,1',1,1,1,1,1,1,10,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (12,'見習騎士','1,3','1,2','1,2','0,2','0,2',30,15,10,15,0,'0,1','0,1',1,1,1,1,1,1,5,5,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (13,'上乘射手','1,3','2,3','0,3','0,2','1,2',29,45,0,25,0,'0,2','0,2',1,1,1,1,1,1,0,0,0,3,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (14,'祭師','0,2','1,3','0,2','0,2','2,4',0,28,51,25,0,'0,2','1,3',1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0.1);
INSERT INTO `wog_character` VALUES (15,'武技長','2,4','0,3','1,3','1,2','0,2',52,28,0,25,0,'0,2','0,1',1.2,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (16,'殺手','1,3','2,4','1,2','0,2','1,2',40,78,28,52,0,'0,2','0,2',1,1,1,1,1,1,0,10,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (17,'巫師','0,2','1,3','0,2','0,2','2,5',28,30,80,52,0,'0,2','1,3',1,1,1.2,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (18,'鬥士','2,5','0,3','1,3','1,3','0,2',84,38,0,52,90,'0,2','0,1',1,1,1,1,1,1,0,0,0,0,1,0.8,1,1,1,0);
INSERT INTO `wog_character` VALUES (19,'遊俠','2,3','2,3','0,2','0,2','1,3',91,101,50,85,0,'0,3','0,3',1,1,1,1,1,1,0,0,0,0,1,1,1,1,0.8,0);
INSERT INTO `wog_character` VALUES (20,'妖師','0,3','1,3','1,2','1,2','2,5',30,70,110,85,0,'0,3','1,3',1,1,1,1,1,1,0,0,0,0,1,1,1,0.8,1,0);
INSERT INTO `wog_character` VALUES (21,'勇者','2,3','2,3','1,3','2,2','1,2',350,350,350,250,350,'1,4','1,3',1.1,1.1,1.1,1.1,1.1,1,0,0,0,1,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (22,'神偷','1,4','2,5','1,2','1,2','1,3',120,180,80,130,90,'1,2','0,3',1,1,1,1,1,1,20,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (23,'主教','1,2','1,4','1,2','1,3','2,4',70,80,180,130,70,'0,3','1,4',1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0.15);
INSERT INTO `wog_character` VALUES (24,'領主','2,6','0,3','1,4','2,3','1,2',180,120,70,130,160,'1,2','0,3',1,1,1,1,1,1,0,0,0,0,0.8,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (25,'傳奇舞者','1,4','2,5','1,2','1,2','1,4',180,300,180,260,180,'2,4','1,4',1,1,1,1,1,1,10,0,0,2,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (26,'煉術士','1,3','1,3','1,2','1,4','2,4',167,180,253,185,167,'0,4','1,4',1,1,1,1.2,1,1,0,0,0,0,1,1,1,1,1,0.1);
INSERT INTO `wog_character` VALUES (27,'重戰士','2,7','0,2','1,4','2,4','0,2',270,200,150,185,255,'0,2','0,2',1,1.2,1,1.2,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (28,'聖騎士','2,6','1,3','1,3','1,4','1,2',550,400,300,320,520,'0,4','1,4',1,1,1,1,1,1,0,0,15,0,1,1,1,1,1,0.02);
INSERT INTO `wog_character` VALUES (29,'上忍','2,4','2,6','1,3','1,3','1,4',470,550,360,320,470,'1,3','1,2',1,1,1,1,1,1,20,20,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (30,'大賢者','1,2','2,3','1,3','1,4','2,7',200,390,600,320,350,'1,4','2,4',1,1,1,1,1,1,0,0,0,0,0.8,1,1,0.8,1,0);
INSERT INTO `wog_character` VALUES (31,'英雄','3,7','2,3','1,4','1,3','1,3',900,600,400,500,750,'1,4','0,3',1.2,1,1,1,1,1,15,0,0,1,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (32,'風魔','2,3','2,7','1,3','1,2','2,4',780,900,500,500,750,'1,2','1,3',1,1,1,1,1,1,0,100,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (33,'召喚師','1,4','2,5','1,2','1,3','3,7',350,500,900,500,480,'1,3','2,3',1,1,1.5,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (34,'龍魂','3,7','1,3','2,3','2,3','1,3',1600,1000,800,800,1400,'0,4','1,3',1.5,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (35,'精靈王','1,3','2,4','1,3','1,4','4,7',800,1000,1600,800,1000,'1,5','2,4',1,1.2,1,1.5,1,1,0,0,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (36,'傳說','2,5','3,6','1,4','1,2','1,4',1400,1400,1000,800,1200,'1,4','1,3',1,1,1,1,1.5,1,0,0,5,1,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (37,'準騎士','2,4','1,3','1,2','2,3','0,3',120,60,30,85,120,'0,2','0,2',1,1,1,1,1,1,10,10,0,0,1,1,1,1,1,0);
INSERT INTO `wog_character` VALUES (38,'中忍','2,4','2,4','1,3','1,2','1,3',180,270,180,185,180,'0,3','1,2',1,1,1,1,2,1,0,0,0,0,1,1,1,1,1,0);

#
# Table structure for table wog_cp
#

DROP TABLE IF EXISTS `wog_cp`;
CREATE TABLE `wog_cp` (
  `p_id` int(11) unsigned NOT NULL auto_increment,
  `p_birth` tinyint(3) unsigned NOT NULL default '0',
  `p_name` varchar(30) NOT NULL default '',
  `p_at` smallint(5) unsigned NOT NULL default '0',
  `p_df` smallint(5) unsigned NOT NULL default '0',
  `p_mat` smallint(5) unsigned NOT NULL default '0',
  `p_mdf` smallint(5) unsigned NOT NULL default '0',
  `p_s` tinyint(1) unsigned NOT NULL default '1',
  `p_url` varchar(100) NOT NULL default '',
  `p_homename` varchar(30) NOT NULL default '',
  `p_str` smallint(5) unsigned NOT NULL default '0',
  `p_life` smallint(5) unsigned NOT NULL default '0',
  `p_vit` smallint(5) unsigned NOT NULL default '0',
  `p_smart` smallint(5) unsigned NOT NULL default '0',
  `p_agl` smallint(5) unsigned NOT NULL default '0',
  `p_hp` int(11) unsigned NOT NULL default '0',
  `p_luck` tinyint(4) unsigned NOT NULL default '0',
  `p_sat_name` varchar(250) default NULL,
  `p_hpmax` int(10) unsigned NOT NULL default '0',
  `p_win_total` int(10) unsigned NOT NULL default '0',
  `p_lv` int(10) unsigned NOT NULL default '0',
  `a_id` smallint(5) unsigned NOT NULL default '0',
  `d_body_id` smallint(5) unsigned NOT NULL default '0',
  `d_foot_id` smallint(5) unsigned NOT NULL default '0',
  `d_hand_id` smallint(5) unsigned NOT NULL default '0',
  `d_head_id` smallint(5) unsigned NOT NULL default '0',
  `d_item_id` smallint(5) unsigned NOT NULL default '0',
  `p_sex` tinyint(1) NOT NULL default '0',
  `p_money` int(10) unsigned NOT NULL default '0',
  `p_exp` int(11) NOT NULL default '0',
  `p_nextexp` int(11) NOT NULL default '0',
  `p_win` int(10) unsigned NOT NULL default '0',
  `p_lost` int(10) unsigned NOT NULL default '0',
  `i_img` smallint(3) NOT NULL default '0',
  `p_img_url` varchar(200) NOT NULL default '',
  `p_img_set` tinyint(3) unsigned NOT NULL default '0',
  `ch_id` tinyint(4) unsigned NOT NULL default '0',
  `p_pid` int(10) NOT NULL default '0',
  `p_au` smallint(5) unsigned NOT NULL default '0',
  `p_be` smallint(5) unsigned NOT NULL default '0',
  `p_ch_s_id` tinyint(2) unsigned NOT NULL default '0',
  `p_g_id` int(10) unsigned NOT NULL default '0',
  `p_place` tinyint(3) unsigned NOT NULL default '0',
  `p_cdate` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_cp
#

INSERT INTO `wog_cp` VALUES (1,0,'test',9,9,9,9,1,'http://www.2233.idv.tw/','WOG',9,9,8,9,9,45,0,'',45,1,1,0,0,0,0,0,0,2,8000,0,1000,1,1,1,'',0,6,1,8,8,0,0,1,1148147535);

#
# Table structure for table wog_df
#

DROP TABLE IF EXISTS `wog_df`;
CREATE TABLE `wog_df` (
  `d_id` int(11) NOT NULL auto_increment,
  `d_df` smallint(5) NOT NULL default '0',
  `d_mdf` smallint(5) NOT NULL default '0',
  `d_agl` smallint(5) NOT NULL default '0',
  `d_mstr` smallint(5) NOT NULL default '0',
  `d_magl` smallint(5) NOT NULL default '0',
  `d_msmart` smallint(5) NOT NULL default '0',
  `ch_id` int(11) NOT NULL default '0',
  `d_money` int(11) NOT NULL default '10',
  `d_name` varchar(96) NOT NULL default '',
  `d_type` tinyint(1) unsigned NOT NULL default '0',
  `d_at` smallint(4) NOT NULL default '0',
  `d_mat` smallint(4) NOT NULL default '0',
  `d_dbst` tinyint(1) NOT NULL default '0',
  `d_g_hp` int(10) unsigned NOT NULL default '0',
  `d_g_str` tinyint(3) unsigned NOT NULL default '0',
  `d_g_smart` tinyint(3) unsigned NOT NULL default '0',
  `d_g_agl` tinyint(3) unsigned NOT NULL default '0',
  `d_g_life` tinyint(3) unsigned NOT NULL default '0',
  `d_g_vit` tinyint(3) unsigned NOT NULL default '0',
  `d_g_au` tinyint(3) unsigned NOT NULL default '0',
  `d_g_be` tinyint(3) unsigned NOT NULL default '0',
  `d_g_exp` int(10) unsigned NOT NULL default '0',
  `d_g_bag` tinyint(3) unsigned NOT NULL default '0',
  `d_s` tinyint(3) unsigned default NULL,
  `d_lv` tinyint(3) unsigned NOT NULL default '0',
  `ch_pro` int(10) unsigned NOT NULL default '0',
  `d_send` tinyint(5) unsigned NOT NULL default '0',
  `d_vip` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`d_id`),
  UNIQUE KEY `d_name` (`d_name`),
  KEY `d_lv` (`d_lv`)
) TYPE=MyISAM;

#
# Dumping data for table wog_df
#

INSERT INTO `wog_df` VALUES (1,3,1,2,0,0,0,0,18,'布衣',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (2,0,0,5,0,0,0,0,14,'木刀',0,15,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (3,0,0,8,0,0,0,0,14,'木弓',0,11,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (4,0,0,5,0,0,0,0,14,'木杖',0,0,15,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (5,0,0,7,0,0,0,0,89,'小刀',0,18,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (6,0,0,6,8,8,8,0,103,'精緻木杖',0,0,18,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (7,0,0,3,19,10,8,0,269,'彎刀',0,21,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (8,0,0,1,28,15,8,0,429,'短劍',0,26,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (9,0,0,0,38,17,8,0,752,'長劍',0,30,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (10,0,0,8,44,21,8,0,1397,'火熱彎刀',0,37,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (11,0,0,6,46,23,8,0,1693,'雙頭劍',0,44,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (12,0,0,0,54,25,8,0,1988,'強化之劍',0,50,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (13,0,0,12,71,31,16,0,3922,'雷鳴劍',0,70,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (14,0,0,0,61,46,16,0,4003,'火鳴劍',0,76,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (15,5,0,10,86,46,16,0,9697,'卡西奈特劍',0,88,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (16,0,20,12,71,36,91,0,4863,'魔法劍',0,75,75,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (17,10,10,21,127,41,28,0,23264,'陶瓷劍',0,129,20,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (18,25,0,-15,161,16,16,0,10,'亞克鐵鎚',0,165,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (19,10,5,0,196,46,16,0,81291,'怒之劍',0,174,80,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (20,10,0,0,161,16,16,0,46502,'重劍',0,149,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (21,15,15,15,213,56,80,0,137974,'龍劍',0,180,165,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (22,10,0,10,256,70,16,0,400381,'狂暴劍',0,260,100,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (23,0,5,5,8,8,20,0,564,'魔法杖',0,0,23,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (24,0,6,5,8,8,51,0,402,'魔彈之杖',0,0,30,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (25,0,0,10,8,8,56,0,1075,'雷之杖',0,0,37,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (26,0,5,0,8,8,61,0,1371,'治療之杖',0,0,44,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (27,0,0,6,8,8,61,0,1693,'毒之杖',0,0,61,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (28,5,5,12,10,10,76,0,2498,'聖魔杖',0,0,66,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (29,10,0,0,16,16,86,0,4029,'可巴斯之杖',0,0,78,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (30,0,10,12,16,16,93,0,7039,'妖精之杖',0,0,86,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (31,0,0,0,16,16,106,0,4782,'永恆之杖',0,25,96,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (32,12,10,0,16,16,126,0,8005,'聖光杖',0,35,130,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (33,0,0,0,16,16,149,0,15419,'精靈之力',0,0,133,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (34,0,10,10,16,16,179,0,27832,'火球術',0,0,152,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (35,10,0,0,16,16,204,0,10,'冰柱術',0,0,159,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (36,0,0,15,16,16,207,0,49268,'電光球',0,0,184,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (37,0,10,0,16,16,249,0,94185,'火焰術',0,0,200,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (38,10,0,0,16,16,260,0,202715,'冰雪術',0,0,237,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (39,0,0,8,8,12,8,0,254,'迴旋刀',0,19,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (40,0,0,10,8,16,8,0,358,'火焰弓箭',0,23,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (41,0,0,12,8,20,8,0,546,'俠盜弓箭',0,23,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (42,0,0,16,16,28,10,0,832,'艾魯夫之弓',0,28,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (43,0,10,25,12,36,12,0,1210,'忍者刀',0,35,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (44,0,0,30,16,42,16,0,1881,'神經系毒針',0,42,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (45,0,0,35,30,41,16,0,2255,'風魔十字鏢',0,51,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (46,0,0,31,36,48,16,0,2659,'格林機槍',0,64,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (47,0,0,40,36,58,16,0,4727,'十字手裡劍',0,69,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (48,12,5,51,56,74,16,0,8113,'風車',0,80,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (49,0,15,40,31,89,21,0,15609,'蝶形刀',0,92,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (50,10,10,60,36,112,26,0,28368,'虎牙',0,130,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (51,10,0,70,41,147,31,0,32667,'金屬之爪',0,133,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (52,10,10,70,66,172,56,0,74306,'鑽石之爪',0,147,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (53,10,10,70,101,197,81,0,128840,'水晶之爪',0,164,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (54,10,10,77,156,237,116,0,174777,'白金之爪',0,190,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (55,10,10,78,206,227,106,0,240325,'帝王之爪',0,220,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (56,0,10,90,266,239,106,0,319844,'究極心爪',0,255,50,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (57,0,10,102,301,301,121,0,563770,'靈爪',0,280,100,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (58,15,15,110,351,351,141,0,874856,'神爪',0,300,120,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (59,10,0,0,14,8,8,0,298,'一般鎧甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (60,18,0,0,20,12,8,0,564,'連鎖鎧甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (61,28,0,0,31,18,8,0,859,'鋼之鎧甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (62,37,0,0,41,21,8,0,1585,'刺骨鎧甲',2,10,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (63,49,0,0,48,26,8,0,1988,'甲型防具',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (64,60,0,5,76,31,16,0,2713,'戰神鎧甲',2,10,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (65,70,0,5,96,34,16,0,4996,'白金鎧甲',2,5,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (66,85,0,0,127,51,26,0,14667,'聖戰甲',2,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (67,108,0,0,152,61,16,0,22351,'昇龍聖甲冑',2,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (68,125,0,0,213,71,16,0,33285,'源氏之鎧甲',2,15,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (69,138,0,5,284,76,16,0,56737,'破龍盔甲',2,15,15,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (70,152,0,10,359,76,36,0,110842,'次元之鎧',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (71,5,10,5,8,8,15,0,312,'魔法袍',2,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (72,6,19,7,8,8,21,0,484,'黑色道袍',2,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (73,5,28,9,8,20,26,0,779,'輕盈之服',2,0,8,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (74,9,39,8,8,26,36,0,1290,'青光之服',2,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (75,10,48,13,8,26,41,0,1757,'魔法師之戰袍',2,0,16,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (76,10,60,20,8,26,66,0,2364,'風之道袍',2,0,15,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (77,10,75,0,8,26,89,0,4324,'聖光袍',2,0,20,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (78,10,95,10,16,26,112,0,15878,'滅魔聖袍',2,0,20,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (79,10,116,10,16,36,164,0,25951,'榮耀披風',2,0,15,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (80,10,132,15,16,36,219,0,44433,'神農服',2,0,15,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (81,20,150,20,16,51,284,0,96603,'炎帝之服',2,0,20,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (82,20,168,15,16,51,344,0,121936,'貴族之氣',2,0,20,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (83,180,50,10,420,326,200,0,286532,'幻想之元',2,20,20,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (84,50,190,15,200,354,489,0,368334,'古代魔服',2,0,30,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (85,5,5,5,12,10,8,0,283,'獵人衣裝',2,2,2,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (86,8,8,5,16,16,8,0,429,'盜賊服',2,2,2,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (87,15,7,10,16,28,12,0,752,'擬態服',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (88,20,7,15,26,31,16,0,1210,'低忍服',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (89,28,10,15,31,41,16,0,1693,'中忍服',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (90,40,15,15,41,52,16,0,2632,'上級忍服',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (91,55,20,20,46,66,26,0,3572,'空想服',2,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (92,68,23,20,73,81,36,0,5614,'風魔忍服',2,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (93,75,30,25,91,106,40,0,6663,'迷霧輕甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (94,88,25,25,119,106,16,0,16548,'神射輕甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (95,102,25,28,168,172,50,0,40806,'疾風輕甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (96,132,25,30,190,195,52,0,69496,'音速輕甲',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (97,145,30,25,241,262,56,0,109498,'自然護衣',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (98,165,25,32,356,375,70,0,162742,'神偷袍',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (99,5,5,5,8,8,8,0,149,'學徒帽',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (100,8,0,0,12,12,12,0,209,'冒險者帽',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (101,13,3,0,16,16,10,0,484,'戰士頭盔',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (102,21,3,0,31,26,16,0,564,'武術頭巾',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (103,10,16,0,16,16,34,0,698,'極魔帽',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (104,32,10,3,41,31,16,0,1451,'藍天頭盔',1,5,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (105,22,35,6,21,26,46,0,1745,'尖頂魔帽',1,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (106,25,25,15,36,36,36,0,2095,'音速頭巾',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (107,41,35,10,31,46,61,0,2928,'羽毛帽',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (108,52,30,0,48,36,36,0,9213,'貴族帽',1,5,5,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (109,67,51,9,79,51,46,0,22593,'皇家帽',1,8,6,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (110,85,70,0,131,51,74,0,36964,'龍頭盔',1,10,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (111,97,80,5,170,51,74,0,62486,'破龍之盔',1,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (112,108,70,0,208,36,59,0,122929,'騎士盔',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (113,95,115,15,269,180,285,0,260205,'緞帶',1,15,15,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (114,135,90,0,309,76,94,0,298890,'王者之冠',1,15,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (115,145,80,0,329,76,76,0,572098,'霸者之冠',1,15,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (116,160,120,15,366,260,174,0,673912,'戰神之盔',1,15,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (117,175,165,15,410,465,350,0,1081171,'忍術頭巾',1,15,15,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (118,165,180,20,485,480,483,0,10,'究極緞帶',1,20,20,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (119,3,3,0,8,8,8,0,75,'旅人手套',3,3,2,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (120,0,6,2,12,12,16,0,89,'魔法手套',3,0,2,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (121,8,0,0,21,21,12,0,402,'戰士護手',3,3,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (122,12,0,2,28,16,16,0,532,'騎士護手',3,2,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (123,3,10,0,16,16,31,0,484,'祭師護手',3,0,5,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (124,12,15,0,21,16,38,0,859,'魔力盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (125,27,10,0,41,16,16,0,1021,'圓桌盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (126,36,25,0,51,36,36,0,1826,'龍磷盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (127,30,40,2,20,20,20,0,10,'火焰護手',3,0,5,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (128,56,67,5,51,51,56,0,4727,'鬼力手甲',3,5,5,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (129,60,50,8,71,78,50,0,4513,'忍者護手',3,6,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (130,68,76,0,96,51,36,0,6877,'反射盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (131,70,95,8,71,46,114,0,13863,'賢者手套',3,5,15,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (132,95,50,0,135,46,36,0,25413,'霸者護手',3,10,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (133,102,70,0,163,100,132,0,41800,'皇家盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (134,115,65,0,197,120,46,0,96603,'戰神護手',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (135,120,90,15,206,154,124,0,152347,'暗殺手套',3,10,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (136,105,140,0,219,180,280,0,238446,'精靈盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (137,140,110,0,299,206,215,0,412794,'冰封護手',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (138,160,150,10,385,385,385,0,865183,'究極護手',3,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (139,3,2,5,8,8,8,0,68,'冒險靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (140,5,5,6,12,12,12,0,155,'皮靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (141,9,6,2,26,16,12,0,328,'鐵靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (142,16,10,6,36,16,16,0,643,'戰士靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (143,12,15,7,16,26,36,0,671,'魔法靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (144,27,15,8,41,31,16,0,1101,'騎士靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (145,20,25,8,16,31,41,0,1210,'祭師靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (146,35,20,10,46,41,26,0,2175,'武術靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (147,45,40,15,46,51,36,0,2605,'忍術靴',4,5,5,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (148,50,45,10,51,61,16,0,4863,'射手靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (149,68,40,0,81,26,26,0,8086,'重裝靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (150,60,55,30,66,36,56,0,20659,'獸皮靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,2,0,0,0);
INSERT INTO `wog_df` VALUES (151,80,50,40,134,26,26,0,33957,'鋼靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (152,80,75,55,119,66,89,0,10,'水晶靴',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (153,105,120,60,173,156,184,0,65871,'火靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (154,125,100,70,268,245,236,0,102110,'龍之靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (155,135,150,80,209,145,215,0,159465,'古代靴',4,0,10,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (156,150,150,80,289,266,289,0,215235,'傳說靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (157,165,165,90,349,349,349,0,506818,'妖靴',4,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (158,170,180,100,459,459,459,0,914076,'究極靴',4,10,10,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (159,0,0,10,380,250,100,0,1304681,'死神之槍',0,401,120,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (160,0,10,10,410,260,150,0,1611845,'水晶劍',0,410,150,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (161,0,20,30,470,310,300,0,2149126,'勇者之劍',0,451,200,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (162,0,0,35,380,420,200,0,1746165,'天使弓箭',0,386,160,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (163,0,0,10,500,400,250,0,3358010,'惡魔之爪',0,486,180,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (164,0,0,10,150,150,290,0,161185,'時光魔笛',0,160,267,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (165,10,0,-30,520,350,100,0,2820729,'鬼神斧頭',0,462,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (166,0,10,0,580,420,160,0,4163932,'艾魯夫鐵鎚',0,547,100,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (167,0,0,10,520,520,280,0,4029611,'銀河之牙',0,522,120,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (168,0,0,10,580,580,200,0,4835533,'虎式拳套',0,582,160,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (169,10,10,10,630,600,350,0,7790583,'神秘之刀',0,691,200,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (170,0,20,10,100,250,330,0,268640,'狂火術',0,0,374,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (171,0,20,10,120,260,360,0,335801,'冰凍術',0,0,404,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (172,0,20,0,150,300,390,0,391685,'狂雷術',0,0,392,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (173,0,20,0,180,300,410,0,1034268,'巨震術',0,0,442,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (174,0,0,0,360,380,200,0,1680778,'猛刺之矛',0,430,100,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (175,0,0,0,660,620,480,0,10208350,'封印之劍',0,731,210,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (176,0,0,0,120,350,500,0,3720675,'超重力',0,0,523,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (177,0,0,0,200,420,610,0,10544151,'時間衝擊',0,0,721,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (178,0,0,0,200,520,700,0,18536214,'消滅術',0,0,871,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (179,0,0,0,250,650,850,0,30356409,'融合術',0,0,910,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (180,0,0,20,700,690,300,0,18267572,'天使之矛',0,861,210,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (181,0,0,50,1100,900,400,0,32236894,'天之叢雲',0,1070,300,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (182,0,0,30,800,800,350,0,22297184,'夜叉',0,920,250,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (183,0,0,0,0,0,0,0,1405,'金幣',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (184,0,0,0,0,0,0,0,7021,'黃金',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (185,0,0,0,0,0,0,0,14042,'水晶',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (186,0,0,0,0,0,0,0,1405,'鬥志指輪',5,5,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (187,0,0,0,0,0,0,0,1405,'智慧指輪',5,0,5,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (188,0,0,8,0,0,0,0,1755,'疾風指輪',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (189,0,0,0,0,0,0,0,7021,'領主徽章',5,15,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (190,0,0,0,0,0,0,0,7021,'主教徽章',5,0,15,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (191,0,0,20,0,0,0,0,13339,'音速斗篷',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (192,10,0,0,0,0,0,0,5617,'龍磷',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (193,0,10,0,0,0,0,0,5617,'魔法水',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (194,0,0,0,20,20,20,0,35104,'英雄徽章',5,50,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (195,0,0,0,20,20,20,0,35104,'召喚師徽章',5,0,50,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (196,30,60,0,20,20,20,33,140415,'幻獸羽毛',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (197,0,0,30,800,1100,500,0,28207282,'圓月輪',0,1030,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (198,0,0,35,1250,1400,600,0,38146990,'風魔手裡劍',0,1230,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (199,0,0,0,1400,1100,650,0,42445243,'陸奧守吉行',0,1350,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (200,0,0,0,1600,1500,700,0,10,'封魔太刀',0,1500,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (201,0,0,0,300,700,1000,0,26864077,'召喚 路行鳥',0,0,1000,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (202,0,0,0,300,700,1200,0,40296117,'召喚 伊弗利特',0,0,1300,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (203,0,0,0,450,700,1400,0,10,'召喚 希瓦',0,0,1500,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (204,0,0,0,0,0,0,0,352,'錢包',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (205,0,0,18,100,60,30,0,12638,'白龍矛',0,192,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (206,0,0,0,20,30,80,0,11373,'魔女之書',0,0,180,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (207,0,0,0,0,0,0,0,3511,'靈術符',5,0,8,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (208,0,8,0,0,0,0,0,3511,'妖精之水',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (213,0,0,0,500,500,1800,0,10,'召喚 亞歷山大',0,0,1800,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (214,0,0,0,600,600,2200,0,10,'召喚 澳丁',0,0,2200,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (215,0,10,20,300,300,140,0,10,'魔鞭',0,326,180,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (216,0,25,10,12,12,12,0,10,'鬼牌',5,0,5,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (217,40,65,15,25,35,100,0,10,'鬥法羽衣',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (218,0,0,30,1000,1000,600,0,10,'名刀 不知火',0,1100,320,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (219,0,0,0,15,15,15,0,8426,'戰神徽章',5,30,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (220,0,0,0,15,15,15,0,8426,'賢者徽章',5,0,30,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (222,186,0,0,530,215,150,0,10,'黃金之鎧',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (223,0,0,0,0,0,0,0,8,'50 hp回復劑',5,0,0,0,50,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (224,0,0,0,0,0,0,0,44,'300 hp回復劑',5,0,0,0,300,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (225,0,0,0,0,0,0,0,155,'1500 hp回復劑',5,0,0,0,1500,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (226,0,0,0,0,0,0,0,313,'4500 hp回復劑',5,0,0,0,4500,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (227,0,0,0,0,0,0,0,738,'10000 hp回復劑',5,0,0,0,10000,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (228,0,0,0,0,0,0,0,1290,'20000 hp回復劑',5,0,0,0,20000,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (229,30,120,0,30,10,70,0,10,'貴婦髮帶',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (230,20,480,0,10,0,500,0,10,'星星髮夾',1,0,30,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (231,450,-80,30,3200,0,0,0,10,'噬血頭巾',1,60,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (232,250,170,0,580,480,420,0,1611845,'領導者冠',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (233,100,270,0,100,100,600,0,1558117,'天使髮圈',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (234,90,130,230,100,600,100,0,1665572,'時間頭巾',1,30,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (235,250,30,0,800,300,150,0,564145,'魔神之鎧',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (236,410,-100,30,1100,200,0,0,805921,'噬血之鎧',2,60,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (237,80,260,80,100,100,760,0,591009,'二極衣',2,0,20,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (238,100,120,200,300,800,300,0,671602,'時間外套',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (239,210,120,0,600,350,250,0,1069190,'動力盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (240,60,220,65,200,200,630,0,1061131,'幻力盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (241,60,80,180,220,620,100,0,1101426,'時間手套',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (242,286,100,0,682,200,0,0,1249180,'魔神靴',4,45,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (243,220,160,100,520,380,300,0,1128291,'亞崙靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (244,80,300,80,100,100,700,0,1249180,'魔導靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (245,30,100,290,260,720,260,0,1316339,'時間靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (246,180,180,190,600,600,600,0,10,'火焰輪',4,45,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (247,0,30,100,120,800,320,0,224665,'路行鳥披風',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (248,0,80,0,100,250,800,0,210622,'智慧耳環',5,0,80,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (249,0,0,0,0,0,0,0,1915,'35000 hp回復劑',5,0,0,0,35000,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (250,0,0,0,1900,450,300,0,48355339,'末日之劍',0,2000,0,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (251,0,0,100,560,2200,100,0,45668932,'淬紅暗器',0,1850,0,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (252,0,0,0,100,300,2000,0,51041748,'冰火雙重',0,0,2000,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (253,0,0,1000,0,1800,0,36,10,'Jordan鞋',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,17500,0,0);
INSERT INTO `wog_df` VALUES (254,200,-100,-100,2350,0,0,0,59100971,'逆天之斧',0,2500,0,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (255,0,0,0,2000,2000,1300,0,83278640,'名廚菜刀',0,2750,0,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (256,0,0,0,500,1000,2200,0,85965048,'神聖之光',0,0,2900,0,0,0,0,0,0,0,0,0,0,0,NULL,7,0,0,0);
INSERT INTO `wog_df` VALUES (257,0,0,200,800,2000,1000,0,10,'龍之爆彈',0,2350,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (258,0,0,0,0,0,0,0,738,'捕捉器',5,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (259,0,0,0,0,0,0,0,2638,'50000 hp回復劑',5,0,0,0,50000,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (260,0,0,0,0,0,0,0,3569,'80000 hp回復劑',5,0,0,0,80000,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (261,50,50,120,300,500,150,38,10,'小烏丸',0,1250,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,14000,0,0);
INSERT INTO `wog_df` VALUES (262,80,0,0,600,200,100,24,10,'流螢劍',0,1420,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,0,0);
INSERT INTO `wog_df` VALUES (263,10,10,0,300,150,100,37,247949,'薙刀',0,625,100,0,0,0,0,0,0,0,0,0,0,0,NULL,4,10500,0,0);
INSERT INTO `wog_df` VALUES (264,0,180,0,100,500,1000,30,29845726,'聖龍黑魔杖',0,0,1680,0,0,0,0,0,0,0,0,0,0,0,NULL,6,14000,0,0);
INSERT INTO `wog_df` VALUES (265,10,30,300,460,900,700,25,10,'羽扇',0,2130,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,14000,0,0);
INSERT INTO `wog_df` VALUES (266,180,180,0,1500,1500,1500,21,10,'龍神王刃',0,3400,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,0,0);
INSERT INTO `wog_df` VALUES (267,180,300,0,450,500,800,0,1584120,'水鏡之盾',3,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (268,580,0,0,1400,800,500,0,1205308,'星辰之鎧',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (269,100,520,0,400,600,1320,0,1136434,'月白之袍',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (270,0,0,0,0,0,0,20,10,'骨十字之徽章',5,0,80,1,0,0,0,0,0,0,0,0,0,0,NULL,0,7000,0,0);
INSERT INTO `wog_df` VALUES (271,380,150,150,800,1300,500,0,1308621,'蒼龍之鎧',2,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (272,300,400,0,0,0,900,0,2601935,'精靈環',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (273,50,20,18,50,70,50,0,27550,'微風帽',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (274,60,100,10,70,50,90,0,33672,'魅力面罩',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (275,280,350,0,0,0,800,0,2448880,'魔法眼鏡',1,0,30,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (276,100,100,310,0,800,0,0,2525407,'月光面罩',1,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (277,100,300,0,0,0,700,0,2295825,'博士帽',1,0,80,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (278,100,100,0,800,0,0,0,10,'攻擊頭巾',1,90,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (279,80,150,360,0,850,0,0,10,'兔子髮圈',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (280,0,0,0,0,0,5100,0,10,'究極水晶',0,0,3800,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (281,0,0,600,0,5000,0,0,10,'名刀 正宗',0,3000,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (282,0,0,0,5200,0,0,0,10,'流星拳套',0,4100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (283,0,0,0,0,0,0,0,10,'力量之水',6,3,0,1,0,3,0,0,0,0,0,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (284,0,0,3,0,0,0,0,10,'速度之水',6,0,0,1,0,0,0,3,0,0,0,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (285,0,0,0,0,0,0,0,10,'智力之水',6,0,3,1,0,0,3,0,0,0,0,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (286,0,0,0,0,0,0,0,10,'生命之水',6,0,0,1,0,0,0,0,3,0,0,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (287,3,0,0,0,0,0,0,10,'體質之水',6,0,0,1,0,0,0,0,0,3,0,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (288,0,3,0,0,0,0,0,10,'信仰之水',6,0,0,1,0,0,0,0,0,0,0,3,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (289,0,0,0,0,0,0,0,10,'魅力之水',6,0,0,1,0,0,0,0,0,0,3,0,0,0,NULL,0,0,0,1);
INSERT INTO `wog_df` VALUES (290,0,0,60,0,120,0,0,22958,'神偷鞋',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (291,0,75,0,0,0,92,0,24871,'七色鞋',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,3,0,0,0);
INSERT INTO `wog_df` VALUES (292,50,0,0,180,0,0,0,57396,'怒神靴',4,30,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (293,60,0,0,250,0,0,0,114791,'鬥氣靴',4,50,0,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (294,0,50,0,0,0,160,0,61222,'浮雲鞋',4,0,35,0,0,0,0,0,0,0,0,0,0,0,NULL,4,0,0,0);
INSERT INTO `wog_df` VALUES (295,0,80,0,0,0,280,0,267846,'天罰鞋',4,0,75,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (296,30,0,130,120,250,0,0,306111,'暗殺鞋',4,20,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (297,60,0,0,290,0,0,0,298457,'冰刃靴',4,80,0,0,0,0,0,0,0,0,0,0,0,0,NULL,5,0,0,0);
INSERT INTO `wog_df` VALUES (298,50,0,230,0,500,0,0,1033121,'馭風靴',4,0,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (299,50,120,0,0,0,600,0,1033121,'魔剎靴',4,0,100,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (300,90,50,0,600,0,0,0,1033121,'染血靴',4,110,0,0,0,0,0,0,0,0,0,0,0,0,NULL,6,0,0,0);
INSERT INTO `wog_df` VALUES (301,80,180,20,0,0,1200,0,10,'封神鞋',4,0,170,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (302,50,50,320,500,1000,0,0,10,'步雲靴',4,50,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (303,150,80,0,1200,0,0,0,10,'無量腿甲',4,180,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (304,300,300,180,0,300,300,25,10,'女王鞋',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,0,0);
INSERT INTO `wog_df` VALUES (305,400,500,0,1500,700,2700,0,10,'水晶王盾',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (306,0,0,0,0,0,0,0,10,'鋼鐵',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (307,0,0,0,0,0,0,0,10,'魔樹枝',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (308,55,30,0,30,16,16,0,10,'鋼鐵圓桌盾',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (309,80,120,0,50,50,80,0,10,'喚龍盾',3,0,30,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (310,700,400,0,3500,700,600,0,10,'冥王之盾',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (311,450,300,0,2700,1400,300,0,10,'神騎士護手',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (312,300,450,0,200,350,2100,0,10,'大賢者手套',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (313,150,200,0,200,200,500,0,10,'火靈盾',3,0,30,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (314,70,20,10,200,100,50,0,10,'攻擊護手',3,80,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (315,0,0,0,0,0,0,0,10,'天使之息',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (316,0,0,0,0,0,0,0,10,'火砂',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (317,0,0,70,300,450,300,25,10,'月下美人',0,800,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,10500,1,0);
INSERT INTO `wog_df` VALUES (318,0,0,0,320,100,100,18,10,'落櫻',0,620,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,8750,1,0);
INSERT INTO `wog_df` VALUES (319,0,0,0,0,0,0,18,10,'戰狂之魄',5,120,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,0,0);
INSERT INTO `wog_df` VALUES (320,0,0,0,0,0,0,26,10,'冰漩之眼',5,0,160,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,0,0);
INSERT INTO `wog_df` VALUES (321,0,0,180,0,0,0,22,10,'盜風魂',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,0,0);
INSERT INTO `wog_df` VALUES (322,150,170,90,200,200,230,0,10,'烈火靴',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (323,0,0,0,0,0,0,0,100,'時鐘',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (324,0,0,0,0,0,3800,0,10,'時空侵蝕',0,0,3500,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (325,250,250,250,0,0,0,21,10,'勇者魂',5,300,150,1,0,0,0,0,0,0,0,0,0,0,NULL,0,28000,1,0);
INSERT INTO `wog_df` VALUES (326,0,0,0,0,0,0,33,10,'召喚 巴哈姆特',0,0,4100,1,0,0,0,0,0,0,0,0,0,0,NULL,0,28000,1,0);
INSERT INTO `wog_df` VALUES (327,0,0,0,0,0,0,0,10,'召喚石',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (328,0,0,0,0,0,0,0,10,'高級召喚書',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (329,0,0,0,0,0,0,0,100,'巨人毛髮',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (330,0,0,0,0,0,0,0,100,'狼牙齒',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (331,0,0,0,0,0,0,0,100,'蜘蛛絲',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (332,0,0,0,0,0,0,0,100,'水晶碎片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (333,0,0,0,0,0,0,0,100,'硬殼',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (334,100,100,260,0,0,0,16,10,'惡魔之護印',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,12250,1,0);
INSERT INTO `wog_df` VALUES (335,0,0,0,0,0,0,31,10,'破軍王戟',0,4100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,28000,1,0);
INSERT INTO `wog_df` VALUES (336,0,0,0,0,0,0,0,100,'巴哈姆特之魂',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (337,0,0,0,0,0,0,0,150,'瑪那樹葉',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (338,0,0,0,0,0,0,0,150,'天堂羽毛',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (339,0,0,0,0,0,0,0,150,'古書',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (340,0,0,0,0,0,0,0,150,'破舊卡片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (341,0,0,0,0,0,0,0,50,'生鏽鐵釘',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (342,0,0,0,0,0,0,0,200,'白色布料',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (343,0,0,0,0,0,0,0,200,'魔法染料',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (344,0,0,0,0,0,0,0,7000,'鑽石',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (345,0,0,0,0,0,0,0,200,'強化鋼鐵',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (346,300,380,0,1000,1500,3900,0,10,'邪眼面具',1,0,90,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (347,520,400,0,4200,3000,2500,0,10,'鑽石頭盔',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (348,200,200,400,1500,3900,2000,0,10,'瑪那頭巾',1,30,30,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (349,100,100,150,0,0,0,13,10,'白羽帽',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,14000,1,0);
INSERT INTO `wog_df` VALUES (350,120,200,180,0,0,0,13,10,'蜘蛛裝',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,14000,1,0);
INSERT INTO `wog_df` VALUES (351,350,100,0,0,0,0,15,10,'獸人服',2,70,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,14000,1,0);
INSERT INTO `wog_df` VALUES (352,670,200,0,2300,0,0,0,10,'光之聖甲',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (353,350,100,0,2700,0,0,0,10,'反擊針胄',2,250,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (354,0,700,0,0,0,2900,0,10,'水晶袍',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (355,0,0,5,0,0,0,0,10,'風神珠',5,0,5,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (356,2,2,0,0,0,0,0,10,'雷神珠',5,5,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (357,0,0,0,0,0,0,0,10,'微晶片',5,2,2,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (358,0,0,0,0,0,0,0,10,'火藥',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (359,0,0,1200,0,0,0,32,10,'靈劍布都御魂',0,3200,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,28000,1,0);
INSERT INTO `wog_df` VALUES (360,0,0,1500,0,0,0,16,10,'鬼神心爪',0,2500,0,1,0,0,0,0,0,0,0,0,0,0,6,0,21000,1,0);
INSERT INTO `wog_df` VALUES (361,-300,0,-800,0,0,0,18,10,'冷月銀槍',0,4200,0,1,0,0,0,0,0,0,0,0,0,0,2,0,21000,1,0);
INSERT INTO `wog_df` VALUES (362,0,0,700,0,0,0,13,10,'聖十字短弓',0,3500,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,1,0);
INSERT INTO `wog_df` VALUES (363,0,0,2000,0,0,0,19,10,'喚龍之笛',0,1600,1400,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,1,0);
INSERT INTO `wog_df` VALUES (364,-400,-400,-800,0,0,0,15,10,'幽冥神釜',0,4500,0,1,0,0,0,0,0,0,0,0,0,0,6,0,21000,1,0);
INSERT INTO `wog_df` VALUES (365,0,200,200,0,0,0,14,10,'星塵之憶',0,0,2900,1,0,0,0,0,0,0,0,0,0,0,5,0,21000,1,0);
INSERT INTO `wog_df` VALUES (366,-300,-300,0,0,0,0,17,10,'閃靈爆震',0,0,4000,1,0,0,0,0,0,0,0,0,0,0,3,0,21000,1,0);
INSERT INTO `wog_df` VALUES (367,0,0,0,0,0,0,0,10,'竹葉',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (368,0,0,0,0,0,0,0,10,'竹片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (369,0,0,0,0,0,0,0,10,'布鞋',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (370,0,0,0,0,0,0,0,10,'信封',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (371,0,0,0,0,0,0,0,10,'橡膠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (372,0,0,0,0,0,0,0,10,'綠色液體',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (373,0,0,0,0,0,0,0,10,'黏稠液體',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (374,0,0,0,0,0,0,0,10,'昆蟲翅膀',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (375,0,0,0,0,0,0,0,10,'阿拉丁壺',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (376,0,0,0,0,0,0,0,10,'巫女髮簪',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (377,0,0,50,0,0,0,20,10,'辟邪石',5,0,350,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,1,0);
INSERT INTO `wog_df` VALUES (378,200,200,150,0,0,0,37,10,'初心項鍊',5,100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,19250,1,0);
INSERT INTO `wog_df` VALUES (379,150,0,620,0,0,0,22,10,'神偷手套',3,80,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,19250,1,0);
INSERT INTO `wog_df` VALUES (380,100,150,0,0,0,0,23,10,'天福帽',1,0,280,1,0,0,0,0,0,0,0,0,0,0,NULL,0,17500,1,0);
INSERT INTO `wog_df` VALUES (381,200,400,100,0,0,0,24,10,'領導者劍',0,3000,0,1,0,0,0,0,0,0,0,0,0,0,1,0,21000,1,0);
INSERT INTO `wog_df` VALUES (382,500,850,0,0,0,0,26,10,'造物盾',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,1,0);
INSERT INTO `wog_df` VALUES (383,950,300,0,0,0,0,27,10,'無量鎧',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,21000,1,0);
INSERT INTO `wog_df` VALUES (384,-350,0,1000,0,0,0,38,10,'吹雪丸',0,2000,0,1,0,0,0,0,0,0,0,0,0,0,2,0,19250,1,0);
INSERT INTO `wog_df` VALUES (385,800,250,0,0,0,0,34,10,'龍神鎧',2,100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,24500,1,0);
INSERT INTO `wog_df` VALUES (386,400,600,100,0,0,0,35,10,'大精靈手套',3,0,100,1,0,0,0,0,0,0,0,0,0,0,NULL,0,24500,1,0);
INSERT INTO `wog_df` VALUES (387,0,0,1600,0,0,0,36,10,'傳說鞋',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,24500,1,0);
INSERT INTO `wog_df` VALUES (388,0,0,0,0,0,0,0,700,'玻璃鞋',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (389,0,0,0,0,0,0,0,10,'冰塊',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (390,0,0,0,0,0,0,0,10,'詛咒娃娃',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (391,0,0,0,0,0,0,0,50,'蟲草',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (392,0,0,0,0,0,0,0,30,'魚鱗',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (393,0,0,0,0,0,0,0,3200,'珍珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (394,0,0,0,0,0,0,0,10,'陽光盒',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (395,0,0,0,0,0,0,0,10,'黑暗盒',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (396,0,0,0,0,0,0,0,10,'500經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,500,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (397,0,0,0,0,0,0,0,10,'1000經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,1000,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (398,0,0,0,0,0,0,0,10,'3000經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,3000,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (399,0,0,0,0,0,0,0,10,'木材',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (400,0,0,0,0,0,0,0,200,'月光花',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (401,0,0,0,0,0,0,0,10,'泡泡龍的戲服',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (402,0,0,0,0,0,0,0,500,'日蝕之花',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (403,0,0,0,0,0,0,0,10,'麻醉草',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (404,0,0,0,0,0,0,0,50,'止血草',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (405,0,0,0,0,0,0,0,10,'王城補給品',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (406,0,0,0,0,0,0,0,10,'聖潔之花',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (407,0,0,0,0,0,0,0,10,'暗之刃印記',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (408,0,0,0,0,0,0,0,10,'9000經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,9000,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (409,0,0,0,0,0,0,0,10,'15000經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,15000,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (410,0,0,0,0,0,0,0,320,'惡靈的妖目',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (411,0,0,0,0,0,0,0,10,'古舊劍',0,1,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (412,0,0,0,0,0,0,0,0,'古舊杖',0,0,1,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (413,0,0,0,0,0,0,0,10,'古代文物',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (414,0,0,60,320,200,100,0,10,'藍耀之劍',0,490,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (415,0,0,0,0,0,0,0,10,'遺跡調查員證書',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (416,0,0,0,100,100,300,0,10,'藍耀之杖',0,0,530,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (417,0,0,0,0,0,0,0,10,'夢魔之書',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (418,0,0,0,0,0,0,0,10,'性感照片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (419,0,0,0,0,0,0,0,10,'生髮水',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (420,0,0,0,0,0,0,0,10,'魔界邀請函',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (421,0,0,0,0,0,0,0,10,'祝福之酒',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (422,0,0,0,0,0,0,0,10,'莉吉亞的遺作',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (423,0,0,0,0,0,0,0,10,'沙漠之鷹',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (424,0,0,0,0,0,0,0,10,'毒蠍石',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (425,600,550,0,2800,1000,1000,0,10,'榮耀大盾',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (426,0,0,0,0,0,0,0,10,'大地精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (427,0,0,0,0,0,0,0,10,'清水精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (428,0,0,0,0,0,0,0,10,'烈火精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (429,0,0,0,0,0,0,0,10,'巨木精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (430,0,0,0,0,0,0,0,10,'旋風精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (431,0,0,0,0,0,0,0,10,'猛毒精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (432,0,0,0,0,0,3200,0,10,'大精靈召喚',0,0,4520,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (433,0,0,0,0,0,0,0,10,'封印界環',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (434,0,0,0,0,0,0,0,10,'空白書．絢雲',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (435,0,0,0,0,0,0,0,10,'真實水晶',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (436,0,0,0,0,0,0,0,10,'幻獸的記憶',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (437,0,0,0,0,0,0,0,10,'120000 hp回復劑',5,0,0,1,120000,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (438,0,0,0,0,0,0,0,10,'160000 hp回復劑',5,0,0,1,160000,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (439,0,0,0,0,0,0,0,10,'200000 hp回復劑',5,0,0,1,200000,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (440,0,0,0,0,0,0,0,10,'英雄書',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (441,0,0,0,0,0,0,0,10,'20000經驗膠囊',6,0,0,1,0,0,0,0,0,0,0,0,20000,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (442,0,0,0,0,0,0,0,10,'白輪蛋撻',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (443,0,0,0,0,0,0,0,10,'炸雞腿',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (444,0,0,0,0,0,0,0,10,'元素溶劑',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (445,0,0,0,0,0,0,0,10,'莉吉亞的遺物',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (446,0,0,0,0,0,0,0,10,'紅襪子',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (447,0,0,0,0,0,0,0,10,'虛擬形象卷',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (448,210,250,0,0,0,0,0,10,'亞斯迪手套',3,0,150,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (449,0,100,0,0,0,0,0,10,'雷茵的祝福',5,90,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (450,0,0,0,0,0,0,0,10,'玻璃杯',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (451,0,0,0,0,0,0,0,10,'輕旋律樂譜',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (452,0,0,0,0,0,0,0,10,'五線譜',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (453,0,0,0,0,0,0,0,10,'吉他樂譜',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (454,0,0,0,180,120,0,0,10,'血色之鞭',0,250,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (455,0,0,0,0,0,0,0,1200000,'2格背包',6,0,0,0,0,0,0,0,0,0,0,0,0,2,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (456,0,0,0,0,0,0,0,2400000,'3格背包',6,0,0,0,0,0,0,0,0,0,0,0,0,3,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (457,0,0,0,0,0,0,0,10,'水龍劍',0,350,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (458,0,0,0,0,0,0,0,10,'暗影之火',5,0,100,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (459,0,0,0,0,0,0,0,10,'賽蓮豎琴',0,0,2500,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (460,0,0,0,0,1800,0,0,10,'寒冰弓',0,2100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (463,0,0,0,0,0,0,0,10,'風之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (464,0,0,0,0,0,0,0,10,'花之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (465,0,0,0,0,0,0,0,10,'雪之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (466,0,0,0,0,0,0,0,10,'月之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (467,0,0,0,0,0,0,0,10,'奇之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (468,0,0,0,0,0,0,0,10,'山之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (469,0,0,0,0,0,0,0,10,'異之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (470,0,0,0,0,0,0,0,10,'水之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (471,0,0,0,0,0,0,0,10,'春之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (472,0,0,0,0,0,0,0,10,'夏之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (473,0,0,0,0,0,0,0,10,'秋之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (474,0,0,0,0,0,0,0,10,'冬之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (475,0,0,0,0,0,0,0,10,'炎之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (476,0,0,0,0,0,0,0,10,'瀧之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (477,0,0,0,0,0,0,0,10,'砂之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (478,0,0,0,0,0,0,0,10,'嵐之詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (479,0,0,0,0,0,0,0,10,'火藥成分配合表',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (480,0,0,0,0,0,0,0,10,'新式火藥劑量表',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (481,20,20,30,0,0,0,0,10,'四時帽',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (482,0,0,0,0,0,0,0,10,'精靈口語',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (483,0,0,0,320,0,0,0,10,'耀芒長劍',0,420,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (484,0,0,75,0,300,0,0,10,'耀芒弓',0,370,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (485,0,0,0,0,0,0,0,10,'新式炸藥',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (486,140,190,190,0,0,0,0,10,'夢幻鞋',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (487,370,0,0,0,0,0,0,10,'聖光腿甲',4,100,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (488,0,0,0,0,0,0,0,10,'解毒草',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (489,0,0,200,0,0,0,0,10,'鮑魚小刀',0,1200,0,1,0,0,0,0,0,0,0,0,0,0,6,0,0,1,0);
INSERT INTO `wog_df` VALUES (490,0,0,0,0,0,0,0,10,'異變之火',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (491,0,0,0,0,0,0,0,10,'夫拉多羽毛',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (492,0,0,0,0,0,0,0,10,'萬用船票',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (493,0,0,80,0,0,0,0,10,'望遠鏡',5,30,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (494,180,180,150,0,0,0,0,10,'艾伯羅-雷格項鍊',5,100,100,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (495,0,0,0,0,0,0,0,10,'內裂火藥的構想',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (496,0,0,0,0,0,0,0,10,'內裂火藥',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (497,0,0,350,0,0,0,0,0,'火閃電掃帚',0,0,1980,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (498,0,0,0,0,0,0,0,10,'美白面膜',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (499,80,80,0,0,0,0,0,10,'混沌水晶',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (500,50,0,150,0,0,0,0,10,'葛雷之劍',0,3700,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (501,0,60,0,0,0,0,0,10,'葛雷魔法記典',5,0,220,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (502,0,0,1200,0,0,0,0,10,'葛雷腿甲',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (503,0,0,0,0,0,0,0,10,'秘密文件(白)',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (504,0,0,0,0,0,0,0,10,'秘密文件(赤)',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (505,0,0,0,0,0,0,0,10,'秘密文件(綠)',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (506,0,0,2300,0,0,0,0,10,'間諜短槍',0,1100,0,1,0,0,0,0,0,0,0,0,0,0,5,0,0,1,0);
INSERT INTO `wog_df` VALUES (507,0,0,120,0,0,0,0,10,'黑影披風',5,50,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (508,450,0,100,0,0,0,0,10,'黑影服',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (509,0,0,0,0,0,0,0,10,'舊羊皮紙',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (510,0,0,0,0,0,0,0,10,'顯影溶液',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (511,0,0,0,0,0,550,0,10,'夜梟長笛',0,0,610,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (512,80,60,0,0,0,0,0,10,'荒漠靴',4,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (513,60,60,0,0,0,0,0,10,'固希爾披風',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (514,0,0,0,0,0,0,0,10,'固希爾的解約證明',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (515,0,0,0,0,0,0,0,10,'忠誠之劍',0,2900,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (516,30,40,0,0,0,30,0,10,'智能頭巾',1,0,20,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (517,35,0,20,0,30,0,0,10,'AI頭盔',1,10,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (518,0,0,0,0,0,0,0,10,'艾亞斯詩集',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (519,0,0,0,0,0,0,0,10,'石翼鱗片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (520,0,0,0,0,0,0,0,10,'祕術水晶',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (521,0,0,0,0,0,0,0,10,'記憶碎片',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (522,0,0,0,0,0,0,0,10,'黯淡的清水精靈珠',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (523,0,10,0,0,0,0,0,10,'智慧的精華',5,0,60,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (524,0,0,300,1000,1000,0,0,10,'妖火拳套',0,2950,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (525,0,0,0,0,0,0,0,10,'密銀金屬礦石',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (526,0,0,100,2500,0,0,0,10,'退魔雙刃',0,3150,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (527,0,0,0,0,0,0,0,10,'活性布料',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (528,0,0,0,0,0,2000,0,10,'樹靈法杖',0,0,3300,1,0,0,0,0,0,0,0,0,0,0,4,0,0,1,0);
INSERT INTO `wog_df` VALUES (529,0,0,0,0,0,0,0,10,'暗樹調查報告',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (530,0,0,0,0,0,0,0,10,'迪克地圖',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (531,0,0,0,0,0,0,0,10,'科本林地圖',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (532,0,0,0,0,0,0,0,10,'長生之水',5,0,0,1,500000,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (533,0,0,0,0,0,0,0,3800000,'4格背包',6,0,0,0,0,0,0,0,0,0,0,0,0,4,NULL,1,0,0,0);
INSERT INTO `wog_df` VALUES (534,450,400,0,0,0,0,0,10,'熔炎頭冠',1,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (535,0,0,0,0,0,0,0,10,'戰役石板',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (536,0,0,50,100,140,0,0,10,'斬荊利刃',0,240,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (537,0,0,0,0,0,0,0,10,'世界之水',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (538,0,0,0,0,0,0,0,10,'世界樹種子',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (539,120,210,80,0,0,350,0,10,'智慧軟鞋',4,0,100,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (540,110,230,0,0,0,700,0,10,'惡魔符文',3,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (541,0,0,-300,900,0,0,0,10,'炙熱戰斧',0,1350,0,1,0,0,0,0,0,0,0,0,0,0,3,0,0,1,0);
INSERT INTO `wog_df` VALUES (542,0,0,0,0,0,0,0,10,'薩佈雷5格背包',6,0,0,1,0,0,0,0,0,0,0,0,0,5,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (543,0,160,90,0,0,0,0,10,'清靜弓',0,980,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (544,0,0,100,0,0,0,0,10,'魚人釣竿',3,100,50,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (545,0,0,0,0,0,0,0,10,'挖掘隊補給品',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (546,150,0,0,1600,0,0,0,10,'地龍之矛',0,2250,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0);
INSERT INTO `wog_df` VALUES (547,0,0,0,0,0,1800,0,10,'地龍權杖',0,0,2080,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (548,50,0,170,0,0,0,0,10,'地龍爪',0,1900,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (549,250,0,0,1900,0,0,0,10,'土靈之刃',0,2480,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (550,0,0,20,0,1500,1200,0,10,'無線炸彈',5,80,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (551,285,0,0,250,0,0,0,10,'挖掘手套',3,85,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (552,125,150,0,0,0,200,0,10,'地脈面罩',1,0,55,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (553,240,170,0,300,0,200,0,10,'大地披風',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (554,0,0,0,0,0,0,0,10,'星隕石',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (555,200,490,0,0,0,950,0,10,'星隕髮帶',1,0,75,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (556,270,310,280,0,1000,0,0,10,'靈風裝束',2,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (557,390,350,0,1200,0,0,0,10,'魔化硬盾',3,20,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (558,720,320,0,2000,0,0,0,10,'怒鐵鋼甲',2,45,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (559,350,0,-250,0,0,0,0,10,'怒鐵之槌',0,2800,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,1,0);
INSERT INTO `wog_df` VALUES (560,0,0,0,0,0,0,0,10,'萊姆香料',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (561,0,0,0,0,0,0,0,10,'青綠果實',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (562,0,0,0,0,0,0,0,10,'火焰龍蛋',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (563,0,0,0,0,0,0,0,10,'半成品蛋撻',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (564,0,0,0,0,0,0,0,10,'幻氣焦糖',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (565,0,0,0,0,0,0,0,10,'火樹精華',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);
INSERT INTO `wog_df` VALUES (566,0,0,0,0,0,0,0,10,'雨林咖啡豆',5,0,0,1,0,0,0,0,0,0,0,0,0,0,NULL,0,0,0,0);

#
# Table structure for table wog_event
#

DROP TABLE IF EXISTS `wog_event`;
CREATE TABLE `wog_event` (
  `e_id` int(10) unsigned NOT NULL auto_increment,
  `e_body` varchar(200) NOT NULL default '',
  `e_ans` varchar(100) NOT NULL default '',
  PRIMARY KEY  (`e_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_event
#


#
# Table structure for table wog_group_area
#

DROP TABLE IF EXISTS `wog_group_area`;
CREATE TABLE `wog_group_area` (
  `g_a_id` int(10) unsigned NOT NULL auto_increment,
  `g_id` int(10) unsigned NOT NULL default '0',
  `g_a_type` tinyint(3) unsigned NOT NULL default '0',
  `g_a_hp` tinyint(3) unsigned NOT NULL default '100',
  `g_a_dateline` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`g_a_id`),
  KEY `g_id` (`g_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_group_area
#


#
# Table structure for table wog_group_book
#

DROP TABLE IF EXISTS `wog_group_book`;
CREATE TABLE `wog_group_book` (
  `g_id` int(11) NOT NULL default '0',
  `g_book` text NOT NULL,
  KEY `g_id` (`g_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_group_book
#


#
# Table structure for table wog_group_event
#

DROP TABLE IF EXISTS `wog_group_event`;
CREATE TABLE `wog_group_event` (
  `g_b_inid` int(10) unsigned NOT NULL auto_increment,
  `g_b_id` int(10) unsigned NOT NULL default '0',
  `g_b_body` varchar(250) NOT NULL default '',
  `g_b_dateline` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`g_b_inid`),
  KEY `g_b_id` (`g_b_id`),
  KEY `g_b_dateline` (`g_b_dateline`)
) TYPE=MyISAM;

#
# Dumping data for table wog_group_event
#


#
# Table structure for table wog_group_join
#

DROP TABLE IF EXISTS `wog_group_join`;
CREATE TABLE `wog_group_join` (
  `g_j_id` int(10) unsigned NOT NULL auto_increment,
  `g_id` int(10) unsigned NOT NULL default '0',
  `p_id` int(10) unsigned NOT NULL default '0',
  `g_j_dateline` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`g_j_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_group_join
#


#
# Table structure for table wog_group_main
#

DROP TABLE IF EXISTS `wog_group_main`;
CREATE TABLE `wog_group_main` (
  `g_id` int(10) unsigned NOT NULL auto_increment,
  `g_name` varchar(50) NOT NULL default '',
  `g_win` smallint(5) unsigned NOT NULL default '0',
  `g_lost` smallint(5) unsigned NOT NULL default '0',
  `g_peo` smallint(5) unsigned NOT NULL default '0',
  `g_adm_id1` int(11) NOT NULL default '0',
  `g_adm_id2` int(11) NOT NULL default '0',
  `g_money` int(10) unsigned NOT NULL default '0',
  `g_exp` int(10) unsigned NOT NULL default '0',
  `g_lv` tinyint(3) unsigned NOT NULL default '0',
  `g_fire` tinyint(1) unsigned NOT NULL default '0',
  `g_fire_time` int(11) NOT NULL default '0',
  PRIMARY KEY  (`g_id`),
  UNIQUE KEY `g_name` (`g_name`),
  KEY `g_fire` (`g_fire`)
) TYPE=MyISAM;

#
# Dumping data for table wog_group_main
#


#
# Table structure for table wog_img
#

DROP TABLE IF EXISTS `wog_img`;
CREATE TABLE `wog_img` (
  `i_filename` varchar(20) NOT NULL default 'N/A',
  `i_id` tinyint(4) unsigned NOT NULL auto_increment,
  PRIMARY KEY  (`i_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_img
#

INSERT INTO `wog_img` VALUES ('1.gif',1);
INSERT INTO `wog_img` VALUES ('2.gif',2);
INSERT INTO `wog_img` VALUES ('3.gif',3);
INSERT INTO `wog_img` VALUES ('4.gif',4);
INSERT INTO `wog_img` VALUES ('5.gif',5);
INSERT INTO `wog_img` VALUES ('6.gif',6);
INSERT INTO `wog_img` VALUES ('7.gif',7);
INSERT INTO `wog_img` VALUES ('8.gif',8);
INSERT INTO `wog_img` VALUES ('9.gif',9);
INSERT INTO `wog_img` VALUES ('10.gif',10);
INSERT INTO `wog_img` VALUES ('11.gif',11);
INSERT INTO `wog_img` VALUES ('12.gif',12);
INSERT INTO `wog_img` VALUES ('13.gif',13);
INSERT INTO `wog_img` VALUES ('14.gif',14);
INSERT INTO `wog_img` VALUES ('15.gif',15);
INSERT INTO `wog_img` VALUES ('16.gif',16);
INSERT INTO `wog_img` VALUES ('17.gif',17);
INSERT INTO `wog_img` VALUES ('18.gif',18);
INSERT INTO `wog_img` VALUES ('19.gif',19);
INSERT INTO `wog_img` VALUES ('20.gif',20);
INSERT INTO `wog_img` VALUES ('21.gif',21);
INSERT INTO `wog_img` VALUES ('22.gif',22);
INSERT INTO `wog_img` VALUES ('23.gif',23);
INSERT INTO `wog_img` VALUES ('24.gif',24);
INSERT INTO `wog_img` VALUES ('25.gif',25);
INSERT INTO `wog_img` VALUES ('26.gif',26);
INSERT INTO `wog_img` VALUES ('27.gif',27);
INSERT INTO `wog_img` VALUES ('28.gif',28);
INSERT INTO `wog_img` VALUES ('29.gif',29);
INSERT INTO `wog_img` VALUES ('30.gif',30);
INSERT INTO `wog_img` VALUES ('31.gif',31);
INSERT INTO `wog_img` VALUES ('32.gif',32);
INSERT INTO `wog_img` VALUES ('33.gif',33);
INSERT INTO `wog_img` VALUES ('34.gif',34);
INSERT INTO `wog_img` VALUES ('35.gif',35);
INSERT INTO `wog_img` VALUES ('36.gif',36);
INSERT INTO `wog_img` VALUES ('37.gif',37);
INSERT INTO `wog_img` VALUES ('38.gif',38);
INSERT INTO `wog_img` VALUES ('39.gif',39);
INSERT INTO `wog_img` VALUES ('40.gif',40);
INSERT INTO `wog_img` VALUES ('41.gif',41);
INSERT INTO `wog_img` VALUES ('42.gif',42);
INSERT INTO `wog_img` VALUES ('43.gif',43);
INSERT INTO `wog_img` VALUES ('44.gif',44);
INSERT INTO `wog_img` VALUES ('45.gif',45);
INSERT INTO `wog_img` VALUES ('46.gif',46);
INSERT INTO `wog_img` VALUES ('47.gif',47);
INSERT INTO `wog_img` VALUES ('48.gif',48);
INSERT INTO `wog_img` VALUES ('49.gif',49);
INSERT INTO `wog_img` VALUES ('50.gif',50);
INSERT INTO `wog_img` VALUES ('51.gif',51);
INSERT INTO `wog_img` VALUES ('52.gif',52);
INSERT INTO `wog_img` VALUES ('53.gif',53);
INSERT INTO `wog_img` VALUES ('54.gif',54);
INSERT INTO `wog_img` VALUES ('55.gif',55);
INSERT INTO `wog_img` VALUES ('56.gif',56);
INSERT INTO `wog_img` VALUES ('57.gif',57);
INSERT INTO `wog_img` VALUES ('58.gif',58);
INSERT INTO `wog_img` VALUES ('59.gif',59);
INSERT INTO `wog_img` VALUES ('60.gif',60);
INSERT INTO `wog_img` VALUES ('61.gif',61);
INSERT INTO `wog_img` VALUES ('62.gif',62);
INSERT INTO `wog_img` VALUES ('63.gif',63);
INSERT INTO `wog_img` VALUES ('64.gif',64);
INSERT INTO `wog_img` VALUES ('65.gif',65);
INSERT INTO `wog_img` VALUES ('66.gif',66);
INSERT INTO `wog_img` VALUES ('67.gif',67);
INSERT INTO `wog_img` VALUES ('68.gif',68);
INSERT INTO `wog_img` VALUES ('69.gif',69);
INSERT INTO `wog_img` VALUES ('70.gif',70);
INSERT INTO `wog_img` VALUES ('71.gif',71);
INSERT INTO `wog_img` VALUES ('72.gif',72);
INSERT INTO `wog_img` VALUES ('73.gif',73);
INSERT INTO `wog_img` VALUES ('74.gif',74);
INSERT INTO `wog_img` VALUES ('75.gif',75);
INSERT INTO `wog_img` VALUES ('76.gif',76);
INSERT INTO `wog_img` VALUES ('77.gif',77);
INSERT INTO `wog_img` VALUES ('78.gif',78);
INSERT INTO `wog_img` VALUES ('79.gif',79);
INSERT INTO `wog_img` VALUES ('80.gif',80);
INSERT INTO `wog_img` VALUES ('81.gif',81);
INSERT INTO `wog_img` VALUES ('82.gif',82);
INSERT INTO `wog_img` VALUES ('83.gif',83);
INSERT INTO `wog_img` VALUES ('84.gif',84);
INSERT INTO `wog_img` VALUES ('85.gif',85);
INSERT INTO `wog_img` VALUES ('86.gif',86);
INSERT INTO `wog_img` VALUES ('87.gif',87);
INSERT INTO `wog_img` VALUES ('88.gif',88);
INSERT INTO `wog_img` VALUES ('89.gif',89);
INSERT INTO `wog_img` VALUES ('90.gif',90);
INSERT INTO `wog_img` VALUES ('91.gif',91);
INSERT INTO `wog_img` VALUES ('92.gif',92);
INSERT INTO `wog_img` VALUES ('93.gif',93);
INSERT INTO `wog_img` VALUES ('94.gif',94);
INSERT INTO `wog_img` VALUES ('95.gif',95);

#
# Table structure for table wog_item
#

DROP TABLE IF EXISTS `wog_item`;
CREATE TABLE `wog_item` (
  `p_id` int(11) NOT NULL default '0',
  `a_id` varchar(150) NOT NULL default '',
  `d_body_id` varchar(150) NOT NULL default '',
  `d_foot_id` varchar(150) NOT NULL default '',
  `d_hand_id` varchar(150) NOT NULL default '',
  `d_head_id` varchar(150) NOT NULL default '',
  `d_item_id` varchar(150) NOT NULL default '',
  PRIMARY KEY  (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_item
#

INSERT INTO `wog_item` VALUES (1,'','','','','','');

#
# Table structure for table wog_message
#

DROP TABLE IF EXISTS `wog_message`;
CREATE TABLE `wog_message` (
  `m_id` int(10) unsigned NOT NULL auto_increment,
  `p_id` int(10) NOT NULL default '0',
  `title` varchar(250) NOT NULL default '',
  `dateline` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`m_id`),
  KEY `p_id` (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_message
#


#
# Table structure for table wog_mission_book
#

DROP TABLE IF EXISTS `wog_mission_book`;
CREATE TABLE `wog_mission_book` (
  `m_id` int(10) unsigned NOT NULL default '0',
  `p_id` int(10) unsigned NOT NULL default '0',
  `m_status` tinyint(1) NOT NULL default '0',
  `m_kill_num` tinyint(3) unsigned NOT NULL default '0',
  UNIQUE KEY `m_id` (`m_id`,`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_mission_book
#


#
# Table structure for table wog_mission_main
#

DROP TABLE IF EXISTS `wog_mission_main`;
CREATE TABLE `wog_mission_main` (
  `m_id` int(10) unsigned NOT NULL auto_increment,
  `m_body` text NOT NULL,
  `m_end_message` text NOT NULL,
  `m_subject` varchar(100) NOT NULL default '',
  `m_name` varchar(50) NOT NULL default '',
  `m_lv` int(10) unsigned NOT NULL default '0',
  `m_sex` tinyint(1) unsigned NOT NULL default '0',
  `m_job` tinyint(4) unsigned NOT NULL default '0',
  `m_rating` int(10) unsigned NOT NULL default '0',
  `m_need_id` int(10) unsigned NOT NULL default '0',
  `m_not_id` int(10) unsigned NOT NULL default '0',
  `m_birth` tinyint(4) unsigned default NULL,
  `m_store_id` tinyint(1) unsigned NOT NULL default '0',
  `m_area_id` tinyint(3) unsigned NOT NULL default '0',
  `m_monster_id` varchar(15) NOT NULL default '0',
  `m_kill_num` tinyint(3) unsigned NOT NULL default '0',
  `m_pet_id` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`m_id`),
  KEY `m_lv` (`m_lv`),
  KEY `m_sex` (`m_sex`),
  KEY `m_job` (`m_job`),
  KEY `m_rating` (`m_rating`)
) TYPE=MyISAM;

#
# Dumping data for table wog_mission_main
#

INSERT INTO `wog_mission_main` VALUES (1,'近日村內的漁網因為已經長年使用而不堪修補了，必須全面換新，希望有人能夠幫忙蒐集製作漁網的材料。 \r\n\r\n完成條件：蜘蛛絲*3 \r\n任務獎勵：白色布料*1','感謝您的努力，讓漁村可以繼續用漁網捕魚\r\n但是最近常常有魚群大量死亡，我懷疑是上游的惡水族搞的鬼\r\n\r\n可在銀鯨任事所接受這項任務','製作漁網','漁人碼頭村長 周漁民',1,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (2,'上游的惡水族，每到夜晚都會排放有毒物質，造成海岸邊魚群大量死亡\r\n請循著河流前往迷霧森林打敗惡水族族長 米列\r\n\r\n完成條件：打敗米列\r\n任務獎勵：500經驗膠囊*3','謝謝您幫我們打敗惡水族，可是之前的毒物事件讓村民得了怪病\r\n聽說蟲草可治這種病\r\n\r\n可在銀鯨任事所接受這項任務','打敗米列','漁人碼頭村長 周漁民',25,3,99,0,1,0,NULL,3,4,'212',1,0);
INSERT INTO `wog_mission_main` VALUES (3,'由於受到米列毒物的影響，村民紛紛產生怪病聽說黑暗沼澤的蟲草可治這種病能否請你幫我們收集蟲草？ \r\n\r\n完成條件：收集7個蟲草\r\n任務獎勵：500經驗膠囊*5','','收集7個蟲草','漁人碼頭村長 周漁民',30,3,99,0,2,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (4,'本村最紅的偶像團體F4，最近要舉行一場慈善表演但是搭建舞台的木材被附近的盜賊搶走請幫忙收集木材 \r\n\r\n完成條件：收集8個木材\r\n任務獎勵：金錢30000','','收集8個木材','漁人碼頭村長 周漁民',10,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (5,'我愛戀F4中的泡泡龍很久，雖然爸爸很反對但我仍希望在慈善演出中，送泡泡龍上花環我需要月光花，能幫我收集嗎？ \r\n\r\n完成條件：收集6朵月光花\r\n任務獎勵：妖精之水*1，500經驗膠囊*2','','收集月光花','漁人碼頭村長女兒 周美人',15,3,99,0,4,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (6,'我是F4中的泡泡龍，慈善表演快開始了\r\n可是我的戲服在一次的練習中被Fans偷走\r\n希望你能打敗我的Fans，替我拿回戲服\r\n\r\n完成條件：擊敗Fans，拿回戲服\r\n任務獎勵：水晶*2，500經驗膠囊*6','','拿回戲服','漁人碼頭村民 泡泡龍',30,3,99,0,5,0,NULL,2,4,'213',1,0);
INSERT INTO `wog_mission_main` VALUES (7,'我現在正需要人手，幫我收集麻藥但是最近附近怪物肆虐，需要強壯的人來收集你能幫忙嗎？ \r\n\r\n完成條件：麻醉草*3\r\n任務獎勵：金錢10000','','收集麻醉草3個','怪醫 白傑克',8,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (8,'在最近一次的大手術中，止血草用完了下個月有一場大手術，需要止血草才能開刀能否幫我收集止血草？ \r\n\r\n完成條件：收集8個止血草\r\n任務獎勵：金錢10000，500經驗膠囊*5','','收集8個止血草','怪醫 白傑克',20,3,99,0,7,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (9,'我查墨H前的古書籍，裡面記載傳說中的手術刀-不見血\r\n製造這把手術刀需要強化鋼鐵*3，鑽石*2\r\n如果有這把手術刀，就能讓我醫治更多人\r\n\r\n完成條件：強化鋼鐵*3，鑽石*2\r\n任務獎勵：古書*2，1000經驗膠囊*9','','傳說中的手術刀','怪醫 白傑克',45,3,99,0,8,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (10,'我終於如願成為祭司了，但是直到昨天我才想到我竟然忘記準備神職服裝了...！ \r\n可是這些服裝並不是一天兩天就能夠找齊的，所以希望大家能幫忙收集。\r\n\r\n完成條件：智慧指輪*1，智慧耳環*1，主教徽章*1\r\n任務獎勵：天使之息*1，500經驗膠囊*8','','邁向祭司之路','迷糊祭司克利夫',50,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (11,'喔呵呵呵，我的美貌是世界皆知的，我想你們也都知道。\r\n但是，僅僅如此的外觀並不能襯托我這嬌麗的氣質;若是有人能夠幫忙收集下列的這些珍品的話必施重賞！ \r\n\r\n完成條件：天使之息*1，貴婦髮帶*2，鑽石*2，珍珠*2\r\n任務獎勵：阿拉丁壺*1，1000經驗膠囊*5','','美之巔峰','中年肥貴婦',55,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (12,'傳說在迷霧森林中生長著一朵只在日蝕之夜才會綻放的花朵，而持有這朵花的人將會的到永久的幸福... \r\n我最近迷戀上一位美麗的女子，卻遲遲無法對他說出我的感受...因此請求各位能夠替我找出這朵花...\r\n\r\n完成條件：日蝕之花*5\r\n任務獎勵：1000經驗膠囊*6','','幸福之花','戀愛中的男子 如風',60,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (13,'近日會內需要一些物品以便舉行活動，在此發出委託請求協助。\r\n\r\n完成條件：蜘蛛裝*1，鬼牌*1，火藥*1\r\n任務獎勵：1000經驗膠囊*7','','盜賊新人歡迎會','盜賊工會',60,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (14,'傳奇的武具出自於偉大的刀匠，而偉大的刀匠要製作出一把曠世神兵卻需要有上等的材料！ \r\n現在，偉大的刀匠已經有了，卻唯獨缺了上等的材料啊~~ \r\n來吧，就讓我們一同創造出足以名留千古的傳奇之作吧！ \r\n\r\n完成條件：火砂*1，強化鋼鐵*1，雷神珠*1，戰狂之魄*1\r\n任務獎勵：3000經驗膠囊*9','','紅蓮與奔雷','矮人鐵匠',65,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (15,'原本也是德魯依教徒的凱西勒法師，與依佛雷姆大祭司是從小一同長大的好友，但卻在年長後，逐漸地與黑暗的力量有所掛勾\r\n\r\n遭人發現後，依佛雷姆在教徒的壓力下，只好不顧多年情誼，忍痛將其以放逐之名義，禁臠於戰慄森林地底下的地道中\r\n\r\n凱西勒法師因而對德魯依教徒懷恨在心，不時想找機會報復，甚至研究起召喚魔物的法術，想致德魯依教徒於死地。現在，凱西勒召喚來具有強大法術的冰雪女魔，你能幫助德魯依教徒免於危難嗎？\r\n\r\n完成條件：打敗冰雪魔女\r\n任務獎勵：冰塊*1，3000經驗膠囊*2','','幫助德魯依教徒','德魯依教徒',70,3,99,0,0,0,NULL,1,5,'214',1,0);
INSERT INTO `wog_mission_main` VALUES (16,'不久之前，我帶著我的寵物史萊姆外出散步時\r\n遇到怪物襲擊，使得我的寵物受到驚嚇走失了\r\n能幫我找回史萊姆嗎？\r\n\r\n完成條件：寵物史萊姆\r\n任務獎勵：金錢3500','','協尋寵物','漁人碼頭村長女兒 周美人',5,3,99,0,0,0,NULL,1,0,'0',0,1);
INSERT INTO `wog_mission_main` VALUES (17,'近日青魔導士四處為惡，我的手下在最近幾次的行動中受了重傷\r\n王城也遲遲不加派人手\r\n看你蠻強壯的，是否能替我擊敗8位青魔導士\r\n\r\n完成條件：擊敗8位青魔導士\r\n任務獎勵：金錢15000，500經驗膠囊*2','不好了，上位青魔導士劫走王城運送過來的補給品\r\n\r\n請你前往銀鯨任事所接受這項任務','擊敗青魔導士','中央城治安官 亞里斯',50,3,99,0,0,0,NULL,3,4,'59',8,0);
INSERT INTO `wog_mission_main` VALUES (18,'這件事情相當嚴重，王城運送過來的補給品\r\n在半路上被上位青魔導士劫走，我們營地糧食只能再支撐1個月\r\n斥候回報上位青魔導士目前在古代遺跡\r\n希望你能代替我前往古代遺跡打敗上位青魔導士，並奪回補給品\r\n\r\n完成條件：打敗上位青魔導士，奪回補給品\r\n任務獎勵：1000經驗膠囊*5，強化鋼鐵*1','傳說中的紅鱗巨龍出沒，請前往銀鯨任事所','打敗上位青魔導士','中央城治安官 亞里斯',80,3,99,0,17,0,NULL,3,5,'215',1,0);
INSERT INTO `wog_mission_main` VALUES (19,'古代遺跡附近有一做老礦坑，在附近採礦的礦工遭遇不明生物襲擊\r\n根據目擊者報告是傳聞中的紅鱗巨龍\r\n希望你能打敗紅鱗巨龍，讓採礦作業能繼續進行\r\n\r\n完成條件：打敗紅鱗巨龍\r\n任務獎勵：1000經驗膠囊*8，詛咒娃娃*2','','治退紅鱗巨龍','中央城治安官 亞里斯',85,3,99,0,18,0,NULL,3,5,'216',1,0);
INSERT INTO `wog_mission_main` VALUES (20,'諾亞尼爾是一個位在山谷裡的小村莊，因為村裡的人得罪了居住在黑暗沼澤旁的的黑沼法師而被施與詛咒\r\n使的全村的人都陷入了永久的沉睡，你能解救村民脫離這個沉寂之村百年來的宿命嗎? \r\n\r\n完成條件：打敗黑沼法師\r\n任務獎勵：金錢5000','','解救諾亞尼爾村','流浪村民',12,3,99,0,0,0,NULL,1,3,'217',1,0);
INSERT INTO `wog_mission_main` VALUES (21,'村民們發現，黑沼法師長期居住在黑暗沼澤是為了研究沼澤中的神秘力量\r\n雖然我們不知道這股神秘力量是什麼，但是希望你們協助我們封印這股力量\r\n\r\n完成條件：打敗黑沼守護者\r\n任務獎勵：500經驗膠囊*2','','封印黑沼力量','諾亞尼爾村民',16,3,99,0,21,0,NULL,1,3,'218',1,0);
INSERT INTO `wog_mission_main` VALUES (22,'我最近想買一批lv包包，可是無奈海關把守的很緊，所以一直到不了手，能不能請你幫我弄來9個錢包，我有謝禮13000元，麻煩你了！\r\n\r\n完成條件：錢包*9\r\n任務獎勵：金錢13000','','LV包包','路易貴婦',10,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (23,'一年一度的十二月精靈祭即將隆重登場，村民們為了佈置環境而忙的不可開交\r\n然而於每年三月為了取得純真無垢的聖潔之花而選出的精靈祭司這次卻因為腳踝不幸扭傷而無法外出，希望有熱心的冒險者能夠協尋。 \r\n\r\n完成條件：聖潔之花*1\r\n任務獎勵：賢者手套，貴族帽，滅魔聖袍','','精靈之祭與聖潔之花','佛洛斯村村長',95,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (24,'一年一度的十二月精靈祭即將隆重登場，村民們為了佈置環境而忙的不可開交 \r\n然而原本被視為村子象徵的精靈之木卻因為不明原因而逐漸炸銦A眼看著精靈祭就要到了，精靈之木卻尚未恢復原有的氣息 \r\n聽說世界上有著一種名為妖精之水的神秘液體具有提高施術者魔法力的效果，這種液體或野i以為凋零的精靈之木帶來一絲的希望... \r\n因此請求各位能夠協助搜尋妖精之水。\r\n\r\n完成條件：妖精之水*3\r\n任務獎勵：3000經驗膠囊*3，古舊劍','','最後的輪舞曲','佛洛斯村村長',110,3,99,0,23,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (25,'大家知道正在被通緝的殺手集團\"暗之刃\"嗎？ \r\n他們的高級殺手好像正躲藏在王者之路。 \r\n這可是個不錯的機會啊！ \r\n\r\n完成條件：暗之刃印記*1\r\n任務獎勵：金錢25000','','暗之刃','情報販子布利特',120,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (26,'我不小心把玻璃鞋掉進了失落古船地帶。 \r\n這是我和男朋友第一次約會時他送我的禮物對我來說相當重要。所以我想趁他未發現時趕快找回來。 \r\n\r\n完成條件：玻璃鞋*1\r\n任務獎勵：9000經驗膠囊*2，陽光盒*1','','協尋玻璃鞋','賣火柴的灰姑娘',750,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (27,'我打聽到一些關於惡靈的妖目的消息… \r\n這可不是一件好東西。 \r\n聽說它可以肆意操縱惡靈襲擊無辜的女性… \r\n它現在就在惡靈伯爵的手上。\r\n\r\n完成條件：惡靈的妖目*2\r\n任務獎勵：9000經驗膠囊*2，金錢60000','','惡靈的妖目','某情報販子',600,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (28,'最近突然收到了一封決鬥書。 \r\n我很害怕，有誰願意代替我去嗎？ \r\n只要打扮成我的樣子就可以了。 \r\n\r\n完成條件：打敗光明騎士*10\r\n任務獎勵：500經驗膠囊*4，金錢35000','','決鬥代理','二世祖子爵',90,3,99,0,0,0,NULL,2,4,'106',10,0);
INSERT INTO `wog_mission_main` VALUES (29,'勇者是全世界人類的英雄，是所有人類的救星 \r\n然而，最近據說出現了一批冒充為勇者的人在各地吃霸王嚏A甚至還四處胡作非為 \r\n現在他們正棲息在王者之路中，徵求各位勇敢的戰士們一同去揭穿他們的真面目吧！\r\n\r\n完成條件：擊敗冒牌英雄or冒牌召喚師6次\r\n任務獎勵：9000經驗膠囊*4，金錢15000','','冒牌傳說','全國冒險者工會',680,3,99,0,0,0,NULL,1,7,'111,112',6,0);
INSERT INTO `wog_mission_main` VALUES (30,'最近武器好像有些供不應求， \r\n所以我們水色工房決定開始實施一個新的服務項目！ \r\n就是讓舊劍換新貌。 \r\n請大家一定要多多捧場\r\n\r\n完成條件：古舊劍，鋼鐵*1，強化鋼鐵*1，硬殼*1\r\n任務獎勵：藍耀之劍','','鍛劍去！','水色工房',150,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (31,'今年也將繼續調查未日王城的古代遺跡。 \r\n現徵調查員，經驗不問。 \r\n這是個親身接觸古代文化的好機會啊！ \r\n有興趣的朋友請務必參加！ \r\n\r\n完成條件：擊敗古代遺跡守護者*5，古代文物*5\r\n任務獎勵：金錢30000，遺跡調查員證書*1','','遺跡調查1','水色遺跡調查團',140,3,99,0,0,0,NULL,2,5,'220',5,0);
INSERT INTO `wog_mission_main` VALUES (32,'傳說在遺跡的深處有一把古舊杖，用這把舊杖跟鬥法羽衣可以鍛造出藍耀之杖\r\n但是至今無人可以找出這把舊杖。\r\n\r\n請你把這把杖找出來，我們幫你製作藍耀之杖\r\n\r\n完成條件：古舊杖*1，鬥法羽衣*1，擊敗舊杖守護者\r\n任務獎勵：藍耀之杖','','遺跡調查2','水色工房',145,3,99,0,31,0,NULL,1,5,'221',1,0);
INSERT INTO `wog_mission_main` VALUES (33,'我親眼所見！老爺他對著一個恐佈的娃娃下咒語！ \r\n我肯定女主人的病就是因為這個… \r\n拜拜哪位好心人救救我的女主人吧。 \r\n\r\n完成條件：魔法水*1，詛咒娃娃*1，古書*1\r\n任務獎勵：9000經驗膠囊*3','原來老爺是受到地下室惡魔所操縱','詛咒的人偶怪','斯多林家族 女僕人',175,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (34,'老爺從年輕時熱衷惡魔召喚術，斯多林家族之所以致富，也是惡魔召喚術的戊塗r\n不久之前老爺召喚出惡魔莉莉斯後，整個人性情大變還對女主人下咒\r\n莉莉斯現在已逃往久遠戰場\r\n\r\n完成條件：擊敗惡魔莉莉斯\r\n任務獎勵：9000經驗膠囊*4','','擊敗惡魔莉莉斯','斯多林家族 女僕人',185,3,99,0,33,0,NULL,3,6,'222',1,0);
INSERT INTO `wog_mission_main` VALUES (35,'我終於即將完成我畢生最大的心願！ \r\n一個偉大的發明~春藥！ \r\n只要把它完成了，我就能成為百萬富翁並且流方百世。 \r\n有沒有誰能給我一些好的建議? \r\n\r\n完成條件：綠色液體*1，黏稠液體*1，古書*1，性感照片*1\r\n任務獎勵：？','','終極的發明！','宮廷鍊金術應用署委員 大白',200,1,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (36,'魔界君主將於本月隆重舉辦四千大壽宴會，希望在這時候能夠不分敵我一同來慶祝這難能可貴的一日！ \r\n不過，這場宴會必須要具備一定實力以上的英雄才有資格參加，如此才不辱君主的聲望 \r\n所以，必須先找尋異界守護者並將之擊敗，方能取得參加的邀請函。請各位英雄們一同來共襄盛舉吧！ \r\n\r\n委託物品：擊退異界守護者*8 \r\n報酬物品：魔界邀請函*1','','魔界的邀請1','次元惡魔',2500,3,99,0,0,0,NULL,2,9,'132',8,0);
INSERT INTO `wog_mission_main` VALUES (37,'各位有著過人實力的英雄們，歡迎你們來到魔界君主的四千大壽宴會！ \r\n君主正為了能看到如此傑出的英雄們齊聚這裡為它祝壽而感到十分的欣慰呢！ \r\n好了，先切回正題，既然是來替君主祝壽的，那麼當然也不能忘了帶點東西來慶祝囉！ \r\n君主說這慶祝的東西揪由我來決定。而最近剛好魔界的上等優良好酒已經快要用完了，所以宴會上要用到的酒可能會不夠用，所以這次的祝壽品就決定是祝福之酒囉！ \r\n不過這種酒極為罕有，只有海神那邊才找得到這種夢幻佳釀，至於其他的地方有沒有就不得而知了。 \r\n好了，話就到此結束，請各位英雄們找到之後盡快回來替君主完成這四千年的大壽宴禮吧！\r\n\r\n委託物品：魔界邀請函*1\r\n報酬物品：祝福之酒*1','','魔界的邀請2','次元惡魔',2500,3,99,0,36,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (38,'今年也已經快要過去了，路過每戶皆可聽見喜悅之聲，但是史塔利克家卻無法像他們一樣地快樂... \r\n我們家的小姐在前幾天的時候不幸被診斷出罹患有不治之症...! \r\n這種病感染上之後起初並不會有什麼特別的症狀。然而，約過了10天之後患者會突然出現眼神呆滯現象，接著會出現強烈的幻覺，到了最後，腦部負荷不了龐大的負荷之後便會造成腦部受損... \r\n小姐雖然表現出一副安然無恙的樣子，但是其實內心也是非常的痛苦的... \r\n因為小姐曾經說過她以後想要到世界上的每一個角落留下她的足跡 \r\n如今卻因為這場突如其來的大病而沒辦法實現... \r\n據說，在某個國度中有著一本傳說中的書，只要將這本書一翻開之後嬝牧漱H便會如身歷其境般的與書中的人物活躍著 \r\n現在只剩下這唯一的希望能夠幫助小姐完成願望了，請各為勇士們幫幫忙！\r\n\r\n委託物品：莉吉亞的遺作*1\r\n任務獎勵：9000經驗膠囊*3，金錢30000','','終歲之願','史塔利克家管家',280,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (39,'嗯～草原的空氣真是新鮮啊，彷彿能使平時的煩憂一掃而空似的 \r\n今天是我好不容易才等到的十八歲生日，同時也是我展開冒險的第一日 \r\n就如同所有的冒險者們一樣，我也是抱著滿心的熱血來到了這片草原 \r\n卻沒想到在這平原上竟然四處都有惹人厭的小白再作怪！？ \r\n不是強奪走我的目標就是偷走我的戰利品！我真的快要被他們煩死了！ \r\n請各位一同來將可惡的該死小白從這片美麗的草原上驅逐出去吧！\r\n\r\n完成條件：擊敗該死小白*10\r\n任務獎勵：金錢3000','','葛雷的冒險日誌-草原探險','葛雷',3,3,99,0,0,0,NULL,4,1,'226',10,0);
INSERT INTO `wog_mission_main` VALUES (40,'我終於找到這令人毛骨悚然的地方了！ \r\n這裡到處都是無名的墳墓或是慘遭丟棄的屍體，讓每個路過的人都不由得嚇出一身冷汗．．． \r\n可是我卻不得不來這裡，因為我前不久才剛想到一種尚未問世的新藥的藥品調劑方法 \r\n而這種新藥的材料剛好有一個是這裡才找得到的\"蟲草\" \r\n據說在沼澤裡面出沒的昆蟲怪獸身上可能帶有這種藥品，希望各位勇士能替我帶來這個藥品。 \r\n\r\n完成條件：蟲草*2\r\n任務獎勵：金錢5000，500經驗膠囊*2','','葛雷的冒險日誌-沼澤驚魂','葛雷',25,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (41,'滾滾的黃砂，與異常刺眼的烈日，我來到了一片鮮為人知的沙漠 \r\n在這片沙漠上，有著陶多多帶有濃厚民族色彩的部落 \r\n某天，我從部落中的一位朋友口中得知，要想在這片荒涼無比的沙漠中存活，必須隨身攜帶著一種沙漠住民的信物：沙漠之鷹 \r\n只要攜帶著這把銀長的彎刀，在沙漠中便幾乎可以橫行無阻了 \r\n然而，這種物品卻只有沙漠部落中的人才知道要如何取得這種物品，一般外來者幾乎不可能取得這種物品... \r\n不知道有沒有人能幫我弄到一把沙漠之鷹呢？\r\n據說沙漠之鷹在法老王身上\r\n\r\n完成條件：擊敗法老王，沙漠之鷹*1\r\n任務獎勵：毒蠍石*1','','葛雷的冒險日誌-荒漠之鷹','葛雷',50,3,99,0,0,0,NULL,4,10,'223',1,0);
INSERT INTO `wog_mission_main` VALUES (42,'滿佈著濃濃的白霧，以及未知植物遍處叢生的地方，就是這令眾人聞之無一不色變的迷霧森林 \r\n在森林中充滿著無數的危機，氣鬚長不見尾的老樹，不時散發著詭異笑聲的巨大植物，不知道何時會突然衝出來的古代機器，冒險者們會稱這裡是黑暗之森也不是不無道理的 \r\n然而，在這片森林中最為恐怖的，絕非變態花精末屬了 \r\n這種植物平常時會將自己埋藏在地上，偽裝成一叢毫不起眼的花草 \r\n等到一有人經過時，便會慢慢地跟在他的後面，只要時機成熟後便會突然地從目標後方跳出來，並將其一口吞下 \r\n這種恐怖的植物嚴重地威脅經過此處的村民以及行商 \r\n我與各個冒險同好們討論之後，決定到此處發表退治這群植物的委託 \r\n\r\n完成條件：擊敗變態花精*20\r\n任務獎勵：狡薵K*1，金錢6000','','葛雷的冒險日誌-迷霧異誌','葛雷',100,3,99,0,0,0,NULL,4,4,'35',20,0);
INSERT INTO `wog_mission_main` VALUES (43,'茂密的籐蔓攀附在一片片碩大的石塊上，漫無目的地生長、盛開著 \r\n地面上滿佈落著細小的砂石與艷綠的苔厥植物… \r\n這就是曾經繁華一時的洛裴旻王國…的遺跡 \r\n從內部看可以想見當時那繁榮至極的市集… \r\n四處腐朽敗壞的縱橫木條，以及上面似乎畫著每位水果的破舊布幔 \r\n實在令人無法想像為何這座城堡竟然會從歷史上消失？ \r\n經過多番調查之後，發現原來是國王所引發的災難… \r\n\r\n在當時，洛裴旻的國王為了強化國內的軍容，來確保人民的安全，避免遭受敵國的迫害 \r\n國王召集了數十位國內首驅一指的大魔導士，透過祕術將古代的強大守備兵器：怒神像從魔界召來… \r\n\r\n但是，國忘卻沒有想到召喚而來的怒神像竟然完全不受術者的控制，不停地殺害國內的人民… \r\n不過三日，洛裴民王國的歡樂之聲已經不復存在，取而代之的是臉帶著恐怖、絕望與殺戮的怒神像… \r\n\r\n如今，這群怒神像仍然存在這遺跡之中，不停地破壞著遺跡中的建築 \r\n為了不再讓這群恐怖的怒神像橫行於遺跡之中，希望有人能夠幫忙退治這群怒神像。\r\n\r\n完成條件：擊敗火怒神像*20\r\n任務獎勵：火砂*1，金錢10000','','葛雷的冒險日誌-淡忘的記憶','葛雷',230,3,99,0,0,0,NULL,4,5,'225',20,0);
INSERT INTO `wog_mission_main` VALUES (44,'遠從數十公尺外的地方就聞到一股令人不寒而慄的氣息，卻迫使人燃起想要前往一探究竟的慾望 \r\n朝向內心所指引的方向之後，那景像似乎傳正訴說著數千年前那場戰爭中那鮮紅的記憶 \r\n「棕紅色的土壤？為何會出現這種顏色的土呢？」當我把頭向四周看了之後才恍然大悟：那是血的顏色 \r\n到底要流下多少的鮮血才能使眼前這廣闊的土地染成令人驚駭的棕紅色呢？我不敢再多想 \r\n光是眼前那橫豎在地上的無數兵甲與白骨，就可略知一二了… \r\n\r\n那些光榮的戰士，不管他們是正亦邪，英勇地戰死沙場，卻無法得到他們仰賴的國君的弔慰 \r\n使得他們無法離開這裡，轉化成幽靈在這籠罩著鮮紅氣息的戰場上四處地徘徊、徬徨，他們臉上的表情顯得既英勇，又悽涼 \r\n\r\n為了使這群英勇的戰士們能夠安眠，勢必要賦予他們一股無可言喻的榮耀，與他們那勇敢的靈魂相呼應的信念，那就是全人類的希望，能夠賜予被授與者無限榮耀的『勇者魂』 \r\n然而，勇者魂卻是世界上少之又少的珍貴物品，一個人要擁有一個就已是非常的不容易了，要取的大量的更是幾乎不可能 \r\n眼看著這群無助的幽靈終日地徘徊在這令他們難捨的地方，著實令人不勝唏噓 \r\n因此在此發出蒐集勇者魂的請託，懇求各位拯救這群值得歌誦千古的靈魂吧！ \r\n\r\n完成條件：勇者魂*1\r\n任務獎勵：榮耀大盾，15000經驗膠囊*1','','葛雷的冒險日誌-榮耀之星','葛雷',1000,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (45,'我們精靈族在遠古時是一個極為強大的種族， \r\n可是不知為何，我們的能力被神限制住了… \r\n為了能讓精靈族可以繼續繁衍下去， \r\n我就在很久以前已經四散了族人們去尋找傳說中擁有強大力量的精靈聖物--六大精靈珠 \r\n現在，我快要死了… \r\n希望你可以替我集合六大精靈珠，讓精靈們可以在這世上平靜地生存下去吧。 \r\n六大精靈珠分別為--地、水、火、木、風、毒 精靈珠 \r\n請找到四散的精靈族人，他們可以告訴你有關精靈珠的事。 \r\n\r\n「精靈們就拜託你了…我們的勇者」 \r\n\r\n完成條件：大地精靈珠*1、清水精靈珠*1、烈火精靈珠*1、巨木精靈珠*1、旋風精靈珠*1、猛毒精靈珠*1\r\n任務獎勵：大精靈召喚，15000經驗膠囊*1','','六大精靈珠','精靈族大長老',920,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (46,'那坐落在荒野上的一片巨石團之中，隱藏著人類貪婪慾望的標地，以及魔物們最為憧憬的一片黑暗密境，那就是無淵洞窟。 \r\n\r\n在平日，洞窟的入口處便不時散發出陣陣足以迷惑人類心智的紫幻煙霧，吸引著人類的到來，使其在闇暗的洞窟中迷失方向，再伺機攫食，或是使其無限的黑暗棲息在人類之中。這一切的神秘現象的起源，便是那吸引著人類們來到此處的原因：罪惡的聖盃 \r\n\r\n這是傳說中的神器之一，會不停的產生出黑暗氣息，而這種黑暗氣息凝結之後，即會變成極為珍貴的黑耀魂的原石。然而，其產生出來的黑暗氣息卻足以使所有吸入這種氣息的生物變成惡魔的奴僕… \r\n\r\n我在某次的機會下找到了這只聖盃的所在地，然而，我卻被眼前那恐怖的景象給嚇得無法言語… \r\n無數的人們，在黑暗的煙霧中徘徊，露出極度飢渴的樣子，似乎想以他們手中那放出閃閃白光的武器消滅出現在他們眼前的所有事物… \r\n\r\n我決定將這聖盃封印，永遠的封印，絕不再讓任何人有何想找尋它的念頭。因此，我需要世界上最強的封印道具來將之封印，讓這黑暗的根源就此終止…。 \r\n\r\n完成條件：封印界環*1\r\n任務獎勵：9000經驗膠囊*4','','葛雷的冒險日誌-漆黑聖盃','葛雷',270,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (47,'那一天的月黑風高的夜晚，當時所發生的事至今仍然深深地刻印在我的心裡… \r\n\r\n如往常地，我持續的進行著我的冒險，不論是多麼危險、黑暗、恐怖的地方都是我羽毛筆下的圈痕 \r\n就在我圈著圈著的時候，突然發現一處炙手可熱的地點：王者之路 \r\n凡是追求更高境界的人們都必定會來到此處，為著夢想而努力。但也有無法克服此處艱辛的人們含恨消逝於此… \r\n既然我是為了追求更高的境界(冒險)而四處旅行，那麼這裡想當然爾我也得來一次才行 \r\n\r\n經過一段漫長的山路，以及無數的森林、危機，我終於看見那夢想的啟程點了！ \r\n然而，這裡的程度卻遠遠超出我的想像，不斷從暗處飛出的劇毒吹箭或是從森林裡發出激烈的刀劍聲，無依不使我膽戰心驚！ \r\n就在我為這種恐怖的場景而夢想快要幻滅之前，一位全身覆輓蛚薩ㄔ跓Z甲的戰士出現在我的眼前。 \r\n他告訴了我來到這裡時該做的事，並且要立刻習慣這裡的環境，要是連這種危險都無法克服的話只會離夢想越來越遠。 \r\n並且，他還說以冒險為目標的人必須要擁有一本可以隨時紀錄自己冒險紀錄的書 \r\n但是這時候該如何是好呢？要從王者之路出去是比進來還困難的，有無數的魔物會潛伏在優暗的草叢中，等待著懷著絕望而離去的人們，帶領他們進入更深的絕望… \r\n難道，我的夢想就要因而躊躇在這了嗎？\r\n\r\n完成條件：空白書．絢雲*1\r\n任務獎勵：15000經驗膠囊*2，金錢60000','','葛雷的冒險日誌-啟程之時','葛雷',900,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (48,'閃白的光芒不斷地射入我的眼眸，使我的眼睛幾乎無法張開，但是我卻無法退縮，因為這裡面有著我所追求的夢想 \r\n\r\n我的夢想，是成為一位冒險家，一位探究世界所有真理的探險家。因此，我在這裡絕對不能退怯，只要心生膽怯的話，我的夢想也就可能因此消失得無影無蹤。 \r\n\r\n而這裡，會有如此耀眼光芒的原因，其實是再簡單不過的了，因為這裡四周都是水晶。除了水晶之外還是水晶，整個洞穴似乎就只由水晶架構而成。據謠傳在這水晶洞窟的某處藏有一扇水晶製成的門，與其他的水晶一同豎立在這座洞窟之中。而在那扇水晶門的後面，可能就藏有我所追求的夢想的基石。 \r\n\r\n但是要找出這扇門卻非常的不容易。四周皆是同樣閃著白光的水晶，要在這之中找出一扇水晶門幾乎是不可能的事！而且洞窟中的兇猛魔物，很有可能使我在找到門之前就先命喪黃泉了。 \r\n幸好，並不是沒有方法找出這扇門的方法。但這方法似乎也不太可行，因為這必須要找到世界上罕有的珍品：冰漩之眼 \r\n這件物品可以完全的使水晶反射的光芒瞬間化為烏有，讓洞窟中那耀眼的光芒不再耀眼。 \r\n為此，在這裡請求各位能夠協助我找到那夢幻的物品！ \r\n\r\n委託物品：冰漩之眼*1\r\n報酬物品：120000 hp回復劑*2，真實水晶*1','','葛雷的冒險日誌-看穿真實之眼','葛雷',650,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (49,'這到底是什麼地方？我自己應該很清楚這個答案，但是眼前的景象卻令我不得不思考這個問題… \r\n細長而蔓延於昏暗天際的白雲，以及那破碎不堪的大地，這就是人類無法存活的地方，也是幻獸們最後能夠存活的淨地 \r\n不斷燃燒著熊熊烈火的火靈，或是能使方圓百里瞬間凍結的冰神，甚至是突然從你的視線內爬起來奔跑的仙人掌，無一不使我為之嘆為觀止… \r\n看到了這種景象，使我體認到從前的我是多麼的無知，視界多麼的狹小… \r\n世界是如此的廣大，可謂深不可測。為何我卻只看見眼前的光景，卻沒有看見那裹在世界另一面的地方呢？ \r\n\r\n為了記下我在這個地方的紀錄，我需要一些能夠代表這個地方的物品來當做寫作時的參考，不知道有沒有人能夠替我尋得這種物品呢？ \r\n\r\n委託物品：幻獸羽毛*1，封魔太刀*1，龍之爆彈*1，雷神珠*1\r\n報酬物品：160000 hp回復劑*2，幻獸的記憶*1','','葛雷的冒險日誌-真實的背側','葛雷',1100,3,99,0,48,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (50,'繼上次的旅途之後，我再次向著未知的地點探險，但這次，還有著另一項重大意義... \r\n在遠古之時，曾經出現一位能夠在超越天空的地方來去自人的英雄。 \r\n據說，他之所以能夠如此橫行於大空之中，是由於他穿的神奇鞋子的關係。 \r\n事隔數千年，我也與那位英雄一樣，來到了故事展開的起源，同時也是故事結束的地方，星河異界。 \r\n雖然英雄已炕A但是他的風采卻仍然留在這個空間之中。他的神奇鞋子，隨身攜帶的神奇石塊，以及四處發放的名片(?)，已被某些魔物們奪走… \r\n\r\n為了完成這次的冒險紀錄，勢必得將那些物品奪回來才行 \r\n若是能完成那位英雄的後續事蹟的話，他的歷史也或陳鈰鷕亃o更加完整了吧？ \r\n\r\n委託物品：破舊卡片*1，召喚石*1，Jordan鞋*1\r\n報酬物品：200000 hp回復劑*2，英雄書*1，20000經驗膠囊*2','','葛雷的冒險日誌-夢想的第二步','葛雷',1500,3,99,0,49,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (51,'據說最近在一處不知名的地方出現了一種讓各大美食家們都讚不絕口的食物 \r\n據說吃了之後，它會在口中徐徐溶化，散發出高貴濃郁的咖啡香氣 \r\n甚至還會使食用者的精神頓時飛入仙境中，體會世界上最不可思議的美景 \r\n聽了這麼動人的描敘之後我怎麼會不為之心動呢？只可惜我現在正在海軍中無法脫身去品嚐這到美食… \r\n若有人能為我帶來的話必定給予豐厚的報酬！\r\n\r\n委託物品：白輪蛋撻*1\r\n報酬物品：200000 hp回復劑*9，15000經驗膠囊*8，金錢 200000','','美食新指標','海軍新兵 K',860,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (52,'不好了！不好了！事情被我搞砸了！ \r\n昨天老師發給我們一項調配巨人生髮水的作業，發給每個人一條珍貴的巨人毛髮 \r\n但是我卻在準備調劑的時候才發現我的巨人毛髮竟然不見了！ \r\n怎麼辦，那可是一條就要數十萬元的珍貴物品啊，要是被老師發現我弄丟的話一定會被當掉的！ \r\n雖然我沒有辦法拿出這麼多錢，但是我對我所調劑出來的藥品很有信心！ \r\n凡是我調配出來的物品無一不在超乎水準之上的，因此希望能用我所調配的物品來交換一條巨人毛髮！\r\n\r\n委託物品：巨人毛髮*1\r\n報酬物品：元素溶劑*1','','巫師之藥','女巫艾琳',580,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (53,'我四處旅行時發現了一處溫泉，並且漁人村最出名的大美女，志玲大姐常到此處泡溫泉\r\n\r\n可是這條路上有很多高級鬥士，害我很難靠近\r\n\r\n能否替我解決這些高級鬥士，我將提供我偶然拍到的志玲大姐性感照片報答你\r\n\r\n完成條件：高級鬥士*10\r\n任務獎勵：性感照片*1','','溫泉中的美女','ETERNAL',190,1,99,0,0,0,NULL,2,7,'97',10,0);
INSERT INTO `wog_mission_main` VALUES (54,'從前有一位冒險家叫做莉吉亞，她仰慕著葛雷的故事，追隨著葛雷足跡四處冒險\r\n\r\n直到她旅行到久遠戰場時，發現到自己得到不治之症並且已經到了末期\r\n雖然我盡全力搶救，但是很可惜仍然宣告失敗，這件事讓我耿耿於懷\r\n\r\n希望你能替我取回莉吉亞留在戰場上的遺物\r\n\r\n委託物品：擊敗莉吉亞之魂，莉吉亞的遺物\r\n報酬物品：莉吉亞的遺作','','莉吉亞的遺憾','怪醫 白傑克',260,3,99,0,0,0,NULL,3,6,'224',1,0);
INSERT INTO `wog_mission_main` VALUES (55,'在十年前，克沙鎮是一座在灼熱沙漠邊境安靜平和的城鎮 \r\n四周被高山圍繞，所以鮮少有冒險者經過 \r\n但是，就在那一天，十年前的一個夜晚，我在教會的門口遇見了一位極需等待救援的少女 \r\n我看見她時她的身體上到處都是擦傷，左側臉頰上還留著一條細長的血跡… \r\n但是當時她卻不斷地對我說著：『神父，快逃！他們來了！再不逃的話就來不及了！』 \r\n我疑惑地問著她：『喔，我的主啊，在這夜黑風高的夜晚裡，這位小女孩您找我有什麼事呢？怎麼會如此地驚慌失措？請先進來休息一下吧。』 \r\n她哭著說：『求你了，拜託你快點逃離這裡！他們就要來了，這個城鎮就快要毀滅了啊…』 \r\n我還來不及問她到底發生了什麼事她就往西邊的另一個房子跑去，急忙地敲著房門，但卻慘被屋主怒罵，而繼續向西邊的下一個房子跑去。 \r\n\r\n就在我為這件事情感到疑惑不解時，另一邊，也就是東邊，忽然傳出了一陣爆炸聲！ \r\n東邊的村子廣場頓時被漫天烈火給吞噬了！我還尚未回神時，四周又突然爆出陣陣巨響！ \r\n以我身為神父的本能，我二話不說就往傳出爆炸聲的地方跑去… \r\n但是我跑到一半時，卻忽然覺得在這麼跑著似乎也沒用了，因為這時我早已知道了，我無法再救贖任何一個人… \r\n四周的火光不知為何突然消失，空氣又變得和往常一樣地平靜，日光也漸漸地從東方的山間徐徐升起。只有我還活著… \r\n\r\n在這十年來，我不斷地找出那些被害者的遺體，並將他們埋葬在教會的後方，不過並沒有找到當時那位女孩的遺體… \r\n但這不重要，因為現在仍然有釵h位村民的遺體尚未找到… \r\n遺體只要超過一年沒有被任何人觸碰過，便會轉化成活死屍。關於這點我已經見過太多例子了… \r\n但是這群活死屍們卻一天比一天的強大，怨念一天比一天的深，已經到了不是我一個神父就能夠解決的規模了… \r\n雖然不願意，但也只能夠藉由找尋願意前來擊敗他們的人來將他們強制送回天父的身邊了… \r\n\r\n完成條件：擊敗活死屍*20','','救贖靈魂','格斯特鎮神父 霍爾',210,3,99,0,0,0,NULL,1,10,'228',20,0);
INSERT INTO `wog_mission_main` VALUES (56,'我在兩年前來到了克沙鎮，原本是來探望在神父中頗有名望的霍爾神父 \r\n但卻沒想到克沙鎮已變成這副模樣，和人間煉獄幾乎只有一線之隔！ \r\n於是我決定要和神父一同來救贖這些可憐的生命，但情況卻演變成令人難以想像的局面… \r\n鎮中到處都是活死屍，不停地徬徨、躊躇在早已毀壞的建築物上 \r\n要拯救他們的方法只有兩種，一個是使屍體完全壞死，強制送回天父的身邊 \r\n而另一個方法則是使用聖水來洗滌他們的身體，以便承受天父的召喚時身體不會產生排斥 \r\n霍爾神父是負責找尋能夠強制送活死屍們回去的冒險者，而我則是負責調製聖水來使用 \r\n但是目前手邊的藥品已經漸漸地消耗光了，只剩下數星期還能夠再製作出聖水 \r\n因此希望各位天主所眷顧的冒險者們能夠幫忙蒐集這些藥品並送到克沙鎮來，願主保佑您。 \r\n\r\n完成條件：蟲草*5，天使之息*1，賢者手套*1\r\n任務獎勵：金錢50000','','神之光耀','克沙鎮修女 潔維爾',230,3,99,0,55,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (57,'十多年前我曾經是國家鍊金術師，當時接到一到命令，前往灼熱沙漠的邊境克沙鎮地底下，做一項很神秘恐怖的研究\r\n當時我們以活體生物，及死刑犯來做實驗，將牠們改造成合成獸，並控制牠們\r\n\r\n我的女兒當時也跟我一起居住在克沙鎮，我一直不敢告訴她爸爸在做什麼工作\r\n\r\n某日不明原因，研究所中的合成獸爆走\r\n造成研究所中心的反應爐爆炸，反應爐中的疫病毒器也蔓延整個克沙鎮\r\n\r\n在慌亂之中，我的女兒跟我失散\r\n而反應爐中心有一顆神秘珠子，也離奇失蹤\r\n\r\n數年來我不斷找尋我女兒，並且研究這疫病的解藥\r\n雖然聖水可以淨化死屍，但是無法解決疫病蔓延\r\n希望你能幫我收集解藥材料\r\n\r\n\r\n完成條件：聖潔之花*1，日蝕之花*2，月光花*2\r\n任務獎勵：120000 hp回復劑*5','','疫病解藥1','鍊術師 皮卡',240,3,99,0,56,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (58,'恭喜解藥順利製作完成，我現在必須動身去克沙鎮地底研究所灑下解藥\r\n但是裡面有很厲害的合成獸守護，讓我無法進入\r\n希望你能替我打敗合成獸\r\n\r\n完成條件：擊敗克沙鎮合成獸*5','','疫病解藥2','鍊術師 皮卡',240,3,99,0,57,0,NULL,1,10,'229',5,0);
INSERT INTO `wog_mission_main` VALUES (59,'偉大的冒險者，當你看到這封信時表示我已經不在人世了\r\n很謝謝你的協助，讓我彌補一些對克沙鎮人的楔?\n\r\n正當我準備跟中央城舉發這件醜聞時，遭到刺客暗殺\r\n派遣刺客來的人，正是這項實驗的負責人，國家鍊金術師指揮官 馬力歐\r\n在爆炸中失蹤的珠子正式傳聞中的猛毒精靈珠\r\n\r\n我猜測猛毒精靈珠應該是被他帶走\r\n希望你前往平原的中央城打敗馬力歐\r\n\r\n完成條件：打敗馬力歐','很可惜調查馬力歐住處，沒有發現到猛毒精靈珠\r\n根據馬力歐供詞，無淵魔導師是猛毒精靈珠提供者，並且主導整個合成獸研究\r\n\r\n或鳥蒤荍J沙鎮事件只是無淵魔導師計畫之一','皮卡的遺言','鍊術師 皮卡',250,3,99,0,58,0,NULL,1,1,'230',1,0);
INSERT INTO `wog_mission_main` VALUES (60,'中央王城下令討伐無淵洞窟的無淵魔導師\r\n\r\n完成條件：無淵魔導師\r\n任務獎勵：猛毒精靈珠，160000 hp回復劑*5','','主謀','中央城王令',255,3,99,0,59,0,NULL,1,11,'231',1,0);
INSERT INTO `wog_mission_main` VALUES (61,'我是鍊金術師皮卡的女兒 吉絲很感謝你把我從無淵魔導師手中救出來當年克沙鎮毀滅時，我被無淵魔導師帶走\r\n\r\n不過無淵魔導師卻沒有加害於我，也沒有限制我的行動在相處的這幾年來，他告訴我，他的過去\r\n\r\n無淵魔導師本名亞斯迪，出生在克沙鎮由於天生具有強大的魔力，受到村人的異樣眼光看待，甚至被人認為是怪物只有從小一起長大，亞斯迪所摯愛的情人 雷茵，認同他並接受他\r\n\r\n某日由於亞斯迪的預言成真，村人懼怕亞斯迪的存在，放火燒死亞斯迪的親人亞斯迪與雷茵一路逃命，在逃命的途中遭遇到克沙鎮村民僱來的傭兵所殺害亞斯迪用著最後一口氣躲入無淵洞窟，之後被人稱為可怕的無淵魔導師\r\n\r\n我想這一切是亞斯迪的復仇吧 唉... 請幫我找些東西來解放亞斯迪的怨念 \r\n\r\n完成條件：陽光盒*1，星星髮夾，珍珠*2，水晶碎片*1\r\n任務獎勵：亞斯迪手套，雷茵的祝福','','無淵魔導師的過去','吉絲',255,3,99,0,60,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (62,'昨天媽媽新買回來了一組玻璃杯，外觀看起來非常的華麗 於是我索性把玻璃杯拿起來仔細的看了看，卻不小心掉到地上摔破了！ \r\n怎麼辦？雖然破掉的玻璃杯已經藏在倉庫裡面了，但是卻不能夠永遠瞞過媽媽啊 聽說粘稠液體是一種不管什麼東西都能粘得起來的神奇液體，應該也可以拿來粘住壞掉的玻璃杯吧？ 拜託大家幫我找找看這種液體的下落！ \r\n\r\n完成條件：黏稠液體*5 \r\n任務獎勵：玻璃杯*1','','玻璃杯的修理','白石鎮 小男孩',48,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (63,'我昨天才剛買的一架豪華大鋼琴裡面居然有一條鋼線壞掉了！ 而且裡頭的木頭竟然還有部分被蟲蛀食！我看到的時候差點沒昏倒… \r\n結果要去找那家店的老闆修理時，老闆竟然說他們不負責鋼琴的事後維修工作...！ 真是快要氣死我了！但是沒有辦法，也只好請人來幫忙修理一下這架鋼琴了...。 \r\n\r\n完成條件：生繡鐵釘*3 ，木材*5，蜘蛛絲*5\r\n任務獎勵：輕旋律樂譜*1','','鋼琴的修理','白石鎮 氣質少女',48,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (64,'每當隔壁的氣質少女開始彈琴時，優美的旋律總是讓我如癡如醉以及專注的神情總是讓我不襟想多看她一眼 我想到一個方法，就是彈吉他來吸引她的注意請你幫我收集製作吉他的材料 \r\n\r\n完成條件：木材*1，蜘蛛絲*3，硬殼*2 ','','一把吉他','白石鎮 陽光少年',49,3,99,0,63,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (65,'很謝謝你幫忙製作的吉他每次只要我一開始彈吉他，就會傳來狗的哀號聲以及左鄰右舍關門關窗的聲音我想我該好好加強一下我演奏技巧 \r\n\r\n完成條件：五音譜*1\r\n任務獎勵：吉他譜*1','','震撼人心的樂曲','白石鎮 陽光少年',50,3,99,0,64,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (66,'以前我在迷霧森林遇到了一個從亞魯多古堡內逃出來的女奴… \r\n她傷得非常非常的重，以一個普通女子的體質來說應該早已經挨不住死了。 \r\n但她仍然一直在爬…爬到我的面前，並大喊了： 「請解救我的姊妹！！」就斷氣了。\r\n 雖然有女奴逃出的事是不足為奇， 但是我每晚一夢到那女奴痛苦的神情和充滿堅毅的聲音， 我就很想很想去幫助她。 \r\n我曾到過城內探查過， 費了一番奶牷A我終於找到了女奴們居住的秘室； 可是，很奇怪…非常奇怪… 這真是奴隸們居住的地方嗎？她們的臉上總掛著害怕的表情。 \r\n\r\n每隔一次探查，都總會有一些女奴們不見了…這究竟是什麼回事!? 但總之，我知道這一定不會是好事 夠了…真是夠了！可憐老娘我對著森嚴的守衛只感到有心無力 每次看見這些生活在這可悲的命運底下的女子們，我很無奈 強而有力的冒險者！你願意和老娘一起解救她們嗎？ \r\n當我看見你時，我就知道命運改變的一刻已經來臨！ 「我們是為了每一個生命應有的希望和權利而戰的！」 \r\n\r\n完成條件：打敗女奴警衛*15','','解放女奴','酒吧老闆娘',120,3,99,0,0,0,NULL,3,4,'232',15,0);
INSERT INTO `wog_mission_main` VALUES (67,'===========[公告]=========== \r\n勇者們，我的女兒亞妮亞… \r\n被身處在最果之島的水龍擄走了！ 能救亞妮亞者，必有重酬。 \r\n亞魯多城城主 示 \r\n============================ \r\n那個可惡的城主，我應該幫助他嗎？ \r\n最果之島…好像很遠的樣子，我想我先要弄一艘好船。 \r\n\r\n完成條件：木材*9，橡膠*5，巨人毛髮*3','偉大的冒險者，你總算追到這裡\r\n\r\n亞魯多祖先在三百年前，找來了數十位法力高強的魔導師，設下水龍封印結界活抓了我\r\n並與我訂下契約，每月供應女性祭品給水龍，可以獲得水龍之力\r\n使得亞魯多家族平均壽命超越常人\r\n原本位於海岸邊的亞魯多古城，周圍終年風平浪靜\r\n\r\n但是隨著時間流逝，封印日漸減弱\r\n在一次的機緣下，亞妮亞解放了封印，於是我帶著亞妮亞逃到這裡來\r\n\r\n你現在有兩種選擇\r\n1.挑戰水龍\r\n2.討伐亞魯多城主','亞妮亞','亞魯多城主',120,3,99,0,66,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (68,'前往最果之島挑戰水龍\r\n\r\n完成條件：打敗最果水龍\r\n任務獎勵：水龍劍','','挑戰最果水龍','亞魯多城主',120,3,99,0,67,69,NULL,3,15,'233',1,0);
INSERT INTO `wog_mission_main` VALUES (69,'前往迷霧森林討伐亞魯多城主\r\n\r\n完成條件：打敗亞魯多城主\r\n任務獎勵：暗影之火','','討伐亞魯多城主','最果水龍',120,3,99,0,67,68,NULL,3,4,'234',1,0);
INSERT INTO `wog_mission_main` VALUES (70,'海上的旅行雖然吸引了釵h的年輕冒險者們爭相前往，但這些人或陶ㄓㄙ器D，海上其實隱藏著非常多的危險的… \r\n\r\n在位於漁人碼頭東南百餘海浬的地方，有著一群天然海礁。這群海礁的附近常常散佈著伸手不見五指的濃霧，令釵h的船在經過這裡時往往會觸撞到暗礁而不幸沉船。 \r\n但是，沉船的原因其實不單只是濃霧而已…另一個原因就是因為這裡的暗礁上棲息著一種恐怖的魔物，那些僥倖從沉船意外中存活下來的人都稱呼她為『賽蓮女妖』 \r\n根據他們的描述，當賽蓮女妖看見有船隻經過的時候，便會開始用她那能夠媚惑男性的歌聲使得船員們為之入迷，就連船碰觸到暗礁時也渾然不知… \r\n賽蓮女妖的歌聲已經嚴重地危害到所有經過的船員們的性命，為此在這裡發出公告能夠找到願意前往退治的勇者。 \r\n\r\n完成條件：擊敗 賽蓮女妖*5\r\n任務獎勵：賽蓮豎琴','','海上的魔女','漁人碼頭村長 周漁民',900,2,99,0,0,0,NULL,2,14,'235',5,0);
INSERT INTO `wog_mission_main` VALUES (71,'海上的旅行雖然吸引了釵h的年輕冒險者們爭相前往，但這些人或陶ㄓㄙ器D，海上其實隱藏著非常多的危險的… \r\n\r\n在海上，時常會颳起陣陣的強風，或是接連下起長達數天的暴風雨，這些其實都是風水靈搞的鬼！ \r\n他們是一群喜歡在海上興風作浪的精靈，這與他們的習俗有關，這裡就先不談這個。 \r\n為了能使在海上旅行的朋友們能夠安然無恙的航行，希望有人能夠前往治退他們。 \r\n\r\n完成條件：擊敗 風水靈*15\r\n任務獎勵：風神珠*1','','碧藍之海與風水靈','漁人碼頭村長 周漁民',950,3,99,0,0,0,NULL,2,14,'203',15,0);
INSERT INTO `wog_mission_main` VALUES (72,'最近上級派給我一個特別的任務，要我們將一千條美味鮪魚送到海軍食品料理中心 \r\n但是從這裡到料理中心的路程必須花費三天，這一千條鮪魚恐怕會在運送的途中就全部變質了 \r\n幸好聽說只要將大量的冰塊放在這些鮪魚中一起存放的話就可以延長這些鮪魚的保存期限 \r\n不知道有沒有人能夠提供我們一些冰塊呢？\r\n\r\n完成條件：冰塊*4\r\n任務獎勵：寒冰弓','','食品保鮮計畫','海軍新兵K',520,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (73,'路行鳥好可愛喔??！ \r\n看它那美麗豐滿又帶有迷人金黃色澤的羽毛，以及那強健的雙腳，還有那炯炯有神迷死人不償命的汪汪大眼 \r\n真是可愛到不行啊！拜託大家能夠幫我帶回來一隻可愛的路行鳥，我願意付出等價的報酬！ \r\n\r\n完成條件：捕捉 幻獸 路行鳥\r\n任務獎勵：寵物 幻獸 不死鳥','','寵物之夢','鄰家女孩',700,3,99,0,0,0,NULL,4,0,'0',0,114);
INSERT INTO `wog_mission_main` VALUES (74,'遠古之時，有一位偉大的詩人，創作了數篇震撼當代的奇蹟詩集 \r\n\r\n如今，這些詩集卻早已不知去向，其內容更是無人知曉… \r\n希望有人能夠協尋找出這些失落的珍寶。\r\n\r\n完成條件：風之詩集*1，花之詩集*1，雪之詩集*1，月之詩集*1','','風花雪月之詩','詩人 艾亞斯',35,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (75,'遠古之時，有一位偉大的詩人，創作了數篇震撼當代的奇蹟詩集 \r\n\r\n如今，這些詩集卻早已不知去向，其內容更是無人知曉… \r\n希望有人能夠協尋找出這些失落的珍寶。 \r\n\r\n完成條件：奇之詩集*1，山之詩集*1，異之詩集*1，水之詩集*1','','奇山異水之詩','詩人 艾亞斯',36,3,99,0,74,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (76,'遠古之時，有一位偉大的詩人，創作了數篇震撼當代的奇蹟詩集 \r\n\r\n如今，這些詩集卻早已不知去向，其內容更是無人知曉… \r\n希望有人能夠協尋找出這些失落的珍寶。 \r\n\r\n完成條件：春之詩集*1，夏之詩集*1，秋之詩集*1，冬之詩集*1\r\n任務獎勵：四時帽','','四時之詩','詩人 艾亞斯',37,3,99,0,75,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (77,'遠古之時，有一位偉大的詩人，創作了數篇震撼當代的奇蹟詩集 \r\n\r\n如今，這些詩集卻早已不知去向，其內容更是無人知曉… \r\n希望有人能夠協尋找出這些失落的珍寶。 \r\n\r\n完成條件：炎之詩集*1，瀧之詩集*1，砂之詩集*1，嵐之詩集*1\r\n任務獎勵：精靈口語','','精靈之詩','詩人 艾亞斯',38,3,99,0,76,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (78,'我已經看過了陶多多的詩集和文章。但是，這些詩文卻只適合存在於當時，不適合現在，這是我對這些詩經的看法。 \r\n\r\n要使現代的人們喜好詩文、嬝疙痐憛A那麼只有這些描述古代的文字是不夠的，還必須有現在的文字才能夠從兩者中真正理解古代文章的意義，盡情遨遊於詩文之中；並能夠充分理解現代詩詞那充滿美麗與感性的文字。 \r\n為此，我希望能夠寫出一本屬於現在與我的詩集，即使必須花上數十年也在所不惜。 \r\n但是要寫出一本詩集所必備的物品卻極為難求，所以只能夠藉由委託來準備這些物品了。\r\n\r\n完成條件：天堂羽毛*1，魔法染料*1，古書*1\r\n任務獎勵：艾亞斯詩集','','從古時到當代','詩人 艾亞斯',850,3,99,0,77,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (79,'來，那邊那位?沒錯，就是你，不要懷疑！ \r\n還記得我嗎？沒錯，就是我！世界最厲害的矮人鐵匠！ \r\n上次你交給我的那批東西所打造出來的東西真的是好得不像話啊！持起劍柄時的感覺就像沒有拿著東西一般的輕盈！ \r\n而且劍端不時閃爍著耀眼的光芒，令人一看見便眼睛為之一亮！ \r\n然而呢，我發現這把劍雖然是如此的好，但是還缺少著一種極為重要的要素。 \r\n相信聰明的你已經想出來是什麼了。沒錯，就是它的色澤！ \r\n雖然它有著無與倫比的鋒芒，但卻缺少了散發鋒芒時的耀眼色澤，要是能夠添加些美麗的色彩的話必定會為它帶來更為傑出的外表！ \r\n希望你能夠再幫我找來一些能夠加上鮮豔色彩的物品，以完成這把登峰造極的武器！\r\n\r\n完成條件：黃金*5，魔法染料*1，白色布料*1\r\n任務獎勵：耀芒長劍，耀芒弓','','鋒芒交會之時','矮人鐵匠',130,3,99,0,14,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (80,'聽爸爸說世界上有釵h非常傑出的冒險者們在他們小時候就已經立定志向，並全力朝著他們的目標而邁進！ \r\n當我聽到的時候覺得非常感動，並且希望能夠傚法他們及時立定目標來決定未來！ \r\n當我在思考這個問題的時候，最先浮現我在我心中的答案，就是劍士！ \r\n劍士們是手持著一把代表著他們自信的長劍而四處旅行的人，從前的我原本非常瞧不起這種人，但是自從那一天起，我的想法大概就被他改變了… \r\n\r\n約一年前，媽媽叫我去村子的後山中找一些可食用的香菇來當作晚尷滌t菜，於是我便帶著愉快的心情跑到了山中去找香菇。 \r\n找著找著，就在我找到一朵巨大的香菇而渾然忘我時，我的後面突然出現了一隻不懷好意的魔蝕精準備要攻擊我！ \r\n就在我覺得小命休矣而頭暈準備倒下時，那隻魔蝕精突然靜止不動，並且緩緩地倒下，化為一攤液體！ \r\n雖然那時候沒有看清楚救我的人是誰，但是看見他右手所拿的長劍時就知道了，他是一位劍士，一位及時拯救了我的劍士。 \r\n\r\n現在，我決定要成為一位能夠和他一樣厲害的劍士，準備從我的家鄉啟程到王城中接受劍士的學習。 \r\n不過，聽說要到城中學習劍士的要領的時候，必須隨身配戴著一隻鬥志指輪，以防止自己因為無法忍受煎熬而半途而廢。 \r\n希望有人能幫我找到這只指輪。\r\n\r\n完成條件：鬥志指輪*1\r\n任務獎勵：500經驗膠囊*3','','始動','村中小孩 赫德',39,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (81,'近日為強化國家城牆結構以抵禦並防止魔物的入侵，必須蒐集大量火藥以撤除舊有城牆 \r\n在此發出公告徵求火藥材料，請手中持有相關物品者踴躍捐出。 \r\n\r\n完成條件：火藥*5','','初等炸藥材料委託','國家中央守備處 司令官',310,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (82,'近日為增進國家社會貿易弁遄A必須重新整治部分街道與建築 \r\n為此需要大量炸藥以撤除舊有建築物 \r\n在此發出公告徵求火藥材料，請手中持有相關物品者踴躍捐出。\r\n\r\n完成條件：火藥*5，火砂*3','','中等炸藥材料委託','國家中央建築處 司令官',310,3,99,0,81,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (83,'近日為強化國家軍事武力，必須重新配置火藥成分結構以製作強力火藥基礎軍備 \r\n在此發出公告徵求火藥材料與製作表，請手中持有相關物品者踴躍捐出。 \r\n\r\n委託物品：火藥成分配合表*1，火藥*4，火砂*4，龍磷*1','','上等炸藥材料委託','國家中央軍備處 司令官',310,3,99,0,82,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (84,'近日為強化國家軍事武力，必須重新配置火藥成分結構以製作新型火藥基礎軍備 \r\n在此發出公告徵求火藥材料與製作表，請手中持有相關物品者踴躍捐出。 \r\n\r\n委託物品：新式火藥劑量表*1，火砂*1，魔法水*1，雷神珠*1\r\n任務獎勵：新式炸藥*1','','新式炸藥材料委託','國家中央軍備處 司令官',310,3,99,0,83,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (85,'聽說這世上最美味的海鮮，就是鮑魚。 \r\n聽說在沒人知道的深海裡面，住著一種極為兇猛的鮑魚。 \r\n此魚不同於其他普通品種，毒性強到可以毒死一頭抹香鯨！所以沒有兩三把刷子的人，是會慘死魚吻之中。 \r\n我希望你能夠幫我抓來，並且在回來的平原中，帶回一把能解天下奇毒的解毒草，用來剋制住鮑魚毒性。 \r\n對了！為了保持它的新鮮度，請你再拿回來的路上用冰塊幫他保存好。 \r\n\r\n完成條件：毒鮑魚(捕捉)，解毒草*1，冰塊*1\r\n任務獎勵：魚鱗*1，鮑魚小刀\r\n','','傳說中的偉大料理','食神馬克',350,3,99,0,0,0,NULL,1,0,'0',0,206);
INSERT INTO `wog_mission_main` VALUES (86,'看那碧青色的大海，是多麼地皓渺，多麼地透徹！ \r\n實在無法讓人想像在這麼美麗的地方上竟然會有這處無法想像的地方存在… \r\n這裡是位於中央大陸終南岸的海邊。平時，這裡總是籠罩著烏黑的雨雲，並且斷斷續續地吹著爆發性的狂風，只要一不注意便會被這恐懼般的狂風給捲走！ \r\n為此，這裡罕見人跡，除了像我這麼悠閒的人之外。 \r\n但也因為這裡罕見人的走動，所以也就蘊藏著陶多多不為人知的秘密！ \r\n就像這次，我沿著海岸一邊抵禦著強風的吹襲一邊走著，總算是讓我找到了一處可以躲避風雨的海蝕洞了。 \r\n等到我進去了之後，我發現在洞的內部竟然存在著一個幽暗的巨大身影！？ \r\n靠近一看，更赫然發現這黑影原來正是一艘在古書中記載著早已失蹤數百年的古船！ \r\n\r\n經過了數百年的洗禮，船的龍骨早已腐壞，甲板上更是遍地坑洞，稍有失神便會掉了下去。 \r\n而在船的四周，則有著陶多多的魚類。或閉O將這艘船當作是洞窟來居住的吧？ \r\n原本我以為這裡就像是仙境般的美妙，如天堂般的平靜。但卻沒想到，在這潮濕無比的地域中竟然會出現火之亡靈！ \r\n這些火之亡靈根據我的調查原本是在這附近死去而徘徊的動物們的靈魂。可能是受到近日位於中央大陸終南岸更南方的次元之門出現異變的影響而強制轉化成火之亡靈。 \r\n\r\n不管這些火之亡靈的來源為何，他們的存在已經嚴重威脅到原本生活在這裡的生物們。因為他們的突然出現，使得釵h的魚類因為水溫驟昇而燙死，洞窟中的附巖植物更是被燒得慘不忍睹，而這些死去的生命也有極大的可能轉化成火之亡靈使得惡況持續循環下去！ \r\n為了不讓這樣的慘劇持續下去，希望有勇敢的人能夠前來消滅這群不該出現在這裡的生命！ \r\n不過，次元之門的異變或釵野痍n好好底調查一番才行… \r\n\r\n完成條件：擊敗 火之亡靈*20\r\n任務獎勵：異變之火*1','','葛雷的冒險日誌-異變','葛雷',1150,3,99,0,0,0,NULL,4,14,'252',20,0);
INSERT INTO `wog_mission_main` VALUES (87,'根據我的私人秘密情報網得知，要前往次元之門的話必須從這裡開始往東走，繞過巨石林的東側山道翻越山頂後便能找到世界上唯一會開往那邊的港口：柏凡亞之港 \r\n而就在我為了前往柏凡亞之港而翻越山谷時，在險峻的道路旁忽然看見一位長著翅膀的鳥人！ \r\n當我前往表示善意時，這位鳥人竟然也熱情地歡迎我的到訪！於是我們便在路邊聊了開來。 \r\n當他一開口時，他的第一句話便直直地命中了我的好奇中心。 \r\n『你是不是也覺得我長得很奇怪？』 \r\n我原本不敢直接的回答他，但又難掩心中的好奇，也使得他從我當時的表情便能得知了，我很好奇。 \r\n『你想知道我為何會長成這樣嗎？』 \r\n他的一句話又不偏不倚地刺進了我的要害，於是我決定直截了當地問他。 \r\n\r\n根據他的回答中得知，他原先是中央大陸的士兵，因為一次跟魔法王國的戰役而淪為俘虜。 \r\n被擄回魔法王國的他，接受了王國中的秘密魔法實驗不幸失敗遭受惡魔的詛咒而變成了鳥人。 \r\n而那些實驗失敗的人們原本是注定要被抹去的，但是他為了不被抹殺而趁著一天夜黑風高的夜晚從自己暗地挖掘的密道中逃出。 \r\n但是外觀已變成了鳥人的他並不被人類的社會所接受，最後而流浪到了這座位於世界邊垂的巨石林。 \r\n\r\n從我以前旅行的紀錄中來看，要從惡魔的詛咒中解脫並不是不可能的，但是必須準備好與該種詛咒相對等的強力聖魔法才能解除。 \r\n雖然夫拉多表示他並不討厭身為鳥人的自己，但我從他所說的內容中得知最近在睡覺時常常做從前不曾做過的噩夢，而且在空中飛翔的時候也時常精神恍惚。 \r\n這種現象可能也與次元之門的異變有所關聯。為了不讓最壞的情況發生，希望大家能幫我找出下列物品以及一件布衣，好讓夫拉多能早點從詛咒中解脫，否則結果真的不堪設想… \r\n\r\n完成條件：辟邪石*1，布衣*1\r\n任務獎勵：夫拉多羽毛*1','','葛雷的冒險日誌-半鳥人之心','葛雷',380,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (88,'這就是隱藏在世界末端的港口嗎？這裡的熱鬧真的是無法形容的！ \r\n從懸崖上俯視下去，街上到處都是賣這各式商品的攤販，以及絡繹不絕的人群！ \r\n攤販們不斷地競相叫賣著自己的商品，而人們的臉上則是充滿著笑容，似乎看不到一絲空寂的地方 \r\n\r\n我到港口附近的酒館中稍微探聽點與次元之門相關的情報，卻沒想到竟然沒有一個人知道！？ \r\n這怎麼可能呢？那影響到全大陸的異常現象竟然會沒有人知道，甚至連聽都沒聽過？ \r\n就在我百思不解的時候，酒館主人暗暗地拍了我的肩膀一下。 \r\n『嗯？看你到處問人問題，你有什麼事情想打聽的嗎？若是要打聽情報的話直接問我就好了，我手邊可是握有各式各樣的情報喔！』 \r\n我二話不說的問他：「你知道次元之門的情報嗎?」 \r\n『唉呀，雖然想問你為什麼想知道次元之門的情報，不過我每次問的結果都是無它茠臐K好吧，我就告訴你吧，不過必須先給相對的情報價格。』 \r\n我拿了一袋十萬元的金幣給他之後，他就開始小聲地說著。 \r\n\r\n當我聽完主人說的話之後感到非常的震驚！ \r\n酒館主人說次元之門的異變其實與一個叫做天空之城的地方有著莫大的關聯，但是實際有著什麼關係上他也不是很清楚… \r\n天空之城？難道要我飛上天空去找嗎？那要該如何上去呢？上去之後又要如何下來呢？… \r\n總之現在應該不是擔心這個的時候，目前最重要的還是要想個方法拿到開往次元之門的船票才行，希望有人能夠幫我弄到一張。 \r\n\r\n完成條件：萬用船票*1','','葛雷的冒險日誌-柏凡亞之港','葛雷',1200,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (89,'大約四個月前，在大陸東方一片海域，一處有著能掃清一切思緒的白色的海域，到過那邊的人們都稱那邊叫做\"無限白\"。 \r\n那淨白無暇的海域上空突然出現了一道似乎連大陸西方的人都能看見的轟雷，打落在無限白的一處無人島上。 \r\n就從那時候開始，無限白變得不在白皙…它的上空出現了濃密的迷霧，阻礙了照射到海面上的光線，使得那邊瞬間成為了\"無限灰\"… \r\n雖然那邊跟我沒有什麼關係，但是卻不知道為什麼無法對那邊的異狀棄之不顧 \r\n這樣可能會有點過分，但希望有人能夠給我一雙望遠鏡，以便能夠更清楚地看見那邊的異狀 \r\n若有人能夠幫我帶來這樣東西的話，我願意以一張能夠隨時搭上任何船隻的超方便船票作為謝禮。 \r\n\r\n完成條件：望遠鏡*1 \r\n任務獎勵：萬用船票*1','','白海的海鷗','港口的船員',1200,3,99,0,0,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (90,'到達次元之門的方法已經有了，所以現在只需要等會到達次元之門的船出現就可以了。 \r\n這是我第一次搭船離開這塊大陸，意味著我已向我的目標邁出了一大步… \r\n曾經有人問過我為何會想當個冒險家，而不從事其他更輕鬆的職業。這其實與我的父親有著相當深遠的關係… \r\n\r\n我的父親，艾伯羅．雷格，是一位名聲傳遍全世界的大冒險家。 \r\n凡是他所到之處，必定會留下一篇永垂不朽的冒險誌，以及一具當地最強魔物的屍體。 \r\n我就是看著父親的背影下成長的，當時的我深深的以如此利害的父親為榮，並也就此下定瘸新自己也要成為和父親一樣利害的冒險家！ \r\n但卻沒想到，就在我十五歲的那一年，父親卻在一次與大惡魔的戰鬥中不幸戰死… \r\n雖然當時父親的死給了我極大的震撼，但我卻也沒有因此而放棄了我的決定！雖然父親已死，但是他當年那威風凌凌而又帶有風趣的意志卻早已深刻地烙印在我的心中，鮮明地活在我的記憶中… \r\n\r\n如今，在這重要的時刻，為了告訴父親我已經快要追趕上他當年時的腳步，我希望能夠帶著三朵純真無垢的聖潔之花去他的墳墓上祭拜。 \r\n然而聖潔之花卻也不是這麼好找的，要是在找花的途中錯過了到次元之門的傳的話就不知道要再等多久才會出現了… \r\n若是有人身邊有著一些聖潔之花的話希望能夠將它讓渡給我，我願意以後禮回報。 \r\n\r\n完成條件：聖潔之花*3\r\n任務獎勵：艾伯羅-雷格項鍊*1','','葛雷的冒險日誌-繼承','葛雷',1220,3,99,0,88,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (91,'據說位於大陸西南側的古代遺跡中藏有一筆天文數字的財富，誰能得到這筆財富，誰就能夠成為世界第一的大奸…不，是大富豪！ \r\n可是要我去那邊拿著小得可憐的鏟子像個傻子般地挖著真是沒效率了，這時候當然就要動用高效率的挖掘祕器：挖掘機 來幫我服務囉！ \r\n在此我以一個尚未公佈於世的秘密計畫草案來收購挖掘機，家裡有用不到的挖掘機的愚…不，家裡有用不到的挖掘機的貴民們請好好地把握這次的良機吧！ \r\n\r\n完成條件：捕捉 挖掘機 \r\n任務獎勵：內裂火藥的構想*1','','秘密挖掘委託','富豪 比爾誑\0',400,3,99,0,0,0,NULL,3,0,'0',0,148);
INSERT INTO `wog_mission_main` VALUES (92,'我做的火藥是眾人公認的，凡是我親手做出的火藥無一不能炸毀一塊重達數十噸的巨石，但如今我卻碰到了難題！ \r\n前幾天在偶然的機會下，我以我的得意炸藥試炸一塊平凡無奇的鋼塊，卻出乎我意料之外的，這塊鋼塊經過了我的強力炸藥的洗禮後竟然毫髮無傷！？ \r\n這件事使我不得不反省自己所做的火藥是否還不夠有威力，但想了酗[卻始終想不出有什麼好方法可以提升火藥的殺傷力，因此希望有人能夠提供我一些寶貴的意見。 \r\n\r\n完成條件：古書*1，新式火藥劑量表*1\r\n任務獎勵：內裂火藥*1 ','','未見的曙光','炸藥技師 鮑伯',400,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (93,'為了從巫師學院畢業，每位學生都必須通過巫師畢業考試才能夠脫離學院的魔爪(?)… \r\n而考試的成績只要達到M就算是及格了，但卻沒想到我竟然只有得到T(山怪).. \r\n怎麼辦？憑我的這點成績連踏出學院的資格都沒有，更別說要從學院畢業了… \r\n聽說世界上有種能夠使頭腦清醒的藥水，說不定能幫我度過這次的難關，請各位幫幫我！\r\n\r\n完成條件：魔法水*8，妖精之水*8\r\n任務獎勵：火閃電掃帚','','巫師畢業考試','女巫艾琳',420,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (94,'『名字是？』 \r\n「涅魂。」 \r\n『你恨嗎？』 \r\n「都是因為那些傢伙，使得我的村莊從此不復存在…更可惡的事，他們在事後甚至還用輕蔑的口氣來嘲諷我的無力…」 \r\n『願望是？』 \r\n「把他們全部拖下地獄！」 \r\n『幫你傳達你的怨恨…』 \r\n\r\n完成條件：擊敗 黑暗魔蝕精*12\r\n任務獎勵：金錢12000','','來自地獄的復仇聲','浪跡者',32,3,99,0,0,0,NULL,1,3,'27',12,0);
INSERT INTO `wog_mission_main` VALUES (95,'在數天前，我獨自經過幻獸森林的邊緣時，因為被森林中傳來的神秘香氣吸引而走進去… \r\n等到我驚覺事態嚴重時，卻怎麼走也走不出森林… \r\n就在此時，我看見了！在我的眼前的一處矮灌樹叢的後面，有著一頭散發著白色神秘光芒的猛獸！ \r\n因為它發出的光芒實在是太強了，以至於沒辦法看清楚它的長相。 \r\n但就在這剎那間，我的身體似乎被一股強大的電流擊中，眼前的畫面頓時轉為模糊，神智不清地倒了下去… \r\n而等到我醒來的時候，卻發現我人竟然是暈倒在森林的外頭！？ \r\n\r\n雖然這只是剎那間的接觸，但是卻令我不由得想再看見一次當時的那頭白色巨獸… \r\n雖然有可能只是我的錯覺，但還是希望有經驗豐富的人們能夠幫我確認一下那頭白色巨獸是否真的存在。 \r\n\r\n完成條件：捕捉 幻獸 白虎\r\n任務獎勵：美白面膜*1','','雪白幻影','白膚色的少年',430,2,99,0,0,0,NULL,3,0,'0',0,255);
INSERT INTO `wog_mission_main` VALUES (96,'約費了數十天航程，歷經了一連串的洶湧海濤，以及令人震懾的狂風暴雨，這艘船總算是到達了次元之門所在的島嶼。 \r\n島上佈滿著群群爭艷的花草，與恣意遨遊的鳥。各種在大陸上隨意可見的風景，就像是原封不動地轉移到了這裡。除了一個地方。 \r\n\r\n位於島的正中央，座落著一座超越人類一切知識的金黃色建築，輪轉之門。 \r\n在門的周圍有著陶多多散發著彩色光芒的光珠環繞，為這座次元之門更添增了釵h神秘色彩。 \r\n傳說中只要帶著神所喜愛的物品來到這座次元之門，神便會欣喜而將該人送往他所想去的地點。 \r\n雖然這只是一個不可靠的謠言，是真是假還不能斷定，但它的神秘卻吸引著釵h的人們前來參觀。即使最近次元之門出現了未知的異變但還是阻擋不了遊客們的好奇心。 \r\n\r\n但是，當我一看見次元之門時，卻不知為何地心中突然悸動了一下，彷彿是看見了令人懷念的事物，腦中突然閃現出了一個從未見過的景象… \r\n那是什麼？與我目前所處的地方迥然不同的世界；高聳的雪白建築，樹立在高處的光芒…為什麼我會突然想起這些畫面？又為何會對這些景物有種熟悉懷念的感覺？ \r\n\r\n在轉瞬間後，又有另一個想法浮現在我的腦海中，我需要一個寶玉。一顆能夠劃破一切真知的寶玉。雖然不知道為何會突然想要這種東西，但我的感覺告訴我這個東西對我來說非常重要，而且我的好奇心也驅使我一定要找到這個寶玉… \r\n為此請各位能夠幫我找出這種寶玉，我願意奉上我身邊的寶物當作報酬。 \r\n\r\n完成條件：混沌水晶*1\r\n任務獎勵：葛雷之劍，葛雷魔法記典*1，葛雷腿甲','','葛雷的冒險日誌-迷藏的黃昏','葛雷',1250,3,99,0,90,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (97,'不知道從什麼時候開始，我的視線中不時會出現一個搖晃不定的身影 \r\n\r\n起初這個現象我認為只是單純的錯覺而不以為意，絲毫不去理會這個怪異現象可能將導致什麼後果... \r\n\r\n直到最近，我才覺得似乎有點不太對勁... \r\n每當我看見這個奇怪的身影時，他會用他手中持有的火炬輕輕地碰觸位於他附近的行人，之後身影便消失不見 \r\n接著慘劇便發生了，先前被他手中的火炬接觸過的人會在接下來的一至十小時內死亡，而且死因都是離奇暴斃... \r\n\r\n雖然我曾經試圖阻止過他去靠近其他人，但是卻徒勞無?.. \r\n只要我一靠近他，他便會開始發出陣陣石頭的摩擦聲，聽起來就像像是在嘲笑我的無力般，接著他就消失不見了... \r\n\r\n我想拯救那些因為他而面臨危險的人，卻無能為力，每當時間一到他們便會突然地消失在我眼前，接著便是在其他地方發現他們的冰冷屍體... \r\n我不想要再有人因為我而死去，即使是間接的... \r\n\r\n據我調查他在試鍊洞窟，從他的行動可以知道他的實力絕對不容小覷，只憑我一個人可能無法應付，希望有人能助我一臂之力！ \r\n\r\n完成條件：擊敗 命運火炬*1\r\n任務獎勵：1000經驗膠囊*1','','搖曳生命之火','雪白少年',18,3,99,0,0,0,NULL,1,2,'253',1,0);
INSERT INTO `wog_mission_main` VALUES (98,'根據上方(國家高層)所提供的情報指出近日我國周邊的三座城邦似乎正積極地拓展各自的軍事武力，為了因應此事件，國王決定派出一位機密調查員前往探查情報，而我便是那位調查員了。 \r\n\r\n原本這項任務只能由我一個人四下秘密執行，然而不久前我又從國家守備處接獲一項更加緊急的任務必須進訴完成，因此向中央提出申請後決定到這裡尋求願意協同調查的人。以下為我目前所掌握的可靠消息： \r\n\r\n1.北之國的機密文件目前不知去向，國內軍隊正全力搜查中 \r\n2.西之國的機密文件目前落在王家地下室中，被嚴密地守護著 \r\n3.南之國並沒有所謂的機密文件，所有的機密全都在國王的掌握之中 \r\n4.東之國的機密文件據說有兩份，一份正存放在國境外的一處洞穴之中，另一份則是悄悄地放在國內某間民宅的書櫃之中，據說目前還沒有人知道第二份文件到底是放在哪裡 \r\n\r\n因為南之國的情報取得難度非常的高，所以這個部分只能由我一個人來執行，至於其他的文件就麻煩各位了。 \r\n\r\n完成條件：秘密文件(白)*1，秘密文件(赤)*1，秘密文件(綠)*1\r\n任務獎勵：間諜短槍，黑影披風，黑影服','','機密文件調查','機密調查組成員',1300,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (99,'最近館內泡茶用的上等珍珠的庫存只剩下不到一個月就要用完了 \r\n而因為北之國境內並不生產珍珠，因此只好將道教南方的地區尋求幫助 \r\n\r\n本國境內生產的威仕爾茶葉非常的有名，要是將此茶葉沖泡成茶之後再加入些釭漪簿]粉末的話，其散發出的迷人香氣絕對能夠讓您感受到天國的存在！ \r\n若有人願意幫我們送珍珠來這裡的話我們將提供一份威仕爾茶葉，以及館長所提供的高檔羊皮紙與一本館藏！ \r\n\r\n委託物品：珍珠*1 \r\n報酬物品：舊羊皮紙*2','','白色下午茶','北之國圖書館長 道格拉斯',1350,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (100,'我想到了！我想到了！原來矮人族的智慧竟是如此的淵博啊！ \r\n如果我的理論正確無誤的話，只要把亞克鐵鎚經過特殊鎔鑄之後再加上特製的液化溶劑 \r\n接著再高溫燒烤的途中立即將溶解的亞克鐵鎚放在祕銀金屬杯中再送入低溫室的話就可以製作出目前尚未有人發現的液體！ \r\n而目前祕銀金屬杯已經找到了，剩下的亞克鐵鎚與液化溶劑只憑我可能沒辦法順利取得 \r\n希望有人能幫我蒐集這兩樣物品，我會將我的新發明的一部分當做酬勞的！ \r\n\r\n完成條件：亞克鐵鎚*1，元素溶劑*1 \r\n任務獎勵：顯影溶液*3','','嶄新的發明','女巫 艾琳',1350,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (101,'可能有人會覺得我很奇怪，為什麼會遠從西之國跑來這裡寫下委託，但其實這是有原因的.... \r\n\r\n兩年前，我只是一位普通的十四歲女孩，每天所做的事情便是幫忙父親照顧羊群，到街上的書房中看看書，或是到附近的市場買點食材回家。 \r\n其中我每天最大的樂趣其實是在晚上接近就寢時刻的時候，到父親的房間中看著坐在書桌前的父親所細心編寫著的冒險故事，據說這些都是父親以前所經歷過的故事，我也深深地沉浸在父親的冒險世界中遊走，直到入睡為止。 \r\n\r\n但是，在某天父親卻突然消失了蹤影，沒有留下半點消息地離開了... \r\n而這時國內的一位將軍卻突然以國王命令為由將父親尚未完成的冒險譚帶走... \r\n\r\n經過我二年的暗地調查後才得知我父親的冒險譚與國家的既密有著密切的關係，而父親則仍舊是音訊全無... \r\n我想奪回父親的冒險譚，雖然父親可能不會再回來了，但我希望至少能留下一點能夠證明父親存在的物品，但是因為這本書目前放在王家地下室中，所以沒辦法透過比較正常的管道來取回這本書... \r\n\r\n根據不久前我在郊外的某處盜賊酒館中有聽到一位喝得爛醉的盜賊所說的情報，王家地下室的守備會在夜晚的時候顯得特別鬆散，要是能夠拿到傳說中能夠將時間轉變為夜晚的夜梟長笛的話絕對能夠輕鬆地在王家地下室中漫步。 \r\n\r\n這是我目前唯一的希望了，希望有人能夠幫我找到那把長笛，我可以從王家地下室中順道帶出一件寶物作為謝禮！ \r\n\r\n委託物品：夜梟長笛\r\n報酬物品：機密文件(赤)*1','','白晝的盜賊','西之國少女',1350,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (102,'在我們的村莊上游處有一條細流綿綿的小河，雖然水量並不多，但是卻足以供應村莊中的需求 \r\n然而，最近河流的水量突然減少，而且每過一天水的流量都會不斷地減少，要是在繼續減少下去的話河流可能終將消失！ \r\n與村中的村民們討論之後覺得可能是居住在村莊上游處的水晶之間內的闇炎爆彈的數量突然增加所造成的影響 \r\n據說最近有村人在水晶之間中發現一處神秘的洞窟，謠傳洞窟內可能藏有寶藏，若有人願意幫助我們擊退闇炎爆彈的話我們願意提供洞窟位置的情報！ \r\n\r\n委託物品：擊敗 闇炎爆彈*10 \r\n報酬物品：秘密文件(綠)*1，黃金之鎧*1','','落蒙村危機','東之國 落蒙村村長',1350,3,99,0,0,0,NULL,4,13,'254',10,0);
INSERT INTO `wog_mission_main` VALUES (103,'我的師父愛德華，數年來到處旅行，不知道去了哪裡\r\n如果你有任何他的消息，請記得告訴我\r\n\r\n完成條件：舊羊皮紙*1，顯影溶液*1\r\n任務獎勵：秘密文件(白)*1','','尋找愛德華(1)','合成大師',1350,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (104,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們能全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n最近邪法師的行動範圍不斷地擴大，且行事作風越來越大膽 \r\n不但會破壞平原周圍的民宅，甚至還集體攻擊在平原上活動的人們！ \r\n根據目擊者的描述，最近邪法師們的個性突然地殘暴起來，只要稍微接近就能感受到他所散發出的邪惡氣息... \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n完成條件：擊敗 邪法師*10\r\n任務獎勵：300 hp回復劑*5','','末日的尾端(1)','全國冒險者工會',3,3,99,0,0,0,NULL,1,1,'50',10,0);
INSERT INTO `wog_mission_main` VALUES (105,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們能全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n原本就殘暴不已的魔蝕精，最近變得更加地凶暴了！ \r\n不但以他們的魔腐液潑灑樹木之外，還會在地面製造暫時性的毒沼澤 \r\n一等到有人不小心陷入沼澤中便會向前撲去！ \r\n目前死在他手中的人不計其數！(其中包含大部分的新人冒險者) \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 魔蝕精*10\r\n任務獎勵：金錢1500','','末日的尾端(2)','全國冒險者工會',3,3,99,0,104,0,NULL,1,1,'14',10,0);
INSERT INTO `wog_mission_main` VALUES (106,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n因為不敵強大敵人的威脅而死在試煉洞窟中的生物屍體最近因為不明原因已大量地轉變成腐屍了！ \r\n他們有默釭犒恓擐瘞岍q契，並且能以本能挑選較軟弱的生物們下手！ \r\n雖然他們並不具有太大的殺傷力，但是他們不時噴出的毒液卻含有致命的劇毒！這種毒素不容易消除，因此還是有潛藏的危險！ \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 腐屍*10\r\n任務獎勵：金錢2500','','末日的尾端(3)','全國冒險者工會',10,3,99,0,105,0,NULL,1,2,'12',10,0);
INSERT INTO `wog_mission_main` VALUES (107,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們能全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n原本就已稱霸試煉洞窟中的強大魔法生物：書怪，最近不知為何數量急劇地增加 \r\n他們在施展魔法時會發出極為恐怖的嘶吼聲，使目標因而膽怯 \r\n然而因為數量增加的影響導致洞窟中經常傳出這種恐怖的聲音，附近的居民們都因為這突然增加的噪音而無法進行正常的作息了... \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 書怪*10\r\n任務獎勵：1500 hp回復劑*2','','末日的尾端(4)','全國冒險者工會',15,3,99,0,106,0,NULL,1,2,'104',10,0);
INSERT INTO `wog_mission_main` VALUES (108,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們能全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n生長在黑暗沼澤的昆蟲怪獸有著喜好掠食蔽囿熔葴D，每隻昆蟲怪獸大約可吃掉將近半頃面積的蔽哄A耕種這類植物的人民們早已不堪其擾 \r\n而近日因不明原因造成的昆蟲怪獸數量暴增更是使得他們幾乎沒辦法採收到一株蔽?\r\n雖然他們曾經試圖驅趕過這群昆蟲怪獸，但換來的卻是一具具血肉糢糊的屍體... \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 昆蟲怪獸*10\r\n任務獎勵：蟲草*1','','末日的尾端(5)','全國冒險者工會',25,3,99,0,107,0,NULL,1,3,'23',10,0);
INSERT INTO `wog_mission_main` VALUES (109,'近日全大陸上出現魔物數量異常增加的現象，可能將會危害到國內人民的安全，請各位冒險者們能全力協助退治！ \r\n以下為近期內觀察到的異象的發生地區： \r\n\r\n灼熱荒漠中最廣為人知的不必多說便是那如奇蹟般的人面獅身，那令他能夠自由行動的秘密至今仍尚未解開 \r\n然而，現在沙漠裡的人面獅身卻在也不是那麼地有趣 \r\n現在的他們會張開他們岩石般的大嘴，將所有的一切吞入他們的體內… \r\n\r\n協助退治者將由全國冒險者工會付出相對等的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 人面獅身*10\r\n任務獎勵：荒漠靴','','末日的尾端(6)','全國冒險者工會',32,3,99,0,108,0,NULL,1,10,'142',10,0);
INSERT INTO `wog_mission_main` VALUES (110,'雖然不斷地到各地進行討伐，但是傷亡事件卻還是有增無減 \r\n因此決定提高委託報酬及內容以尋求更多人是協助退治魔物 \r\n以下是最近所得到的異象發生資料： \r\n\r\n迷霧森林的機器人一號是一種人工的生命體，經由錯綜密集的電子線路組合而成 \r\n平時，他們會看似如同路邊的石頭般地偽裝在從林之中 \r\n除非有人打擾到他們，否則他們是不會主動攻擊的 \r\n但最近森林中的機器人一號們卻不知怎地狂爆了起來，敵我不分地砍殺接近的生物，這種現象若不早點解決將可能會釀成重大災難... \r\n\r\n協助退治者將由全國冒險者工會付出高額的報酬！ \r\n\r\n全國冒險者工會　留 \r\n\r\n完成條件：擊敗 機器人一號*15\r\n任務獎勵：微晶片*1','','末日的尾端(7)','全國冒險者工會',40,3,99,0,109,0,NULL,1,4,'38',15,0);
INSERT INTO `wog_mission_main` VALUES (111,'這是在我們村莊中廣為流傳的故事： \r\n\r\n傳說當在沙漠下雨的夜晚中，身旁有著一隻象徵沙漠的荒漠甲蟲的話，天空之中將會降下一列彩虹色的列車，將此人載往永恆的幸福國度... \r\n\r\n最近有位旅行的占卜師為這個村子占卜未來將會在村子這降下暫時性的小雨時，才令我想起這早已遺忘已久的故事 \r\n\r\n我想要到幸福的國度去，將國度裡的幸福帶回來雨村民們分享 \r\n\r\n因為村子內已因連年乾旱而幾乎無法住人，透過這個方式希望能讓他們對村子重新燃起希望 \r\n\r\n雖然這個傳說或釣瓣ㄔi靠，但目前可能也只有這個方法能夠拯救村子了... \r\n\r\n完成條件：捕捉 荒漠甲蟲','','永恆國度','摩洛斯村 錫得裡克',660,3,99,0,0,0,NULL,2,0,'0',0,146);
INSERT INTO `wog_mission_main` VALUES (112,'我有一位朋友，名叫固希爾，他是一位騎士。 \r\n騎士這個職業必須侍奉一位能夠對之忠一不二的君主，而他也不例外，也因此而讓他自己陷入了迷走的迴廊中… \r\n\r\n有次，他的君主命令他手下的騎士們到一處村莊中燒殺，而原因竟然卻只是為了與其他君主們較量誰旗下的騎士們較為勇猛... \r\n雖然他自己知道這件事情有為於他自己的信念，但因為他必須忠於自己的騎士精神與君主，最後還是只能乖乖地參加討伐村莊的對伍… \r\n\r\n灼熱的火焰圍繞著村莊燃燒，照亮了坐落在世界某處的小村莊。鮮紅的眼睛在烈焰之中中疾速穿梭著，不斷地發出渴望鮮血的眼神望著四周，尋找下一位獻給君主的羔羊。 \r\n然而，在這群兇猛的野獸眼神中，卻仍然殘存有一雙散發出澄淨藍光的眼眸，並不停地流露出憎恨自己的罪惡… \r\n\r\n原來早在固希爾所參與的隊伍到達目標村莊前，其他君主的隊伍早已在村中肆虐多時了… \r\n\r\n這時呈現在他眼前的，已不再是寧靜平和的地方村落，而是飄散著灼熱氣息的人間煉獄… \r\n\r\n『救救我…』 \r\n\r\n突然一個虛弱的聲音從他的耳邊出現。發出聲音的是一位年紀約十五來歲，身體瘦弱，披著破舊土黃色斗篷的少年。 \r\n\r\n這時固希爾腦中所浮現的想法，並不是那些禽獸們的野蠻思想，而思考著該如何以最安全的方法讓他從這裡逃脫 \r\n\r\n於是，他將身上的長白披風包裹住那位少年，並送到村莊外頭隨著討伐隊而來的自己莊園的人民，請他們帶著這位少年從另外一條山路回到莊園中… \r\n\r\n這是上次我們聚會時他所說的，據說那位少年到現在仍然對當時的慘狀餘悸猶存而幾乎不相信莊園中的任何一個人，就算想幫助他也力不從心。 \r\n\r\n據說世界上有種能夠以自己的意志將自己的心思傳達給別人的神奇寶物，有了這個寶物的話應該就可以讓那位少年瞭解他的心意了。 \r\n\r\n雖然他並沒有要求我的幫助，但我可以知道他目前也正在尋找這件寶物，因為這是我當時向他建議的。 \r\n\r\n希望有人能夠幫我們找到這件寶物，讓這位少年能夠瞭解固希爾想法。 \r\n\r\n完成條件：真實水晶*1\r\n任務獎勵：固希爾披風','','哭泣的騎士','詩人 艾亞斯',660,3,99,0,111,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (113,'自從透過真實水晶傳達了固希爾的心思給那位少年之後，他總算能夠完全的信任我們了 \r\n\r\n他說他是從沙漠中的一座村莊搭乘在那邊被稱作幸福的物體來到這裡的 \r\n\r\n這裡是被稱作是幸福國度的地方，只要待在這裡，就能夠找到幸福 \r\n\r\n但卻沒想到來到這裡的第一天就碰上了如此可怕的屠殺…但他還是相信著這個地方是真正的幸福的國度，只要待在這裡，幸福就會無所不在 \r\n\r\n或閉O因為他的村莊的處境十分悲慘吧，不管固希爾如何地對他解釋這裡並不是什麼幸福的國度，只是世界上的一塊大陸 \r\n\r\n他卻依舊對這裡懷著期待，深信著他已經看見拯救村莊的希望了 \r\n\r\n從這時候開始，那位少年便高興的無時無刻跟在固希爾的身邊，希望固希爾能夠跟他說如何能得到幸福 \r\n\r\n但這其實是給了固希爾一個沉重的壓力… \r\n\r\n這或野u有身為他唯一朋友的我才會知道，固希爾平時雖然對他的同袍與莊園同伴們十分地友好，但這其實是有原因的 \r\n\r\n因為固希爾非常清楚他們之間的階層關係，騎士就是騎士，部下就是部下，這種清楚的體認使得他能夠從容地面對他們 \r\n\r\n但是現在卻突然多了一位少年進入了他的生活，一個從未理解過的關係… \r\n\r\n他完全無法明白他們之間究竟是以何種關係來存在的 \r\n\r\n那位少年既不是君主，也不是騎士，更不是他的部下，而朋友也只有我一個(或野L也不知道？)，這是一種新的關係 \r\n\r\n為此他非常的苦惱，也使得他平時的規律變得不平衡… \r\n\r\n君主集會時總是第一個到的他現在變成敬陪末座，君主發言時也時常陷入恍惚 \r\n\r\n其中最大的改變就是當君主發表著下一波的戰爭時，平時必定贊成的他如今開始懷疑君主的指令的正確性，也因此使得君主堆他產生了釵h的不滿 \r\n\r\n雖然他曾經說過成為騎士或閉O錯誤的決定，但這也已經於事無補 \r\n\r\n要解除雙方契約關係的方法有兩個，但這個方法固希爾當然也不會去做，因為這必須要君主或騎士其中一個從世界上消失，或是君主主動提出解約的證明才行 \r\n\r\n出生騎士的他所擁有的騎士精神是絕對不容野L前往殺害君主或是向君主提出解約的要求，因此只能夠由我來了 \r\n\r\n然而身為他的朋友，雖然很想幫助他從這迴廊中走出，但這不是我能解決的問題，領主不是隨隨便便就能應付得了的 \r\n\r\n為此希望有人能夠幫我對付固希爾的領主，取得固希爾的解約證明 \r\n\r\n當然囉，為了防止固希爾發現是我委託的，希望這件事情能夠暗地進行 \r\n\r\n委託物品：固希爾的解約證明*1\r\n完成條件：忠誠之劍','','迷走的迴廊','詩人 艾亞斯',660,3,99,0,112,0,NULL,2,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (114,'前往水晶之間擊敗固希爾的領主，取得解約證明\r\n\r\n完成條件：擊敗固希爾的領主\r\n任務獎勵：固希爾的解約證明*1','','解約證明','詩人 艾亞斯',660,3,99,0,112,0,NULL,2,13,'256',1,0);
INSERT INTO `wog_mission_main` VALUES (115,'人類生命不是永久的，人們的智慧需要靠書籍來延續。 \r\n我們中央城原本藏書屬一屬二的多，全是因為中央城歷史悠久、人才輩出的關係。 \r\n沒想到三年前的一場大火，讓一切都變卦了。 \r\n那場火火燒的猛烈，當我發現時，整個圖書館已經燒去了一大半... \r\n我趕緊叫村民們快來幫忙，救火的救火，搬書的搬書，希望能搶救多一點... \r\n約過了午夜時分，這場令人畏懼的大火終於在眾人的協助下被撲滅了，部分書籍也被村民們救出。 \r\n雖然這場大火奪走了大部分的書籍，但是靠著村民們的協助下，憑著自己的記憶力，也把多數的書的資料重新復原了。 \r\n但是原本不外借的藏書可就沒有這麼幸運了。 \r\n這些書大多都被大火燒個殆盡... \r\n你能幫我到這些書的作者，並且請他們再為我們寫出更好的作品嗎? \r\n拜託了，人類的知識是無價的，找到以後我會好好謝謝你的。 \r\n\r\n完成條件：高級召喚書*1，古書*1，魔女之書\r\n任務獎勵：智慧的精華','','尋找重要書籍','中央圖書館館長',320,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (116,'在我們族裡，流傳著一個這樣的傳說... \r\n在五百年以前，我們遭受到邊境其他民族的攻擊。 \r\n我們因為所在地資源不豐富，武器與人數也落後一大截，於是在不敵對方的情況下，我們節節敗退... \r\n就在沒有退路的情況下，族裡誕生了一個勇士--澳丁。 \r\n澳丁他披著一件白色披風，雙手各拿一把大刀，而他異於常人的地方，是他背後長了一對如昆蟲的翅膀以及一雙如大鵬鳥的翅膀，所以他攻擊時如入無人之地，取敵方首級如同探囊取物... \r\n他的誕生讓我們從地獄的深淵解救出來，在慶幼b的那天晚上，竟然被敵方最後的士兵給暗算了。 \r\n我們族人在憤怒之下，把所有苟延殘喘的敵人都殺的乾淨，從此以後，邊境再也沒有敵人入侵... \r\n不過在幾個月前，有一支民族不斷襲擊我們，而我們因為和平日子過的太久，不敵敵方猛烈的攻勢。 \r\n於是我想拜託你，雖然人死不能復生，但幫我們復活澳丁一天就好，真的一天就好。 \r\n這樣，我們才有機會生存下來。 \r\n\r\n委託物品：召喚 澳丁，封魔太刀，名刀 不知火，高級召喚書*1，詛咒娃娃*1，昆蟲翅膀*1，幻獸羽毛*1，戰狂之魄*1 ，強化鋼鐵*1\r\n任務獎勵：瑪那樹葉*1','','復活葛亞達英雄','葛亞達族勇士',710,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (117,'我真沒想到我家地下室竟然會存放著製作這種東西的捲軸，或閉O巧合吧，還是機緣呢？ \r\n\r\n傳說，地獄之中存在著一位極為利害的拳術師，因為不斷地以他強大的武術殺害人類所以才被送到地獄的 \r\n\r\n在地面上時，他已擁有震撼整個國家的威力，而現在，他擁有了足以撼動所有人類世界的能力… \r\n\r\n他在地獄的期間，利用他帶來的一些道具，搭配著地獄的黑色妖火，創造出了充滿地獄氣息的武器 \r\n\r\n但這把武器並非任何人都能駕馭，若拿著這把武器時心存惡念的話，必定會被武器給支配 \r\n\r\n因此他不打算將這把武器公諸於世 \r\n\r\n但卻又深怕這把武器會從此失傳，於是就將製作方式集結成書後透過矮人族地獄的親信交給了我們 \r\n\r\n如今，我手中的這張捲軸便是那蘊含著遺世神兵的紀錄 \r\n\r\n若有人能夠蒐集到下列這些物品的話，我可以幫你們作出這些早已失傳的武器 \r\n\r\n完成條件：惡魔之爪，火焰輪，魔樹枝*3\r\n任務獎勵：妖火拳套','','地獄的兵器','矮人鐵匠',720,3,99,0,14,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (118,'在人類眼中被視為是無上神兵的武器，是所有戰士們所渴望的目標 \r\n\r\n但人類或釣瓣ㄙ器D一件殘酷的事實，就是這種武器其實只要是二十歲以上的矮人族人幾乎都會作… \r\n\r\n既然這對矮人而言是如此簡單的東西那為什麼矮人們不大量製造這種武器賣給人類呢？ \r\n\r\n理由很簡單，材料不足 \r\n\r\n雖然矮人們擁有製作這種武器的知識與技術，但唯獨卻缺了製作的材料 \r\n\r\n這些被視為珍寶的武器不外乎都會用到一種名為『密銀金屬』的純白礦物 \r\n\r\n但這種礦物卻極為稀有，一座佔地數公畝的礦脈都不見得能找得到一顆純度高於0.01%的祕銀金屬原石呢 \r\n\r\n也因為如此，這類武器即使矮人們幾乎人人皆會做，但仍然還是被矮人們視為自豪的象徵。而我也以製作出密銀武器為目標喔！ \r\n\r\n因此要是有人有密銀金屬礦石的話歡迎送來我這裡，我隨時都能幫你們打造出舉世無雙的祕銀武器！ \r\n\r\n完成條件：密銀金屬礦石*2 ，魔法水*1，強化鋼鐵*4\r\n任務獎勵：退魔雙刃','','曙白銀輝','矮人鐵匠',730,3,99,0,14,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (119,'大部分人類對矮人族的印象就是以打鐵聞名 \r\n\r\n但其實我們也是會做木工的，而且技術也絲毫不遜冶鐵技術呢 \r\n\r\n矮人族的生活與大地、風、樹木以及水流息息相關，因此平時也都會以這些東西為材料來製作物品 \r\n\r\n而能夠完全包含這些元素的物品便是魔法師們所使用的魔杖了，因此矮人族對於魔杖的製作可是非常的講究呢 \r\n\r\n如何？想要親自體驗矮人族精心打造的魔杖的神奇威力嗎？ \r\n\r\n要是有人帶來下列的這些材料的話我可以破例免費幫您製作喔！ \r\n\r\n完成條件：瑪那樹葉*1，魔樹枝*3，竹葉*2，活性布料*1\r\n任務獎勵：樹靈法杖','','大地的恩惠','矮人鐵匠',730,3,99,0,14,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (120,'最近雨林內不知為何時常颳起陣陣狂風，這是原本不應該發生的現象 \r\n\r\n雨林中到處都是之夜茂密的闊葉，以及起伏不定的板根，別說是風了，幾乎連雨都無法穿過濃密的表層落到底部的土表 \r\n\r\n因此這種現象引起了釵h人的注意 \r\n\r\n如今要調查這種怪異現象的話，大概也只能從掌管這整座雨林的叢林之王開始調查了 \r\n\r\n聽說最近叢林之王的行蹤十分隱密，不知道其中是否別有用心還是發生了什麼事？ \r\n\r\n為此希望有人能夠協助暗中調查叢林之王身邊的成員\r\n\r\n完成條件：擊敗 [無淵洞窟]闇輝祭司*5','','叢林之王(1)','雨林守衛 波吉爾',770,3,99,0,110,0,2,4,11,'262',5,0);
INSERT INTO `wog_mission_main` VALUES (121,'將上次您帶回來的可疑染血樹枝做過詳細的調查之後發現樹枝上的綠血中參有疑似與叢林之王的魔力性質極為相似的反應 \r\n\r\n若這綠血真是叢林之王的血液的話那就非同小可了！因為若沒有施展比叢林之王更強大的魔力的話是不可能對叢林之王造成任何損害的 \r\n\r\n為此我們在五天前與居住在雨林深處的暗樹精靈族們展開聯繫 \r\n\r\n希望能夠借助他們族中最情報蒐集能力以及隱密性堪稱數一數二的暗樹調查者來調查叢林之王的行蹤 \r\n\r\n而他們也同意將於三天後將調查結果透過暗樹密使送到我們這邊來 \r\n\r\n然而，在三天後我們卻遲遲沒有收到暗樹密使到來的情報，通常來說這種事應該是不可能發生的，因為他們一族最為注重的就是約定了，凡是他們所立下的誓約無一沒有準時完成的 \r\n\r\n再過了一天之後才得到一位急忙趕來而快喘不過氣的暗樹密使來通報，原先帶著調查文件的暗樹密使在趕路的途中遭到不明生物襲擊，屍體被暗樹族的族人在一處罕為人知的洞穴中發現，而調查文件也因而不知去向 \r\n\r\n這接連而來的奇怪事件使的高層非常的注意，並立即派遣一批為數數十人的菁英部隊前往雨林中尋找文件，但結果卻是他們從此失去了連絡 \r\n\r\n連國內的菁英部隊也無法抵抗這怪異的事件，可知背後必定有著極為強大的力量在操作著，為此徵求有著高超技藝與十足勇氣的冒險者能夠前往尋找暗樹族的調查文件 \r\n\r\n完成條件：擊敗元素殺手，取得 暗樹調查報告','','叢林之王(2)','雨林守衛 波吉爾',770,3,99,0,120,0,2,4,11,'263',1,0);
INSERT INTO `wog_mission_main` VALUES (122,'根據暗樹族的報告顯示，這個魔力的持有者目前並不在這個世界上，而魔力的純度則比叢林之王還要高出釵h，主要施展魔法類型則為元素類型與黑暗類型 \r\n\r\n但這是怎麼回事？施展魔法的人照理說只要還是活人，魔力的來源救必定查得到的 \r\n\r\n難道這代表著這位施術者具有穿越空間的能力？還是說它能夠隱藏自己魔力的氣息呢？ \r\n\r\n要是這樣的話那就真的太糟糕了，這代表對方可能是前所未聞而魔力高深的強者 \r\n\r\n因此當務之急應該是確保叢林之王的真實行蹤與安全，並請求祂能夠協助找出這件事件的籌組人 \r\n\r\n根據暗數族調查報告中所顯示的資料可以知道叢林之王現在可能正在無淵洞窟中療傷 \r\n\r\n然而最近各地發生太多事了，我們早已人手不足，希望您能夠幫助我們找到叢林之王，並帶回祂所希望傳達的訊息 \r\n\r\n祂可能會將祂的情報派遣給洞窟中的祂的僕從，命令他們將情報帶到值得信賴的人手中，你可以嘗試與他們接觸看看\r\n\r\n完成條件：挑戰叢林之王守衛','','叢林之王(3)','雨林守衛 波吉爾',770,3,99,0,121,0,2,4,11,'264',1,0);
INSERT INTO `wog_mission_main` VALUES (123,'最近聽村子裡的人說有人在村子的正北方的賀密湖的沿岸發現一座巨大的巖窟 \r\n\r\n洞窟中到處都爬滿了碩大的劇毒蜘蛛，以及一對散發著劇烈壓力的恐怖眼珠… \r\n\r\n然而，這或野u有村中的幾位長者跟守衛們才知道 \r\n\r\n那座洞窟其實是守護著落月村以及王者之路的聖地 \r\n\r\n在洞窟內無數滿地的蜘蛛之中，只有一位擁有著與眾不同的體型，以及氣勢 \r\n\r\n牠，不，應該是『祂』，就是這裡的守護神的化身，一隻極為恐怖的巨大狼蛛 \r\n\r\n平時，為了不讓人類打擾到祂的作息，祂會在洞窟的入口處施下極為強大的幻覺結界以使人類無法看見這座洞窟 \r\n\r\n就算是世界最高強的法師也不見得能夠從這幻覺中脫困呢 \r\n\r\n但是，現在竟然有平常人能夠清楚地看見那座被強大結界封印的洞窟？ \r\n\r\n我很肯定這之中絕對發生了什麼問題，然而卻礙於守衛的身份而無法自由行動 \r\n\r\n希望有人能夠協助前往幫忙調查結界弱化的原因 \r\n\r\n完成條件：擊敗 魔導石翼獸*5','','勇氣的蜘蛛穴(1)','落月村守衛 吉哈',800,3,99,0,110,0,0,4,7,'257',5,0);
INSERT INTO `wog_mission_main` VALUES (124,'魔導石翼獸？ \r\n\r\n嗯…，我也好久沒有聽到這個名字了… \r\n\r\n魔導石翼獸其實並不是這個世界的生物，他們是經由一群魔力強大的巫師們透過禁忌的魔法陣召喚而來的 \r\n\r\n過去也曾經發生過魔導石翼獸被召喚到這裡的事件，後果真的是慘不忍睹… \r\n\r\n他們的生性殘暴，會將眼前所看到的一切都盡可能地破壞 \r\n\r\n且身上帶有強大的禁錮咒力，可以將他們的身體強化得比鋼鐵還要堅硬，相信您應該也已親身體驗過了才是 \r\n\r\n但也因為這個禁錮咒力的緣故使得他們沒辦法使出他們所有的力量 \r\n\r\n根據古代魔法書上的記載，解咒後的魔導石翼獸可以發揮比禁錮中的魔導石翼獸還要高數倍的破壞力 \r\n\r\n要是一次有多隻魔導石翼獸的禁錮咒力被解放的話可能將會產生無可想像的後果 \r\n\r\n但是，通常來說魔導石翼獸應該是不聽從於任何人的，除非能夠以壓倒性的氣勢使之震懾，否則他會將所有想要控制他的人全部撕裂 \r\n\r\n但這次會突然在這種地方出現為數眾多的魔導石翼獸，可知這絕非偶然，背後必定有人在暗中操作 \r\n\r\n而根據古代魔法書的記載，想要遠距離且一次操縱多隻魔導石翼獸的方法其實不是沒有，但必須要借助一種特殊的魔力保存道具來將自己的魔力注入其中，然後再放在魔導石翼獸的任一部位，不過前提是要能夠操縱他們… \r\n\r\n希望您能夠再次前往擊退這些解咒後石翼獸，並將他們身上的魔力保存道具帶回來給我們，我們想要透過這個東西來查出在幕後操控的黑手 \r\n\r\n完成條件：取得 祕術水晶*2','','勇氣的蜘蛛穴(2)','落月村守衛 吉哈',800,3,99,0,123,0,0,4,7,'258',2,0);
INSERT INTO `wog_mission_main` VALUES (125,'調查這些魔力保存道具中的魔力之後雖然還是無法知道這些魔力的持有者是誰，但至少可以知道一件事，我們的狼蛛，也就是我們的守護神，可能正面臨著生死存亡的關鍵 \r\n\r\n因為這個魔力的強度實在是過於強大，要隨便對我們的守護神施下任何一種詛咒是輕而易舉的… \r\n\r\n因此目前的第一要事是確保守護神的安全，並直接與祂聯繫，以瞭解襲擊者的確實情報 \r\n\r\n雖然我們很想要及時派人前往蜘蛛穴中與守護神聯絡，但最近各地接連發生怪異的事件而人手嚴重短缺 \r\n\r\n希望您能夠代表我們與蜘蛛穴中的守護神接觸，並帶回祂所交付於你的情報 \r\n\r\n完成條件：取得 記憶碎片*1','','勇氣的蜘蛛穴(3)','落月村守衛 吉哈',800,3,99,0,124,0,0,4,7,'259',1,0);
INSERT INTO `wog_mission_main` VALUES (126,'我的大哥 奧格納 是一位地理學家，年輕時跟二位好友進入神秘的幻獸森林進行地質及生態觀察\r\n探勘偌大的幻獸森林是很困難的事情，很不幸的他們迷失在幻獸森林之中\r\n\r\n意外的他們發現到精靈族村落，並且嘗試與精靈族友好\r\n長期的相處下來，精靈族原本從排斥進展到接納人族的他們\r\n並且奧格納與精靈族女性 曼斐拉 相戀\r\n\r\n由於精靈族與人族壽命不同，奧格納為了能長期陪伴曼斐拉，於是奧格納偷偷潛入精靈族代代所守護的精靈之泉\r\n只要人族喝下精靈之泉的泉水，可以跟精靈族一樣長生不老，但這是精靈族的禁忌\r\n\r\n沒多久這件事被精靈族長老發現，奧格納他們被趕出了幻獸森林並被限制再也無法進入精靈族村落\r\n奧格納雖然獲得長生不老，但也失去記憶，奧格納為了找回他的記憶10多年來下落不明\r\n我大膽猜測奧格納應該是前往精靈族村落\r\n\r\n冒險者們，我希望你能進入精靈族村落，尋找曼斐拉打聽奧格納的下落\r\n當年奧格納他們三人，把精靈村地點繪成一張地圖，但是這張地圖被分成三塊，每人持有一塊\r\n目前我手上只有奧格納地圖，必須先收集其他三塊地圖\r\n\r\n完成條件：迪克地圖*1，科本林地圖*1\r\n任務獎勵：長生之水*3','我們循著地圖順利來到精靈族村落，但是長老告知我們奧格納帶著曼斐拉，以及他們的兒子離開多年，最少得知他們相當的幸福\r\n','異族之戀','辛祖爾',460,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (127,'數日之前，我所保管的地圖被灰狼盜賊集團所盜走\r\n\r\n據我所知，此盜賊集團所盜來的寶物藏匿在王者之路，由魔物地獄門犬所守護\r\n\r\n完成條件：擊敗地獄門犬*5\r\n任務獎勵：迪克地圖*1','','迪克地圖','迪克',460,3,99,0,0,0,NULL,3,7,'260',5,0);
INSERT INTO `wog_mission_main` VALUES (128,'你是來尋找奧格納的嗎？他確實有來過我這裡，但是多年前已經前往精靈族村落了，並且也帶走了地圖\r\n\r\n我能夠幫你重新繪製地圖，但是繪製地圖需要一些特別的材料\r\n\r\n完成條件：魔法水*2，白色布料*3，魔法染料*1\r\n任務獎勵：科本林地圖*1','','科本林地圖','科本林',460,3,99,0,0,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (129,'這幾年來，我們村落的精靈之泉的泉水慢慢牯?\n\r\n希望偉大的冒險者們，能替我們查出牯靰滬鴞]\r\n\r\n但是在精靈之泉的源頭，有巨大的落石擋住道路，你必須先尋找解決落石的方法\r\n\r\n完成條件：內裂火藥*1，新式炸藥*1','','乾竭的精靈泉','精靈族長老',460,3,99,0,126,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (130,'我們的調查員發現長久以來，在精靈泉源頭的清水精靈珠被人盜走\r\n\r\n傳聞有一個新興宗教團體，叫做聖水會，只要喝下教中的聖水，可以治百病且長生\r\n\r\n希望您能調查一下此團體是否與清水精靈珠的失蹤有關係\r\n\r\n完成條件：擊敗 聖水會教主\r\n任務獎勵：黯淡的清水精靈珠','','被盜走的清水精靈珠','精靈族長老',460,3,99,0,129,0,NULL,3,13,'261',1,0);
INSERT INTO `wog_mission_main` VALUES (131,'原來精靈珠是被聖水會的教主偷走\r\n但是由於精靈珠長久以來失去精靈族的祝福，失去原有的力量\r\n\r\n若能收集到具有強大魔力的材料來施法，加上精靈族的靈力\r\n或陳鄖牬踰F珠恢復原來的力量\r\n\r\n完成條件：幻獸羽毛*3，聖潔之花*2，水晶碎片*3\r\n任務獎勵：清水精靈珠','','失去光芒的精靈珠','精靈族長老',460,3,99,0,130,0,NULL,3,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (132,'我長期研究精靈所留下來千年之前的壁畫，從壁畫中得知，在遠古時期，精靈族與幻獸跟龍族有一場戰爭，但是龍族的力量過於強大，造成幻獸與精靈死傷慘重\r\n\r\n戰爭末期，精靈王為了對抗龍族用運族人最後的力量製造六大精靈珠，企圖利用六大精靈珠的力量來扭轉戰局，不過這一切都已經太遲了\r\n\r\n正當精靈珠完成的時候，龍族大軍已經攻入最後的根據地，精靈王也因此戰死，殘存的幻獸以及精靈族人，躲入現今的幻獸森林\r\n\r\n龍族軍大勝後的幾天，受到奇怪疫病的流行造成龍族大量死亡，傳聞可能是精靈王死前用了最後的力量在猛毒精靈珠上\r\n\r\n使得殘存的幻獸以及精靈族人沒有受到龍族後續的追殺\r\n\r\n希望你能幫我拿到戰役石板，把這些紀錄寫在石板上\r\n\r\n完成條件：戰役石板*3\r\n任務獎勵：3000經驗膠囊*6','','古時戰役','考古學家 查爾斯',530,3,99,0,0,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (133,'今天有重大發現，從壁畫中得知，在當時的戰役中六大精靈珠的烈火精靈珠在熔炎巨龍手中\r\n\r\n熔炎巨龍喜歡棲息在高溫的火山之中，在灼熱荒漠有一座終年不斷噴出火焰的火山\r\n\r\n這是一條非常危險且困難的道路，想要順利前往必須先找到矮人 倫魯的協助，以及拿到召喚 希瓦\r\n\r\n若你夠好運的話，或野i以在灼熱荒漠找到倫魯\r\n\r\n完成條件：找到矮人 倫魯，召喚 希瓦','','烈火精靈珠','考古學家 查爾斯',530,3,99,0,132,0,NULL,1,10,'265',1,0);
INSERT INTO `wog_mission_main` VALUES (134,'熔炎巨龍是古時期力量強大的巨龍之一，要打敗牠是相當不容易的事情\r\n\r\n祝你好運\r\n\r\n完成條件：擊敗熔炎巨龍\r\n任務獎勵：烈火精靈珠','','熔炎巨龍','考古學家 查爾斯',530,3,99,0,133,0,NULL,1,10,'266',1,0);
INSERT INTO `wog_mission_main` VALUES (135,'我的助手瑪琳，為了尋找珍貴藥材\r\n在黑暗沼澤失蹤了一個多月，曾有人看到她進入最危險的荊棘森林\r\n荊棘森林除了毒蟲之外，最恐怖的是惡魔荊棘，落入惡魔荊棘將無法脫身\r\n只有毒蠍石才能避開惡魔荊棘的攻擊\r\n\r\n完成條件：毒蠍石*1，找到瑪琳\r\n任務獎勵：斬荊利刃','','尋找瑪琳','怪醫 白傑克',62,3,99,0,0,0,NULL,1,3,'268',1,0);
INSERT INTO `wog_mission_main` VALUES (136,'謝謝您救了我，在荊棘森林一個多月中，意外發現到這顆寶珠\r\n據我多日來的研究，猜測這顆可能是巨木精靈珠\r\n但這顆寶珠已經喪失原本的能力，要使其恢復能力，必須把寶珠放入世界樹中心\r\n但是世界樹在數百年前，被惡魔之王 薩佈雷用炙熱戰斧砍斷\r\n要讓世界樹重生，需收集世界之水及世界樹種子\r\n\r\n世界之水在最果之島\r\n世界樹種子在久遠戰場\r\n\r\n完成條件：世界之水*1，世界樹種子*1\r\n任務獎勵：智慧軟鞋','','世界樹(1)','助手瑪琳',155,3,99,0,135,0,NULL,1,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (137,'世界樹重生會影響到薩佈雷的魔力，薩佈雷一定會用盡任何方法來阻止世界樹重生\r\n希望你能保護我前往王者之路，並擊敗薩佈雷手下\r\n\r\n完成條件：殺死薩佈雷手下*8','','世界樹(2)','助手瑪琳',210,3,99,0,136,0,NULL,1,7,'271',8,0);
INSERT INTO `wog_mission_main` VALUES (138,'薩佈雷在惡魔界有著至高的地位，控制著世界上70%的惡魔\r\n在世界樹將完全重生之前，薩佈雷一定會前來破壞\r\n希望你能前往王者之路擊敗薩佈雷\r\n\r\n完成條件：殺死薩佈雷\r\n任務獎勵：巨木精靈珠*1，薩佈雷5格背包*1\r\n','總算讓巨木靈珠獲得原本的力量，巨木精靈珠擁有淨化，但使用一次淨化，必須等上一年才能使用第二次\r\n在我旅行的路上，看到有兩個地方需要巨木精靈珠的協助\r\n1.漁人碼頭的上游\r\n2.克沙鎮','惡魔之王 薩佈雷','助手瑪琳',213,3,99,0,137,0,NULL,1,7,'272',1,0);
INSERT INTO `wog_mission_main` VALUES (139,'前往迷霧森林尋找惡水淨化點\r\n\r\n完成條件：尋找惡水淨化點*6，巨木精靈珠*1\r\n任務獎勵：魚人釣竿，巨木精靈珠*1','','淨化漁人碼頭上游','助手瑪琳',213,3,99,0,138,140,NULL,1,4,'273',6,0);
INSERT INTO `wog_mission_main` VALUES (140,'前往灼熱荒漠尋找克沙淨化點\r\n\r\n完成條件：尋找克沙淨化點*6，巨木精靈珠*1\r\n任務獎勵：清靜弓，巨木精靈珠*1','','淨化克沙鎮','助手瑪琳',213,3,99,0,138,139,NULL,1,10,'274',6,0);
INSERT INTO `wog_mission_main` VALUES (141,'在古代遺跡的壁畫中，我們推測在世界的某處有著更大更神秘的遺跡存在\r\n為了尋找偉大的遺跡中需要更多有經驗的探險者來組成遠征隊\r\n\r\n前往古代遺跡尋找探險者\r\n\r\n完成條件：遺跡調查員證書*1，尋找探險者*8\r\n任務獎勵：1000經驗膠囊*3','','挖掘隊的遠征','地精 比比克',160,3,99,0,0,0,NULL,4,5,'275',8,0);
INSERT INTO `wog_mission_main` VALUES (142,'在一次夜晚的駐紮，我們營地遇到襲擊，所幸無人傷亡，但是大部分的補給品被黑蒙夜盜竊走\r\n黑蒙夜盜成員經常出現在久遠戰場，希望您能替我們找回這些補給品\r\n\r\n完成條件：挖掘隊補給品*5\r\n任務獎勵：金錢50000','','失竊的補給品','地精 比比克',172,3,99,0,141,0,NULL,4,6,'276',5,0);
INSERT INTO `wog_mission_main` VALUES (143,'根據壁畫的記載，埋藏著寶藏的遺跡應該在這附近\r\n但入口似乎被某總機關巧妙的隱藏起來，我們尋找了數日不得而入\r\n若你能協助我們解開機關，我會給你優厚的報酬\r\n\r\n完成條件：玻璃杯*1，綠色液體*5，魔樹枝*3\r\n任務獎勵：挖掘手套','','大地的裂痕','地精 比比克',178,3,99,0,142,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (144,'隨著探查遺跡的進度不斷推進，夜晚不時的從地底下傳來一陣陣地鳴聲\r\n挖掘隊中慢慢開始有人染上不明疾病，倒下的人數漸漸增加，開始有了遺跡詛咒的流言傳出\r\n\r\n請你到中央平原尋找怪醫 白傑克，以及尋找可以治療疾病的藥材\r\n\r\n完成條件：聖潔之花*1，解毒草*5，尋找怪醫 白傑克\r\n任務獎勵：地脈面罩','','地底來的詛咒','地精 比比克',425,3,99,0,143,0,NULL,4,1,'277',1,0);
INSERT INTO `wog_mission_main` VALUES (145,'我們終於挖掘到地鳴聲的源頭，在地底下的神殿遺跡中有一隻地龍，地龍在神殿裡守護了數百年之久\r\n挖掘隊已經有不少成員死在地龍的利爪之下，若不想辦法打倒地龍，遺跡隊無法繼續前進\r\n\r\n完成條件：擊敗神殿地龍(王者之路)\r\n任務獎勵：地龍權杖，地龍爪','','地龍反撲','地精 比比克',475,3,99,0,144,0,NULL,4,7,'278',1,0);
INSERT INTO `wog_mission_main` VALUES (146,'經過漫長的挖掘之路，總算到達地心的最深處，在內部有一處祭壇，祭壇上面有著傳說中的大地精靈珠\r\n只要打敗祭壇前的大地守護者，取得大地精靈珠回王城，我們挖掘隊的任務就可以結束\r\n我會給你優厚的報酬，請繼續協助我們挖掘隊\r\n\r\n完成條件：擊敗大地守護者(王者之路)\r\n任務獎勵：?','我是挖掘隊副隊長 阿炮，在回王城的路上隊長不幸遭到比比克的謀害，大地精靈珠也被比比克所奪走\r\n\r\n後來我們調查，比比克是地精的望族之後，為了鞏固自己的權利地位，安排了這趟挖掘隊的冒險，並搶奪精靈珠\r\n\r\n由於大地神殿周圍的大地靈氣因為失去精靈珠的制御而開始爆走，現在要把精靈珠放回去已經不可行了\r\n必須召換大精靈才能使這地方恢復原貌','深入地心','地精 比比克',495,3,99,0,145,0,NULL,4,7,'279',1,0);
INSERT INTO `wog_mission_main` VALUES (147,'打敗比比克，奪回大地精靈珠\r\n\r\n完成條件：擊敗比比克(王者之路)\r\n任務獎勵：大地精靈珠*1，大地披風*1','','大地精靈珠','挖掘隊副隊長 阿炮',495,3,99,0,146,0,NULL,4,7,'280',1,0);
INSERT INTO `wog_mission_main` VALUES (148,'我們盜賊公會開始舉辦一年一度的賊之試鍊，只要拿到指定物品回到這裡\r\n就可以通過我們的試鍊，正式成為我們的一員\r\n\r\n完成條件：內裂火藥的構想*1，布鞋*1\r\n任務獎勵：3000經驗膠囊*8','','盜賊試鍊','會長 刃音',405,3,99,0,13,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (149,'恭喜你成為我們盜賊公會的一員，在這次的試鍊中，出現了一位百年難得一見的女天才，在一天之內完成要求，讓我想起了以前傳說中的賊之王」神行亞拉岡」\r\n\r\n現在有一個緊急任務，魔物日漸強大使我們受到不小的威脅，需要有人去探查附近的魔物據點\r\n紅翼已經出發了，請盡快去協助紅翼吧\r\n\r\n完成條件：魔物據點*8(水晶之間)\r\n任務獎勵：金錢100000','','新人王 紅翼','會長 刃音',420,3,99,0,148,0,NULL,4,13,'281',8,0);
INSERT INTO `wog_mission_main` VALUES (150,'日前我們對魔物展開大規模的進攻，結果如你所見，我們盜賊軍團遭遇空前的挫敗，死傷慘重\r\n\r\n魔物軍團的首領 魔將軍怒鐵，有著鋼鐵般的防禦，使我們屢攻不下，紅翼的配刀也在戰役中被怒鐵所斷\r\n希望你能尋找矮人鐵匠，來修復紅翼配刀\r\n\r\n完成條件：尋找矮人鐵匠(中央平原)','','戰敗','會長 刃音',580,3,99,0,149,0,NULL,4,1,'282',1,0);
INSERT INTO `wog_mission_main` VALUES (151,'這是一把相當罕見的神兵，使用稀有的材料鑄造而成，要修復相當困難\r\n你必須收集星隕石，星隕石是由天上所墬落的隕鐵所形成，打敗隕鐵石人可以獲得\r\n並使用妖精之水及幻獸 不死鳥的魔力使配刀再生\r\n\r\n完成條件：星隕石*3，妖精之水*2，捕捉幻獸 不死鳥\r\n任務獎勵：星隕髮帶','','紅翼配刀','矮人鐵匠',580,3,99,0,150,0,NULL,4,0,'0',0,120);
INSERT INTO `wog_mission_main` VALUES (152,'當我在修復配刀時，發現到從裂縫之中有股風的能量，從刀的內部散發出來\r\n我向紅翼詢問後得知，這把刀在小時候」神行亞拉岡」所贈送，是亞拉岡剛從中央平原的西風山谷冒險回來所得到的寶物\r\n\r\n西風山谷可能藏著讓配刀更強大的秘密\r\n\r\n完成條件：打敗西風山谷的風神獸\r\n任務獎勵：靈風裝束','我們在風神獸身上意外發現到炫風精靈珠，有炫風精靈珠可以進化紅翼配刀','配刀的秘密','矮人鐵匠',620,3,99,0,151,0,NULL,4,1,'283',1,0);
INSERT INTO `wog_mission_main` VALUES (153,'經過旋風靈珠的融合之後，這把配刀現在的能力超越以往\r\n但要打敗魔物軍團不是這麼容易，我們採取各各破的方式\r\n首先，先打敗魔物據點中的小隊長\r\n\r\n完成條件：魔物軍團 小隊長*8(水晶之間)\r\n任務獎勵：魔化硬盾','','一陣風','會長 刃音',650,3,99,0,152,0,NULL,4,13,'284',8,0);
INSERT INTO `wog_mission_main` VALUES (154,'現在只剩下怒鐵，離勝利剩最後一步，也是要打敗魔物軍團最困難的關卡\r\n怒鐵號稱有著最強的防禦，要打敗他必須要靠紅翼以絕快的速度，在他的防禦中製造破洞\r\n最後由你補上致命一擊\r\n\r\n完成條件：打敗怒鐵(水晶之間)\r\n任務獎勵：旋風精靈珠*1，怒鐵之槌','總算打敗了怒鐵，我們盜賊公會可以獲得短暫的和平\r\n旋風精靈珠請你交還給精靈族吧','魔將軍 怒鐵','會長 刃音',700,3,99,0,153,0,NULL,4,13,'285',1,0);
INSERT INTO `wog_mission_main` VALUES (155,'最近我嚐試做一個味道別與往常的蛋撻，但是怎麼做總是感覺缺少什麼\r\n我想請你幫我收集一些特別的食材，或陶o些食材能給予蛋撻新的風味\r\n\r\n完成條件：萊姆香料*2，青綠果實*1，火焰龍蛋*1\r\n任務獎勵：半成品蛋撻*1\r\n','謝謝你幫我收集來的食材，雖然做出了口感特Q、顏色鮮美的蛋糕\r\n但是一直調配不出能夠與這蛋糕匹配的香郁的味道\r\n我的好朋友 星巴克，是這世界上最有名的咖啡專家，或野L知道如何調配出特別的香味','蛋撻','蛋糕達人 亞尼克',860,3,99,0,0,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (156,'正好我在研究雨林咖啡豆，這是我在熱帶雨林地帶所培養出的咖啡豆\r\n這種咖啡豆所煮出來的味道，除了特別香郁甘甜濃滑之外，還能縈繞人們口中久久無法忘記\r\n若能研究成央A也可以幫忙亞尼克完成夢幻中的蛋撻\r\n\r\n完成條件：幻氣焦糖*3，樹精華*1\r\n任務獎勵：雨林咖啡豆*1\r\n','','雨林咖啡豆','咖啡達人 星巴克',860,3,99,0,155,0,NULL,4,0,'0',0,0);
INSERT INTO `wog_mission_main` VALUES (157,'白輪蛋撻就是我替這夢幻蛋撻所取的名字\r\n只要有雨林咖啡豆，我相信就能做出世上最好吃的蛋撻\r\n\r\n完成條件：雨林咖啡豆*1，半成品蛋撻*1\r\n任務獎勵：白輪蛋撻','','白輪蛋撻','蛋糕達人 亞尼克',860,3,99,0,156,0,NULL,4,0,'0',0,0);

#
# Table structure for table wog_monster
#

DROP TABLE IF EXISTS `wog_monster`;
CREATE TABLE `wog_monster` (
  `m_id` int(11) unsigned NOT NULL auto_increment,
  `m_at` int(11) unsigned NOT NULL default '0',
  `m_df` int(11) unsigned NOT NULL default '0',
  `m_mat` int(11) unsigned NOT NULL default '0',
  `m_mdf` int(11) unsigned NOT NULL default '0',
  `m_agl` int(11) unsigned NOT NULL default '0',
  `m_name` varchar(48) NOT NULL default 'N/A',
  `m_s` tinyint(1) unsigned NOT NULL default '1',
  `m_sat_name` varchar(160) default NULL,
  `m_hp` int(11) unsigned NOT NULL default '0',
  `m_lv` int(10) unsigned NOT NULL default '0',
  `m_luck` tinyint(4) unsigned NOT NULL default '1',
  `d_id` int(10) NOT NULL default '0',
  `m_topr` smallint(4) unsigned NOT NULL default '0',
  `m_place` tinyint(3) unsigned NOT NULL default '0',
  `m_img` varchar(25) default NULL,
  `m_meet` tinyint(3) unsigned NOT NULL default '0',
  `m_mission` tinyint(3) unsigned NOT NULL default '0',
  `m_npc` tinyint(3) unsigned NOT NULL default '0',
  `m_npc_message` text,
  PRIMARY KEY  (`m_id`),
  UNIQUE KEY `m_name` (`m_name`),
  KEY `m_place` (`m_place`),
  KEY `m_meet` (`m_meet`),
  KEY `m_mission` (`m_mission`)
) TYPE=MyISAM;

#
# Dumping data for table wog_monster
#

INSERT INTO `wog_monster` VALUES (1,19,8,15,5,2,'史萊姆',1,'猛烈一擊',35,2,1,204,81,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (2,12,3,21,6,3,'水母',2,'用發電的觸角電極',38,2,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (3,13,3,22,8,3,'香菇怪',4,'噴出有毒氣體',35,1,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (4,22,8,20,8,6,'蟹',2,'猛蟹突擊',42,3,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (5,25,10,15,1,3,'貝殼怪',2,'連續攻擊',53,4,1,466,585,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (6,20,5,25,12,6,'水妖',2,'魔力提升',60,4,1,465,585,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (7,45,32,62,48,25,'魔女',6,'精神集中',285,12,1,464,585,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (8,88,60,30,22,15,'石人',1,'巨石滅頂',430,16,1,0,0,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (9,33,16,25,12,18,'飛兔',4,'攻擊力上升',78,6,1,463,585,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (10,293,180,258,190,130,'腐蝕龍',1,'龍之吐息',1830,32,1,475,621,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (11,28,10,35,18,15,'毒蟾蜍',6,'噴灑劇毒',92,8,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (12,50,35,35,30,23,'腐屍',6,'噴灑劇毒',175,10,1,0,0,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (13,450,280,415,310,250,'白蛇龍',2,'白龍巨浪',3860,43,1,205,340,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (14,42,30,55,43,20,'魔蝕精',6,'魔蝕對方防具',85,8,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (15,120,93,105,84,85,'狂暴獅',3,'狂暴猛擊',640,23,1,478,625,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (16,130,90,90,92,68,'劍棘獸',4,'攻擊力上升',430,19,1,468,603,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (17,105,78,130,92,66,'電化猛獸',1,'發出百萬電壓',450,18,1,0,0,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (18,85,62,60,40,42,'恐怖妖獸',5,'製造恐怖幻覺',400,16,1,467,603,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (19,63,40,77,45,28,'魔化妖',5,'精神集中',265,13,1,469,603,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (20,70,50,88,62,32,'獸喚師',4,'召換猛獸',425,17,1,471,621,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (21,56,35,40,23,20,'靈牛',1,'攻擊力上升',230,11,1,404,405,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (22,207,185,192,174,107,'巨釜戰士',4,'猛烈的必殺一擊',950,27,1,470,594,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (23,190,95,175,120,121,'昆蟲怪獸',5,'呼喚數百隻昆蟲攻擊',580,23,1,391,607,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (24,126,95,111,71,89,'毒蜘蛛',6,'噴灑劇毒',610,24,1,331,648,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (25,225,110,210,153,85,'靈術師',3,'喚出四周幟熱火炎',660,25,1,207,648,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (26,136,85,121,84,73,'變形狂獸',1,'變形成數隻狂獸',523,22,1,0,0,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (27,207,110,192,130,80,'黑暗魔蝕精',6,'魔法  劇毒酸液',540,23,1,373,729,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (28,150,120,135,98,96,'金屬食人怪',1,'成群食人怪一起攻擊',900,29,1,0,0,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (29,354,287,319,250,192,'暴火龍',3,'口中噴出高熱火焰',1990,38,1,127,260,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (30,217,138,202,110,76,'瘋狂爆炎',3,'爆炸術',510,24,1,358,729,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (31,211,95,196,120,67,'蛇身魔女',4,'魔法 石化術',498,23,1,206,340,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (32,527,357,452,366,267,'天使',5,'周圍出現神聖光芒  天使給',6140,53,1,315,810,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (33,286,205,251,170,138,'地獄火球',3,'爆炸術',1397,31,1,472,621,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (34,375,203,340,239,152,'花瓣妖精',4,'魔法 媚惑術',1420,34,1,208,105,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (35,361,254,326,210,174,'變態花精',4,'召喚周圍所有巨籐綑綁對手',1846,38,1,371,1053,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (36,291,251,256,187,102,'骷頭戰車',2,'戰車衝擊',1772,37,1,473,621,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (37,357,232,322,241,132,'沙怪',1,'口中噴出爆風狂沙',1792,38,1,474,621,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (38,300,200,265,200,125,'機器人一號',1,'身上發出無數子母彈',1390,32,1,357,1296,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (39,340,200,305,200,125,'機器人二號',5,'身上發出無數能量光線',1400,32,1,60,279,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (40,390,268,355,275,189,'食人鷲',5,'翅膀捲起巨大暴風',2921,43,1,0,0,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (41,402,287,367,225,180,'狂鷹',5,'全身燃起熊熊烈火往對手衝',3572,46,1,0,0,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (42,392,315,357,280,135,'巨大沙蟲',1,'將對手吞噬無底流沙',4892,48,1,0,0,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (43,462,300,427,301,201,'泥手',4,'巨大化',4934,44,1,10,311,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (44,440,289,405,270,205,'黑衣侍衛',2,'血腥斬',4380,47,1,19,300,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (45,440,320,405,287,217,'暴走機械',2,'猛烈的必殺一擊',4040,49,1,323,891,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (46,480,410,475,350,243,'能量機',3,'光學  能量爆裂',5855,51,1,0,0,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (47,26,10,2,1,5,'暴走黑熊',4,'發狂式攻擊',38,5,1,399,324,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (48,10,5,21,9,7,'鬼魂',1,'死靈魔法',21,6,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (49,12,7,4,3,6,'毒蜂',6,'呼朋引伴群蜂展開攻擊',20,1,1,374,648,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (50,6,6,18,6,5,'邪法師',4,'死靈魔法',28,3,1,0,0,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (51,18,10,6,5,6,'毒蠍',6,'噴出毒液',30,2,1,403,486,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (52,635,430,385,350,210,'龍蛇',2,'龍炎',7350,58,1,216,498,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (53,375,300,325,280,180,'強力史萊姆',1,'分裂',3350,40,1,560,370,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (54,685,450,665,450,300,'史萊姆王',1,'分裂',8650,65,1,152,321,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (55,425,380,495,400,180,'金屬史萊姆',3,'分裂',4650,48,1,217,415,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (56,355,310,295,190,120,'冰毛象',5,'攻擊力上升',2750,38,1,406,980,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (57,285,210,165,150,120,'玄武獸',1,'口中噴出爆風狂沙',2250,34,1,18,344,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (58,235,150,165,100,90,'地獄惡犬',4,'咆哮',1950,31,1,476,630,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (59,165,120,225,160,96,'青魔導士',5,'鏡射對手的攻擊',2100,32,1,402,648,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (60,110,100,180,120,75,'南瓜怪',4,'猛毒術',1200,25,1,372,648,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (61,90,86,175,110,60,'魔鏡',5,'幻象',850,23,1,400,340,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (62,146,94,94,94,67,'魔鼠',4,'利齒猛咬對手',750,23,1,477,630,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (63,52,38,41,38,25,'蜥蜴',1,'用巨爪撕裂對手',320,12,1,0,0,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (64,30,41,58,50,25,'蝙蝠',5,'超音波',320,13,1,0,0,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (65,310,280,402,310,150,'闇爆炎彈',3,'全身發射出無數爆彈',3300,42,1,0,0,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (66,362,260,382,260,168,'火狼',3,'全身燃起熊熊烈火往對手衝',3160,41,1,330,891,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (67,422,300,463,320,200,'黑暗獵人',5,'失傳的黑暗魔術 無淵地獄',4200,45,1,215,429,5,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (68,489,380,563,410,235,'蝙蝠魔人',5,'強力音波',6300,53,1,125,354,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (69,513,362,563,430,235,'樹精',4,'把對手吸入體內',6350,53,1,307,729,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (70,615,422,520,420,253,'死神騎士',5,'血腥槍',7800,57,1,0,0,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (71,560,430,620,450,215,'雷電獸',2,'萬雷奔騰',7650,57,1,0,0,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (72,523,436,543,452,225,'爆裂火焰',3,'地獄火',6540,54,1,316,648,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (73,620,422,412,415,295,'圓錐水晶',2,'水晶魔力',6800,55,1,35,340,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (74,655,452,580,450,250,'寒冰魔獸',2,'口中噴出0度冰炎',8000,59,1,35,429,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (75,730,460,660,420,310,'神力巨人',1,'天翻地覆',9300,68,1,0,0,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (76,712,440,600,445,385,'突擊之狼',4,'瘋狂連打',9150,67,1,43,300,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (77,668,430,708,468,225,'魔雕像',6,'雙眼射出死亡光線',8550,66,1,0,0,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (78,670,470,635,416,213,'火戰車',3,'攻擊力上升',8356,62,1,479,675,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (79,700,450,735,460,335,'火焰巨龍',3,'天際出現巨大高溫火球',9500,69,1,562,490,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (80,625,435,735,435,233,'企鵝',2,'黑魔法  冰雪術',8100,63,1,488,684,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (81,728,445,617,412,210,'地獄戰車',6,'攻擊力上升',8900,64,1,149,583,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (82,790,610,650,610,500,'黑暗劍士',3,'手持黑暗魔劍..砍殺對手..',13000,72,1,367,972,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (83,650,625,810,635,520,'雷電魔獸',2,'天降無數奔雷',14500,74,1,0,0,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (84,825,635,680,615,480,'狂風魔獸',5,'真空裂風',14800,75,1,106,366,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (85,868,600,610,650,468,'裂地魔獸',1,'地震術',15600,76,1,0,0,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (86,700,660,885,612,510,'炎熱魔獸',3,'融合術',18000,78,1,480,675,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (87,690,635,890,660,515,'劇毒魔獸',6,'死亡劇毒',17800,79,1,44,332,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (88,780,680,935,720,535,'自然魔獸',4,'呼喚周圍所有動植物攻擊對',21500,82,1,0,0,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (89,945,717,720,690,540,'死靈武士',1,'死靈一擊',23500,84,1,65,422,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (90,950,700,800,735,550,'墮落貴族',2,'投擲百萬金錢',24800,86,1,76,454,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (91,810,725,980,736,515,'墮落天使',5,'聖光術',28600,87,1,229,648,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (92,980,745,800,700,560,'武技長',4,'武學極致',31200,88,1,146,275,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (93,750,760,1100,880,540,'高級祭師',2,'融合術',34000,94,1,342,1296,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (94,650,720,990,780,520,'高級法師',4,'冰天雪地',29000,90,1,0,0,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (95,1080,810,780,790,790,'高級殺手',5,'暗殺',32600,92,1,407,729,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (96,780,790,1150,890,530,'高級巫師',3,'漫天烈火',34800,93,1,220,1377,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (97,1200,860,810,790,780,'高級鬥士',1,'HIT 99',36000,96,1,222,619,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (98,1030,780,720,780,750,'高級弓箭手',5,'狙擊',33300,91,1,0,0,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (99,1250,850,890,850,800,'萬能戰士',6,'萬能一殺',38000,98,1,219,1377,7,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (100,32,20,20,15,12,'哥布林',1,'攻擊力上升',63,6,1,183,648,1,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (101,50,55,95,55,60,'寶箱怪',4,'把對手吸入箱中',420,15,1,184,81,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (102,167,90,100,90,80,'寶石鳥',5,'砸下堅硬寶石',610,23,1,185,81,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (103,120,80,60,80,70,'初級武鬥家',3,'攻擊力上升',410,18,1,186,405,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (104,60,80,120,80,70,'書怪',2,'魔力提升',380,17,1,187,405,2,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (105,180,100,80,100,100,'餓狼',5,'利齒猛咬對手',560,21,1,188,405,3,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (106,360,250,200,250,180,'光明騎士',3,'鬥志上升',1800,36,1,189,810,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (107,200,230,360,230,160,'魔法石',6,'石化術',1600,35,1,190,810,4,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (108,520,300,380,300,250,'遊俠',5,'分身攻擊',5810,51,1,191,810,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (109,780,480,780,490,500,'千古龍',1,'咆哮',9000,66,1,192,664,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (110,580,460,760,460,365,'神木',4,'射出銳利無比的樹葉',8600,62,1,193,688,6,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (111,2300,1300,1800,1200,1400,'冒牌英雄',5,'冒牌必殺',150000,230,1,194,1620,7,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (112,1750,1200,2200,1200,1280,'冒牌召喚師',2,'召喚失敗',120000,235,1,195,1620,7,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (113,2800,1550,2900,1580,1560,'迷路的幻獸',2,'巨大重力魔法',210000,240,1,196,1296,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (114,3320,1800,3100,1800,1900,'幻獸 路行鳥',1,'路行鳥衝撞',300000,260,1,247,972,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (115,3650,1900,3100,1700,2100,'幻獸 伊弗利特',2,'地獄之火',400000,277,1,246,2049,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (116,3100,1650,3700,1900,2250,'幻獸 希瓦',2,'晶鑽',380000,275,1,203,1701,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (117,3150,1700,3800,1950,2380,'幻獸 雷神',5,'仲裁之雷',400000,278,1,356,1458,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (118,4000,2000,3300,1800,2700,'幻獸 大地之神',1,'大地之怒',480000,285,1,118,1458,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (119,4600,2100,4200,2000,3000,'幻獸 海神',2,'大海衝',620000,300,1,265,1811,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (120,4300,2000,4800,2300,3000,'幻獸 不死鳥',3,'轉生之火',680000,305,1,248,1706,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (121,6800,2500,5100,2300,3500,'幻獸 亞歷山大',4,'聖之審判',980000,310,1,213,1863,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (122,8800,2700,6800,2600,3900,'幻獸 奧汀',5,'斬鐵劍',1500000,315,1,214,1844,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (123,15000,3200,13000,3200,4000,'幻獸 巴哈姆特',3,'億萬烈焰',2800000,530,1,336,972,9,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (124,7000,2700,6000,2700,4500,'幻獸 仙人掌',4,'千針攻擊',1600000,338,1,230,1216,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (125,9000,2800,6800,2600,3600,'幻獸 土撥鼠',6,'菜刀',1200000,329,1,257,1687,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (126,8000,2320,8700,2100,4600,'月神',1,'封魔滅神',1960000,312,1,200,1782,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (127,2360,1200,1800,1200,2000,'邪駭浪人',1,'名刀 不知火-斬',180000,290,1,218,1387,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (128,1900,1500,2000,1300,1000,'腐化龍',3,'死亡吐息',180000,210,1,231,1574,7,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (129,20000,3000,18000,3500,5200,'黑暗巴哈姆特',6,'黑暗烈焰',3300000,610,1,280,1403,9,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (131,22000,13000,20000,18000,3100,'使徒',1,'啃食',320000,650,1,0,0,9,NULL,40,0,0,NULL);
INSERT INTO `wog_monster` VALUES (132,10000,3600,12000,4000,3900,'異界守護者',1,'瞬間移動,給予強烈偷襲',1900000,520,1,0,0,9,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (133,26000,4000,16000,3800,2600,'黑暗盟主',2,'無境深淵必殺斬擊',4000000,660,1,266,1568,9,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (134,8500,3200,16000,3200,2900,'魔導結晶',2,'魔導融合',2100000,560,1,327,810,9,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (135,28000,3900,29000,3200,4900,'上古兵器',4,'釋放異界能源',2600000,650,1,278,2202,9,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (136,10000,2300,10000,2300,18000,'異界小強',6,'給予玩家強烈恐怖感',6000000,655,1,253,1936,9,NULL,60,0,0,NULL);
INSERT INTO `wog_monster` VALUES (137,8600,2900,14500,6200,5300,'生化魔物',4,'生化感染',2300000,580,1,0,0,9,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (138,92,60,88,72,130,'猜迷貓',3,'剪刀石頭布',1200,20,1,289,1310,1,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (139,305,211,280,180,210,'盜墓者',6,'投射有毒小刀',2000,32,1,284,1540,3,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (140,140,160,165,110,50,'邪惡侏儒',1,'邪惡氣籠罩四周',1720,25,1,287,1440,2,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (141,250,360,70,35,60,'仙人掌',1,'射出全身的針',550,23,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (142,610,320,460,300,235,'人面獅身',1,'古老的埃及魔咒',6200,50,1,0,0,10,NULL,85,0,0,NULL);
INSERT INTO `wog_monster` VALUES (143,190,130,230,150,100,'風沙怪',5,'夾帶傷人風沙襲擊',620,20,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (144,700,450,730,480,320,'沙漠龍',1,'無人生還的致命攻擊',8300,65,1,262,1350,10,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (145,188,120,160,120,90,'吐沙怪',1,'噴吐致命沙子',500,19,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (146,170,190,150,100,120,'荒漠甲蟲',1,'用堅硬的身軀撞擊',450,19,1,224,283,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (147,200,150,150,140,120,'掠奪禿鷹',5,'用堅硬的嘴襲擊',580,20,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (148,235,180,190,165,110,'挖掘機',3,'丟擲挖掘出來的武器',720,22,1,341,1215,10,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (149,820,540,700,530,460,'骨頭騎士',1,'丟擲身上的骨頭',21000,80,1,0,0,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (150,760,580,880,620,520,'魔手',6,'手指變的非常銳利,刺向敵人',22000,81,1,0,0,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (151,930,700,650,620,720,'人狼騎兵',4,'吶喊攻擊',28000,85,1,270,1166,11,NULL,85,0,0,NULL);
INSERT INTO `wog_monster` VALUES (152,800,980,800,650,430,'石雕',1,'沉重的石雕壓在敵人身上',19000,80,1,433,792,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (153,690,620,840,555,560,'魔岩漿',3,'巨大爆炸',17600,80,1,0,0,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (154,620,530,950,600,600,'幻魔術師',3,'劇毒魔法',22000,82,1,343,1458,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (155,726,632,890,650,580,'幻氣妖',6,'惡毒氣體',20500,81,1,564,380,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (156,730,680,900,680,580,'穴魔',1,'地震術',18200,79,1,0,0,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (157,790,850,800,700,680,'聖甲蟲',2,'聖光術',17600,78,1,225,324,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (158,1300,960,1450,920,850,'德古拉',4,'巨大魔力帶來無止盡的血腥',38000,95,1,261,1490,11,NULL,88,0,0,NULL);
INSERT INTO `wog_monster` VALUES (159,185,110,130,105,150,'巨蠍',1,'尾巴刺向敵人',430,18,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (160,30000,6500,25000,6000,8500,'神龍武者',5,'飛龍在天',4500000,770,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (161,36000,7200,38000,6800,12200,'太陽神阿波羅',3,'炙熱太陽烈焰',5000000,790,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (162,43000,8000,27000,7000,9000,'戰神阿瑞斯',1,'戰鼓齊昂',5800000,800,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (163,29000,5800,46000,7900,13000,'智慧女神雅典娜',4,'女神之矛',4800000,775,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (164,40000,6750,38000,6500,9600,'海神波塞東',2,'呼喚暴風雨',5600000,800,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (165,178,132,160,95,162,'美洲虎',3,'敏捷的身影,對敵人作出猛烈',520,18,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (166,3800,2000,2000,1500,2000,'力量水晶',1,'強力物理攻擊',450000,270,1,332,648,13,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (167,2000,1200,2100,1250,1000,'邪眼伯爵',6,'邪眼幻惑對手',93000,180,1,328,1134,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (168,1000,850,1700,960,900,'蒼天女',5,'引導水晶魔力攻擊對手',52000,130,1,390,972,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (169,1500,920,1300,860,850,'羅剎',4,'瘋狂的連續攻擊',55000,130,1,0,0,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (170,1350,810,860,680,700,'戰鬼',3,'聚氣攻擊',51000,120,1,0,0,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (171,1620,980,980,820,810,'黑耀騎士',1,'火焰爆裂擊',67000,150,1,306,810,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (172,1850,1000,1320,1000,780,'冰石巨人',2,'聚氣攻擊',87000,160,1,329,810,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (173,2000,1500,3800,2000,2000,'智慧水晶',4,'強力魔法攻擊',450000,270,1,301,1000,13,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (174,1300,1300,2200,1200,1000,'天藍魔石',2,'消滅術',80000,165,1,339,1377,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (175,5500,2800,5500,2800,2800,'水晶王',1,'101顆水晶衝擊',850000,320,1,305,1350,13,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (176,3200,1500,3200,1500,4200,'速度水晶',5,'噴射風暴',450000,270,1,302,1000,13,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (177,7000,2000,2000,1800,1500,'豪腕鍊金術師',1,'迷人的力與美',900000,320,1,283,1700,13,NULL,85,0,0,NULL);
INSERT INTO `wog_monster` VALUES (178,2600,1400,2100,1200,1900,'人造人',6,'無限再生',98000,192,1,0,0,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (179,2900,1650,2500,1800,1200,'白耀騎士',3,'鳳凰炸彈',120000,200,1,345,972,13,NULL,70,0,0,NULL);
INSERT INTO `wog_monster` VALUES (180,1720,1620,2310,1930,2650,'破裂魔鏡',2,'飛來無數破裂的鏡片',73000,140,1,344,1563,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (181,32000,8600,56000,7300,22000,'智天使拉斐爾',4,'無人能從神領活出去',6150000,850,1,279,2093,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (182,39000,9000,59000,8200,21000,'智天使加百列',1,'送你去住宿',6530000,860,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (183,65000,9600,63000,9200,25000,'熾天使米迦勒',3,'秒殺是不會有感覺的',7600000,900,1,0,0,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (184,15000,5000,15000,5000,30000,'異界大強',6,'恐怖飛天特大小強',6200000,670,1,282,1598,9,NULL,85,0,0,NULL);
INSERT INTO `wog_monster` VALUES (185,30000,7000,25000,6000,6000,'星河將軍',3,'隕石斬',5000000,680,1,281,1468,9,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (186,10000,5000,18000,3200,4200,'異界魂魄',3,'來自黑洞的哀嚎',3500000,590,1,340,1215,9,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (187,520,600,580,600,800,'皮甲蟲',1,'射出全身的皮甲',14000,70,1,333,729,11,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (188,1500,1000,1000,800,900,'冤魂武士',5,'黑暗攻擊',25000,92,1,286,1540,11,NULL,85,0,0,NULL);
INSERT INTO `wog_monster` VALUES (189,320,280,480,280,280,'迷霧魔女',4,'恐怖魔霧',4000,45,1,288,1440,4,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (190,700,500,500,420,250,'怒神像',1,'神像怒擊',7800,65,1,394,1620,5,NULL,60,0,0,NULL);
INSERT INTO `wog_monster` VALUES (191,900,650,900,650,650,'戰鬥獅王',3,'暴怒獅子吼',18000,75,1,303,1512,6,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (192,10,10,10,10,10,'不死小白',1,'打我打我',45,1,1,223,81,0,NULL,50,0,0,NULL);
INSERT INTO `wog_monster` VALUES (193,0,12000,18000,4000,6000,'五大精靈',1,'五大元素12連環攻擊',2100000,450,1,285,1255,8,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (194,50000,8000,70000,8000,10000,'千年神木',1,'瑪那祝福的力量',5000000,750,1,337,972,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (195,75000,6500,50000,6500,30000,'天堂鳥',5,'萬羽齊飛',5000000,770,1,338,1134,12,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (196,35000,7500,27000,7500,10000,'海賊王',2,'失落船古砲',6200000,720,1,0,0,14,NULL,90,0,0,NULL);
INSERT INTO `wog_monster` VALUES (197,20000,6000,30000,6000,3600,'海女巫',2,'優美迷人的歌聲,讓人如癡如',4000000,700,1,376,1620,14,NULL,50,0,0,NULL);
INSERT INTO `wog_monster` VALUES (198,15000,6800,15000,5000,7200,'深海龍',2,'大海嘯',3800000,690,1,395,1239,14,NULL,30,0,0,NULL);
INSERT INTO `wog_monster` VALUES (199,10000,3800,100000,3800,4500,'異變魚',6,'噴吐連續水球',1700000,600,1,0,0,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (200,12000,2700,8000,2700,3800,'人魚戰士',1,'魚鱗刺',1700000,600,1,368,1296,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (201,6800,1700,6800,1700,2000,'浪漫烏賊',4,'吐出黑墨',900000,320,1,388,1620,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (202,7200,2000,8200,1800,1900,'水妖精',2,'幻化美女迷惑玩家',930000,340,1,0,0,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (203,5400,1600,5900,1700,1500,'風水靈',5,'風中帶著冷冽的水氣',800000,310,1,355,1458,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (204,8300,2900,4000,1800,2000,'貝殼蟲',1,'貝殼撞擊',780000,340,1,0,0,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (205,4800,1600,3100,1600,1600,'海星',1,'我愛水色',520000,280,1,389,1458,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (206,3600,1500,3400,1700,1800,'毒鮑魚',3,'有毒勿食',500000,260,1,392,688,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (207,3000,1200,3200,1300,1400,'珠寶魚',4,'用LV包包拍打玩家',420000,250,1,393,972,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (208,2800,1530,2100,1200,1200,'幸福豚',5,'召喚海底漩渦',300000,220,1,369,1377,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (209,11000,3600,14500,3900,4900,'情侶珊瑚',3,'月亮代表我的心',2000000,650,1,370,1458,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (210,150000,3200,100000,4200,6400,'清蒸檸檬魚',2,'淡淡的香氣中,帶著微酸誘人',2600000,630,1,375,1620,14,NULL,50,0,0,NULL);
INSERT INTO `wog_monster` VALUES (211,1800,1000,1600,1000,870,'兇惡企鵝',1,'一點都不可愛的企鵝',50000,150,1,371,729,14,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (212,380,300,380,230,320,'米列',6,'噴灑有毒物質',3600,40,1,0,0,4,NULL,10,2,0,NULL);
INSERT INTO `wog_monster` VALUES (213,430,320,500,300,300,'暴龍的Fans',3,'Fans的執著與熱情',4900,48,1,401,1,4,NULL,10,6,0,NULL);
INSERT INTO `wog_monster` VALUES (214,700,420,800,480,320,'冰雪魔女',2,'冰風暴',5500,55,1,0,0,5,NULL,10,15,0,NULL);
INSERT INTO `wog_monster` VALUES (215,300,270,320,270,150,'上位青魔導士',4,'召喚古代魔人',3000,42,1,405,1,5,NULL,10,18,0,NULL);
INSERT INTO `wog_monster` VALUES (216,780,400,590,400,320,'紅鱗巨龍',3,'烈焰吐息',8600,59,1,0,0,5,NULL,10,19,0,NULL);
INSERT INTO `wog_monster` VALUES (217,150,70,250,120,90,'黑沼法師',6,'有毒黑霧',700,22,1,0,0,3,NULL,10,20,0,NULL);
INSERT INTO `wog_monster` VALUES (218,280,110,260,100,180,'黑沼守護者',1,'黑沼的神秘力量',1800,29,1,0,0,3,NULL,10,21,0,NULL);
INSERT INTO `wog_monster` VALUES (219,2000,1000,2300,1000,1200,'惡靈伯爵',5,'惡靈妖目力量',80000,170,1,410,720,13,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (220,800,430,820,410,300,'古代遺跡守護者',1,'瘋狂撞擊',8700,60,1,413,1,5,NULL,10,31,0,NULL);
INSERT INTO `wog_monster` VALUES (221,650,400,890,450,500,'舊杖守護者',1,'遺跡力量',7000,62,1,412,1,5,NULL,10,32,0,NULL);
INSERT INTO `wog_monster` VALUES (222,800,420,830,420,470,'惡魔莉莉斯',4,'SM魔鞭',11000,69,1,417,3,6,NULL,10,34,0,NULL);
INSERT INTO `wog_monster` VALUES (223,720,400,740,380,280,'法老王',6,'召喚古埃及戰士',9000,64,1,423,1,10,NULL,10,41,0,NULL);
INSERT INTO `wog_monster` VALUES (224,930,550,900,520,700,'莉吉亞之魂',5,'葛雷的思念',21000,74,1,445,1,6,NULL,10,54,0,NULL);
INSERT INTO `wog_monster` VALUES (225,680,450,720,460,300,'火怒神像',3,'火怒一擊',7200,60,1,0,0,5,NULL,30,0,0,NULL);
INSERT INTO `wog_monster` VALUES (226,15,10,15,10,15,'該死小白',1,'小白拳',40,2,1,0,0,1,NULL,15,0,0,NULL);
INSERT INTO `wog_monster` VALUES (228,192,145,175,110,120,'活死屍',6,'病菌感染',610,23,1,0,0,10,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (229,780,620,820,570,650,'克沙鎮合成獸',5,'疫病感染',20000,82,1,0,0,10,NULL,0,58,0,NULL);
INSERT INTO `wog_monster` VALUES (230,1100,950,1500,950,800,'指揮官 馬力歐',4,'鍊金術攻擊',32000,93,1,0,0,1,NULL,0,59,0,NULL);
INSERT INTO `wog_monster` VALUES (231,1800,1000,1900,1000,1100,'無淵魔導師',3,'無淵魔力',45000,98,1,0,0,11,NULL,0,60,0,NULL);
INSERT INTO `wog_monster` VALUES (232,320,220,300,200,230,'女奴警衛',4,'血色攻擊',1700,36,1,454,1260,4,NULL,0,66,0,NULL);
INSERT INTO `wog_monster` VALUES (233,710,530,570,620,510,'最果水龍',2,'海嘯衝擊',16000,73,1,0,0,15,NULL,0,68,0,NULL);
INSERT INTO `wog_monster` VALUES (234,590,420,630,490,540,'亞魯多城主',1,'暗影之火',14000,70,1,0,0,4,NULL,0,69,0,NULL);
INSERT INTO `wog_monster` VALUES (235,2600,1200,3700,1600,1100,'賽蓮女妖',2,'迷人之樂',470000,295,1,0,0,14,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (236,250,215,350,270,125,'流浪樂手',4,'乘著歌聲的翅膀',2300,37,1,461,765,4,NULL,15,0,0,NULL);
INSERT INTO `wog_monster` VALUES (237,810,560,520,480,420,'最果鱷魚',4,'咬食',16000,72,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (238,780,540,660,530,480,'青綠果樹',4,'發射無數果實',17500,74,1,561,430,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (239,610,490,480,420,330,'大毛蟹',2,'巨夾',8900,68,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (240,820,880,480,450,220,'堅硬龜',1,'硬殼撞擊',15000,74,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (241,720,460,810,490,560,'紅鰻魚',6,'施放毒水',14800,71,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (242,4800,1750,3600,1500,3600,'巡邏人馬',1,'施放迷煙',500000,290,1,527,630,15,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (243,5700,2180,4200,1900,4200,'戰鬥人馬',3,'螺旋射擊',550000,295,1,0,0,15,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (244,4100,2200,6800,3100,4000,'雷霆人馬',5,'雷霆魔力',530000,300,1,511,1260,15,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (245,7200,2200,4200,2800,4500,'暴力人馬',3,'威力斧',620000,306,1,0,0,15,NULL,40,0,0,NULL);
INSERT INTO `wog_monster` VALUES (246,8100,3200,8300,3400,4600,'精英人馬',5,'鬥志上升',690000,308,1,434,657,15,NULL,40,0,0,NULL);
INSERT INTO `wog_monster` VALUES (247,10000,3200,10000,3200,5000,'人馬首領',1,'王族之雷',900000,350,1,0,0,15,NULL,80,0,0,NULL);
INSERT INTO `wog_monster` VALUES (248,5200,2600,5800,2900,2600,'巨型火樹',3,'密集火焰',490000,289,1,565,450,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (249,3600,1250,3200,1600,1600,'小型火樹',3,'小型火焰',200000,180,1,525,774,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (250,835,500,670,500,500,'迅猛鰻魚',2,'快速攻擊',15000,73,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (251,810,480,880,460,350,'長嘴鷹',5,'長嘴咬食',13000,72,1,0,0,15,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (252,5200,2100,8600,1900,2300,'火之亡靈',3,'異變之火',860000,350,1,0,0,14,NULL,10,0,0,NULL);
INSERT INTO `wog_monster` VALUES (253,110,85,145,85,90,'命運火炬',3,'奇襲火焰',520,20,1,0,0,2,NULL,15,97,0,NULL);
INSERT INTO `wog_monster` VALUES (254,2500,1400,1900,1400,1900,'闇炎爆彈',3,'黑色炸藥',87000,190,1,0,0,13,NULL,15,0,0,NULL);
INSERT INTO `wog_monster` VALUES (255,6600,2600,5000,2000,5100,'幻獸 白虎',1,'白虎爪',810000,310,1,0,0,8,NULL,0,0,0,NULL);
INSERT INTO `wog_monster` VALUES (256,5300,2500,5200,2400,3300,'固希爾的領主',1,'必殺斬',500000,300,1,0,0,13,NULL,20,114,0,NULL);
INSERT INTO `wog_monster` VALUES (257,3400,2000,2900,1700,3800,'魔導石翼獸',5,'震天旋風',360000,280,1,519,270,7,NULL,15,123,0,NULL);
INSERT INTO `wog_monster` VALUES (258,4200,2600,3600,2200,4500,'解咒後石翼獸',5,'石翼旋風',400000,285,1,520,1,7,NULL,30,124,0,NULL);
INSERT INTO `wog_monster` VALUES (259,4800,2700,4300,2600,4200,'狼蛛',6,'蜘蛛毒液',420000,287,1,521,1,7,NULL,30,125,0,NULL);
INSERT INTO `wog_monster` VALUES (260,1300,920,1000,800,1000,'地獄門犬',1,'妖火召喚',40000,100,1,0,0,7,NULL,10,127,0,NULL);
INSERT INTO `wog_monster` VALUES (261,5000,2600,6300,2900,2300,'聖水會教主',2,'波濤之浪',430000,310,1,0,0,0,NULL,20,130,0,NULL);
INSERT INTO `wog_monster` VALUES (262,3000,1300,3500,2000,1050,'闇輝祭司',4,'變異的魔力',310000,250,1,0,0,11,NULL,17,120,0,NULL);
INSERT INTO `wog_monster` VALUES (263,3300,2200,3780,1600,1320,'元素殺手',4,'元素能量',326000,265,1,529,1,11,NULL,20,121,0,NULL);
INSERT INTO `wog_monster` VALUES (264,4120,2200,3200,2000,1900,'叢林之王守衛',1,'綠色守護',364000,270,1,0,0,11,NULL,30,122,0,NULL);
INSERT INTO `wog_monster` VALUES (265,0,0,0,0,0,'倫魯',1,NULL,0,0,1,0,0,10,NULL,30,133,1,'我是倫魯\r\n\r\n你想要前往熔炎火山打敗熔炎巨龍？\r\n那你一定會需要我的協助，但是你也必須拿到召喚 希瓦\r\n');
INSERT INTO `wog_monster` VALUES (266,4000,1950,4150,1800,1900,'熔炎巨龍',3,'火山爆發',470000,283,1,534,45,10,NULL,45,134,0,NULL);
INSERT INTO `wog_monster` VALUES (267,2200,1300,1900,1300,1100,'戰爭水晶',1,'戰役之火',98000,182,1,535,585,13,NULL,15,0,0,NULL);
INSERT INTO `wog_monster` VALUES (268,0,0,0,0,0,'瑪琳',2,NULL,0,0,1,0,0,3,NULL,45,135,1,'我是瑪琳\r\n\r\n謝謝您救了我，趕快帶我離開這麼危險的地方吧');
INSERT INTO `wog_monster` VALUES (269,700,540,880,460,495,'深水元素',2,'水精靈攻擊',18000,76,1,537,200,15,NULL,20,0,0,NULL);
INSERT INTO `wog_monster` VALUES (270,920,550,700,480,590,'戰木神',4,'怒殺鐵木',20000,84,1,538,240,6,NULL,30,0,0,NULL);
INSERT INTO `wog_monster` VALUES (271,975,630,1025,620,600,'薩佈雷手下',4,'惡魔詛咒',22000,83,1,540,320,7,NULL,30,137,0,NULL);
INSERT INTO `wog_monster` VALUES (272,4200,1800,4900,1950,3200,'薩佈雷',4,'高級惡魔元素',620000,290,1,541,100,7,NULL,50,138,0,NULL);
INSERT INTO `wog_monster` VALUES (273,0,0,0,0,0,'惡水淨化點',6,NULL,0,0,1,0,0,4,NULL,40,139,1,NULL);
INSERT INTO `wog_monster` VALUES (274,0,0,0,0,0,'克沙淨化點',6,NULL,0,0,1,0,0,10,NULL,40,140,1,NULL);
INSERT INTO `wog_monster` VALUES (275,0,0,0,0,0,'探險者',1,NULL,0,0,1,0,0,5,NULL,20,141,1,NULL);
INSERT INTO `wog_monster` VALUES (276,790,410,600,390,850,'黑蒙夜盜',5,'迅影殺',8600,63,1,545,1,6,NULL,18,142,0,NULL);
INSERT INTO `wog_monster` VALUES (277,0,0,0,0,0,'怪醫 白傑克',4,NULL,0,0,1,0,0,1,NULL,35,144,1,'救治挖掘隊的隊員?趕快動身吧');
INSERT INTO `wog_monster` VALUES (278,2950,1900,2430,1600,1000,'神殿地龍',1,'大地震鳴',100000,210,1,546,100,7,NULL,40,145,0,NULL);
INSERT INTO `wog_monster` VALUES (279,4100,1900,3700,1900,2700,'大地守護者',1,'大地怒吼',150000,290,1,549,120,7,NULL,40,146,0,NULL);
INSERT INTO `wog_monster` VALUES (280,4200,2050,4400,2000,2800,'比比克',1,'地心爆破',250000,310,1,550,135,7,NULL,40,147,0,NULL);
INSERT INTO `wog_monster` VALUES (281,0,0,0,0,0,'魔物據點',6,NULL,0,0,1,0,0,13,NULL,25,149,1,NULL);
INSERT INTO `wog_monster` VALUES (282,0,0,0,0,0,'矮人鐵匠',1,NULL,0,0,1,0,0,1,NULL,40,150,1,NULL);
INSERT INTO `wog_monster` VALUES (283,5200,1800,6200,1900,4200,'風神獸',5,'風之刃',500000,290,1,430,0,0,NULL,35,152,0,NULL);
INSERT INTO `wog_monster` VALUES (284,3400,1800,3000,1900,2200,'魔物軍團 小隊長',4,'衝鋒一擊',420000,280,1,0,0,13,NULL,35,153,0,NULL);
INSERT INTO `wog_monster` VALUES (285,6400,2800,5500,2300,2700,'魔將軍 怒鐵',1,'銅牆鐵壁',720000,320,1,558,100,13,NULL,45,154,0,NULL);
INSERT INTO `wog_monster` VALUES (286,1300,900,1000,800,770,'隕鐵石人',3,'落隕術',42000,100,1,554,600,7,NULL,15,0,0,NULL);

#
# Table structure for table wog_pet
#

DROP TABLE IF EXISTS `wog_pet`;
CREATE TABLE `wog_pet` (
  `pe_id` int(10) unsigned NOT NULL auto_increment,
  `pe_p_id` int(10) unsigned NOT NULL default '0',
  `pe_name` varchar(100) NOT NULL default '',
  `pe_at` smallint(5) unsigned NOT NULL default '0',
  `pe_mt` smallint(5) unsigned NOT NULL default '0',
  `pe_fu` smallint(5) unsigned NOT NULL default '0',
  `pe_def` smallint(5) unsigned NOT NULL default '0',
  `pe_hu` tinyint(3) unsigned NOT NULL default '0',
  `pe_type` tinyint(4) NOT NULL default '1',
  `pe_age` tinyint(3) unsigned NOT NULL default '1',
  `pe_he` tinyint(3) unsigned NOT NULL default '0',
  `pe_fi` tinyint(3) unsigned NOT NULL default '0',
  `pe_dateline` int(10) unsigned NOT NULL default '0',
  `pe_mname` varchar(30) NOT NULL default '',
  `pe_m_id` int(11) NOT NULL default '0',
  `pe_st` tinyint(1) NOT NULL default '0',
  `pe_money` int(11) unsigned NOT NULL default '0',
  `pe_s_dateline` int(11) unsigned NOT NULL default '0',
  `pe_b_dateline` int(11) unsigned NOT NULL default '0',
  `pe_f_dateline` int(10) unsigned NOT NULL default '0',
  `pe_b_old` tinyint(3) unsigned NOT NULL default '0',
  `pe_mimg` varchar(50) default NULL,
  PRIMARY KEY  (`pe_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_pet
#


#
# Table structure for table wog_player
#

DROP TABLE IF EXISTS `wog_player`;
CREATE TABLE `wog_player` (
  `p_id` int(11) unsigned NOT NULL auto_increment,
  `p_name` varchar(64) NOT NULL default '',
  `p_email` varchar(100) NOT NULL default '',
  `p_at` smallint(5) unsigned NOT NULL default '0',
  `p_df` smallint(5) unsigned NOT NULL default '0',
  `p_mat` smallint(5) unsigned NOT NULL default '0',
  `p_mdf` smallint(5) unsigned NOT NULL default '0',
  `p_s` tinyint(2) unsigned NOT NULL default '1',
  `p_url` varchar(100) NOT NULL default '',
  `p_homename` varchar(30) NOT NULL default '',
  `p_ipadd` varchar(20) NOT NULL default '',
  `p_str` smallint(5) unsigned NOT NULL default '0',
  `p_life` smallint(5) unsigned NOT NULL default '0',
  `p_vit` smallint(5) unsigned NOT NULL default '0',
  `p_smart` smallint(5) unsigned NOT NULL default '0',
  `p_agl` smallint(5) unsigned NOT NULL default '0',
  `p_hp` int(11) unsigned NOT NULL default '0',
  `p_luck` tinyint(4) unsigned NOT NULL default '0',
  `p_sat_name` varchar(248) default NULL,
  `p_hpmax` int(11) unsigned NOT NULL default '0',
  `ch_id` tinyint(4) unsigned NOT NULL default '0',
  `p_money` int(10) unsigned NOT NULL default '0',
  `p_lv` int(11) unsigned NOT NULL default '0',
  `p_exp` int(11) unsigned NOT NULL default '0',
  `p_nextexp` int(11) unsigned NOT NULL default '0',
  `p_win` int(10) unsigned NOT NULL default '0',
  `p_lost` int(10) unsigned NOT NULL default '0',
  `p_sex` tinyint(1) unsigned NOT NULL default '0',
  `a_id` smallint(5) unsigned NOT NULL default '0',
  `d_body_id` smallint(5) unsigned NOT NULL default '0',
  `p_password` varchar(10) NOT NULL default '',
  `i_img` tinyint(3) unsigned NOT NULL default '0',
  `p_img_url` varchar(200) NOT NULL default '',
  `p_img_set` tinyint(3) unsigned NOT NULL default '0',
  `p_act_time` int(10) NOT NULL default '0',
  `p_cdate` int(10) NOT NULL default '0',
  `d_head_id` smallint(5) unsigned NOT NULL default '0',
  `d_hand_id` smallint(5) unsigned NOT NULL default '0',
  `d_foot_id` smallint(5) unsigned NOT NULL default '0',
  `d_item_id` smallint(5) unsigned NOT NULL default '0',
  `p_online_time` int(10) NOT NULL default '0',
  `p_bbsid` int(10) unsigned default '0',
  `p_pk_s` tinyint(1) NOT NULL default '0',
  `p_pk_money` mediumint(6) unsigned NOT NULL default '0',
  `p_pk_win` int(10) NOT NULL default '0',
  `p_pk_lost` int(10) NOT NULL default '0',
  `p_cho_win` int(10) unsigned NOT NULL default '0',
  `p_birth` tinyint(3) unsigned NOT NULL default '0',
  `p_place` tinyint(3) unsigned NOT NULL default '0',
  `p_au` smallint(5) unsigned NOT NULL default '0',
  `p_be` smallint(5) unsigned NOT NULL default '0',
  `p_a_win` int(10) unsigned NOT NULL default '0',
  `p_a_lost` varchar(64) NOT NULL default '',
  `p_ch_s_id` tinyint(2) unsigned NOT NULL default '0',
  `p_bank` int(10) unsigned default '0',
  `p_bag` tinyint(3) unsigned NOT NULL default '0',
  `p_lock` tinyint(1) unsigned NOT NULL default '0',
  `p_g_id` int(10) unsigned NOT NULL default '0',
  `p_g_a_id` int(10) unsigned NOT NULL default '0',
  `p_g_morale` tinyint(3) unsigned NOT NULL default '0',
  `p_g_number` smallint(5) unsigned NOT NULL default '0',
  `t_id` int(10) unsigned NOT NULL default '0',
  `p_support` int(10) unsigned NOT NULL default '0',
  `p_key` varchar(6) NOT NULL default '',
  `p_attempts` tinyint(3) unsigned NOT NULL default '0',
  `p_lock_time` int(10) unsigned NOT NULL default '0',
  `p_st` tinyint(1) unsigned NOT NULL default '0',
  PRIMARY KEY  (`p_id`),
  KEY `p_name` (`p_name`),
  KEY `p_support` (`p_support`)
) TYPE=MyISAM;

#
# Dumping data for table wog_player
#

INSERT INTO `wog_player` VALUES (1,'test','me@localhost',9,9,9,9,1,'http://','1234','',9,9,8,9,9,45,8,'',45,6,2000,1,0,1000,0,0,2,0,0,'1234',1,'',0,0,1148204969,0,0,0,0,1148204969,1,0,0,0,0,0,0,0,8,8,0,'',0,0,0,0,0,0,0,0,0,0,'',0,0,0);

#
# Table structure for table wog_race
#

DROP TABLE IF EXISTS `wog_race`;
CREATE TABLE `wog_race` (
  `p_id` int(11) NOT NULL default '0',
  `r_str` varchar(200) NOT NULL default '',
  `dateline` int(11) NOT NULL default '0',
  KEY `p_id` (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_race
#


#
# Table structure for table wog_sale
#

DROP TABLE IF EXISTS `wog_sale`;
CREATE TABLE `wog_sale` (
  `s_id` int(10) unsigned NOT NULL auto_increment,
  `p_id` int(11) NOT NULL default '0',
  `d_id` int(11) NOT NULL default '0',
  `s_money` int(11) unsigned NOT NULL default '0',
  `dateline` int(11) NOT NULL default '0',
  PRIMARY KEY  (`s_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_sale
#


#
# Table structure for table wog_syn
#

DROP TABLE IF EXISTS `wog_syn`;
CREATE TABLE `wog_syn` (
  `syn_id` int(11) NOT NULL auto_increment,
  `syn_result` mediumint(4) unsigned NOT NULL default '0',
  `syn_ele1` mediumint(4) unsigned NOT NULL default '0',
  `syn_ele2` mediumint(4) unsigned NOT NULL default '0',
  `syn_ele3` mediumint(4) unsigned NOT NULL default '0',
  `syn_ele4` mediumint(4) unsigned NOT NULL default '0',
  `syn_ele5` mediumint(4) unsigned NOT NULL default '0',
  PRIMARY KEY  (`syn_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_syn
#

INSERT INTO `wog_syn` VALUES (1,308,125,306,0,0,0);
INSERT INTO `wog_syn` VALUES (2,309,307,126,0,0,0);
INSERT INTO `wog_syn` VALUES (3,310,270,231,236,305,0);
INSERT INTO `wog_syn` VALUES (4,311,122,306,256,315,0);
INSERT INTO `wog_syn` VALUES (5,312,131,220,208,0,0);
INSERT INTO `wog_syn` VALUES (6,313,136,208,316,0,0);
INSERT INTO `wog_syn` VALUES (7,314,132,219,0,0,0);
INSERT INTO `wog_syn` VALUES (8,317,307,332,276,160,0);
INSERT INTO `wog_syn` VALUES (9,318,306,166,128,0,0);
INSERT INTO `wog_syn` VALUES (10,319,183,207,165,115,0);
INSERT INTO `wog_syn` VALUES (11,320,332,203,208,206,0);
INSERT INTO `wog_syn` VALUES (12,321,247,188,200,0,0);
INSERT INTO `wog_syn` VALUES (13,322,316,153,0,0,0);
INSERT INTO `wog_syn` VALUES (14,324,164,323,177,193,230);
INSERT INTO `wog_syn` VALUES (15,325,327,315,161,222,0);
INSERT INTO `wog_syn` VALUES (16,326,327,328,336,195,0);
INSERT INTO `wog_syn` VALUES (17,334,329,330,216,163,0);
INSERT INTO `wog_syn` VALUES (18,335,332,278,219,194,214);
INSERT INTO `wog_syn` VALUES (19,346,320,339,276,333,0);
INSERT INTO `wog_syn` VALUES (20,347,344,345,311,232,213);
INSERT INTO `wog_syn` VALUES (21,348,339,337,329,230,342);
INSERT INTO `wog_syn` VALUES (22,349,342,343,338,193,0);
INSERT INTO `wog_syn` VALUES (23,350,340,331,329,215,0);
INSERT INTO `wog_syn` VALUES (24,351,330,205,188,186,192);
INSERT INTO `wog_syn` VALUES (25,352,327,337,338,315,317);
INSERT INTO `wog_syn` VALUES (26,353,341,334,333,319,306);
INSERT INTO `wog_syn` VALUES (27,354,343,332,315,307,229);
INSERT INTO `wog_syn` VALUES (28,359,321,261,368,246,376);
INSERT INTO `wog_syn` VALUES (29,360,257,322,330,334,375);
INSERT INTO `wog_syn` VALUES (30,361,367,368,353,344,262);
INSERT INTO `wog_syn` VALUES (31,362,352,349,376,342,0);
INSERT INTO `wog_syn` VALUES (32,363,264,257,309,328,375);
INSERT INTO `wog_syn` VALUES (33,364,346,355,345,372,358);
INSERT INTO `wog_syn` VALUES (34,365,370,371,376,312,356);
INSERT INTO `wog_syn` VALUES (35,366,218,229,257,208,358);
INSERT INTO `wog_syn` VALUES (36,377,373,376,327,324,0);
INSERT INTO `wog_syn` VALUES (37,378,368,370,373,363,0);
INSERT INTO `wog_syn` VALUES (38,379,321,302,290,374,0);
INSERT INTO `wog_syn` VALUES (39,380,342,338,343,312,0);
INSERT INTO `wog_syn` VALUES (40,381,375,344,311,232,200);
INSERT INTO `wog_syn` VALUES (41,382,372,373,357,305,217);
INSERT INTO `wog_syn` VALUES (42,383,355,356,345,344,303);
INSERT INTO `wog_syn` VALUES (43,384,301,320,203,205,118);
INSERT INTO `wog_syn` VALUES (44,385,356,266,363,309,394);
INSERT INTO `wog_syn` VALUES (45,386,389,355,356,365,265);
INSERT INTO `wog_syn` VALUES (46,387,388,390,253,321,338);
INSERT INTO `wog_syn` VALUES (47,486,482,451,453,315,152);
INSERT INTO `wog_syn` VALUES (48,487,482,453,451,345,303);
INSERT INTO `wog_syn` VALUES (49,493,355,357,332,0,0);
INSERT INTO `wog_syn` VALUES (50,499,375,344,323,275,395);
INSERT INTO `wog_syn` VALUES (52,516,357,342,1,0,0);
INSERT INTO `wog_syn` VALUES (53,517,357,372,333,0,0);

#
# Table structure for table wog_team_join
#

DROP TABLE IF EXISTS `wog_team_join`;
CREATE TABLE `wog_team_join` (
  `t_j_id` int(10) unsigned NOT NULL auto_increment,
  `t_id` int(10) unsigned NOT NULL default '0',
  `p_id` int(10) unsigned NOT NULL default '0',
  `t_j_dateline` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`t_j_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_team_join
#


#
# Table structure for table wog_team_main
#

DROP TABLE IF EXISTS `wog_team_main`;
CREATE TABLE `wog_team_main` (
  `t_id` int(10) unsigned NOT NULL auto_increment,
  `p_id` int(10) unsigned NOT NULL default '0',
  `t_name` varchar(160) NOT NULL default '',
  `t_peo` tinyint(4) unsigned NOT NULL default '0',
  `t_time` int(10) unsigned NOT NULL default '0',
  PRIMARY KEY  (`t_id`),
  KEY `t_time` (`t_time`),
  KEY `p_id` (`p_id`)
) TYPE=MyISAM;

#
# Dumping data for table wog_team_main
#

