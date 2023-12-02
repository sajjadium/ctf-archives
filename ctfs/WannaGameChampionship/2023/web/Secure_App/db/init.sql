USE mydb;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `username` varchar(20) UNIQUE NOT NULL,
  `password` varchar(32) NOT NULL,
  `isAdmin` BOOLEAN
);

SET @admin_password := LOAD_FILE('/var/lib/mysql-files/flag');

INSERT INTO `users` (`username`, `password`, `isAdmin`) VALUES('admin', MD5(@admin_password), true);
