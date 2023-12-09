
CREATE USER "admin"@"%" IDENTIFIED BY "REDACTED";
CREATE DATABASE IF NOT EXISTS bot;

USE bot;

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users
(
        id int AUTO_INCREMENT,
        username varchar(255) UNIQUE,
        password varchar(255),
        curve_private_key varchar(255),
        session_key varchar(255),
        enabled boolean DEFAULT true,
        motto varchar(255),
        balance float,
        coupon varchar(36),
        shield timestamp,
        PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS reports
(
        id int AUTO_INCREMENT,
        user_id int UNIQUE,
        url varchar(255),
        PRIMARY KEY(id),
        FOREIGN KEY (user_id) references users(id)
);

CREATE TABLE IF NOT EXISTS actions
(
        id int AUTO_INCREMENT,
        name varchar(255) UNIQUE,
        owner int,
        price float NOT NULL,
        text varchar(255),
        PRIMARY KEY(id),
        FOREIGN KEY (owner) references users(id)
);


INSERT INTO users(username, password, balance, shield) VALUES ("admin","$2a$10$TNoo6JxBs46vgH5fDbE4R.4zb.im8t83L6tDRppx34/FjicQBBGT2", 0, NULL);
INSERT INTO actions(name, owner, price) VALUES ("forward", 1, 5), ("backward", 1, 5), ("left", 1, 5), ("right", 1, 5), ("camera",1, 5);
GRANT ALL ON bot.* TO "admin"@"%";

