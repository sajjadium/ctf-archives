CREATE DATABASE IF NOT EXISTS `app` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use `app`;

CREATE TABLE IF NOT EXISTS `users`(
  `id` VARCHAR(32) NOT NULL PRIMARY KEY,
  `pw` VARCHAR(64) NOT NULL,
  `created` DATETIME
);

CREATE TABLE IF NOT EXISTS `posts`(
  `no` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `writer` VARCHAR(32),
  `views` INT
);

INSERT INTO `users` VALUES ('admin', '[FILTER]', now());
INSERT INTO `posts` VALUES (0, 'flag', 'codegate2022{EXAMPLE_FLAG}', 'admin', 0);