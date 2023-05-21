CREATE DATABASE IF NOT EXISTS `challenge` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `challenge`;

CREATE TABLE `albums` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `year` int(11) NOT NULL,
  `genre` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

INSERT INTO `albums` 
VALUES (1,'Almighty So','Chief Keef',2013,'Drill Rap','2020-05-01 00:00:00','2020-05-01 00:00:00'),
(2,'The Wall','Pink Floyd',1979,'Progressive Rock','2020-05-01 00:00:00','2020-05-01 00:00:00'),
(3,'Trap Back','Gucci Mane',2012,'Hip Hop','2020-05-01 00:00:00','2020-05-01 00:00:00'),
(4,'Thriller','Michael Jackson',1982,'Pop','2020-05-01 00:00:00','2020-05-01 00:00:00'),
(5, 'Anti', 'Rihanna', 2016, 'Pop', '2020-05-01 00:00:00','2020-05-01 00:00:00');

CREATE TABLE `flag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flag` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

INSERT INTO `flag`
VALUES (1,'REDACTED', '2020-05-01 00:00:00','2020-05-01 00:00:00');