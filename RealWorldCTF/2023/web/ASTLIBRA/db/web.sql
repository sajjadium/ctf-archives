DROP TABLE IF EXISTS users;
create table users (id int NOT NULL AUTO_INCREMENT, username varchar(30), password varchar(30), PRIMARY KEY (id));
DROP TABLE IF EXISTS jobs; 
create table jobs (id int NOT NULL AUTO_INCREMENT, zep_file MEDIUMTEXT, `namespace` varchar(20), 
   `class` varchar(20), checked int, result MEDIUMBLOB,
   PRIMARY KEY (id));