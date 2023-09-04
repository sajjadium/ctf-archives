SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `board`;
CREATE TABLE `board` (
  `idx` int(11) NOT NULL AUTO_INCREMENT,
  `title` text,
  `content` text,
  `file_path` varchar(200) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  `require_level` int(10) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `note`;
CREATE TABLE `note` (
  `idx` varchar(30) NOT NULL,
  `to_id` varchar(50) NOT NULL,
  `from_id` varchar(50) NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `date` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `idx` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `pw` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `profilebio` varchar(1000) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `point` int(50) DEFAULT NULL,
  `is_admin` int(11) DEFAULT NULL,
  `is_note` int(11) DEFAULT NULL,
  PRIMARY KEY (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (
  `username`,
  `pw`,
  `email`,
  `profilebio`,
  `level`,
  `point`,
  `is_admin`,
  `is_note`
  ) VALUES (
    "admin",
    "dade533ebe440bc025c0f8022149ff6d",
    "admin@admin.com",
    "hihi",
    255,
    999999,
    1,
    0
  );