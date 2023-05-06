SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP DATABASE IF EXISTS `memo`;
CREATE DATABASE `memo` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `memo`;

DROP TABLE IF EXISTS `memos`;
CREATE TABLE `memos` (
  `idx` int(255) NOT NULL AUTO_INCREMENT,
  `name` text,
  `memo` text,
  PRIMARY KEY (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
