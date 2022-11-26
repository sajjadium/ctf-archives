SET NAMES utf8mb4;

USE `yeeclass`;

CREATE TABLE `homework` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `open` bit(1) NOT NULL,
  `public` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `homework` VALUES (1,'Flag','Please submit the flag.',0,0),(2,'Public Homework','You can view the submission list of the public homework!',1,1),(3,'Non-Public Homework','Only TAs and the teacher can view the submission list of the non-public homework!',1,0);

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(12) NOT NULL,
  `password` varchar(32) NOT NULL,
  `class` tinyint(4) NOT NULL DEFAULT -1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `submission` (
  `hash` varchar(40) NOT NULL,
  `content` text NOT NULL,
  `time` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `userid` int(11) NOT NULL,
  `homeworkid` int(11) NOT NULL,
  `score` int(10) unsigned DEFAULT NULL,
  KEY `userid` (`userid`),
  KEY `homeworkid` (`homeworkid`),
  CONSTRAINT `submission_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `submission_ibfk_2` FOREIGN KEY (`homeworkid`) REFERENCES `homework` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;