
USE colorgram_db;

CREATE TABLE `users` (
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO users (name,email,password,description) values ('admin', 'admin@gmail.com', 'REDACTED', 'I would like to visit sardinia!');

