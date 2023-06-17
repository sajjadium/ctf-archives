SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `idx` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `pw` varchar(50) DEFAULT NULL,
  `isAdmin` int(11) DEFAULT NULL,
  PRIMARY KEY (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (
  `username`,
  `pw`,
  `isAdmin`
  ) VALUES (
    "admin",
    "dade533ebe440bc025c0f8022149ff6d",
    1
  );

  INSERT INTO `user` (
  `username`,
  `pw`,
  `isAdmin`
  ) VALUES (
    "guest",
    "79f1e6c833cbabc35c90711258135ad7",
    0
  );