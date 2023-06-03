CREATE USER 'agent' IDENTIFIED BY 'SUPERSECUREUNCRACKABLEPASSWORD';

CREATE DATABASE IF NOT EXISTS securehash;

USE securehash;

DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user
(
        id int AUTO_INCREMENT,
        username varchar(255),
        password varchar(255),
        PRIMARY KEY(id)
);
DROP TABLE IF EXISTS roles;

CREATE TABLE IF NOT EXISTS roles
(
        id int,
        roleString varchar(20),
        FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE
);

INSERT INTO
    user (username,password)
VALUES
    ('fakeuser1', '$2y$10$X3w7B.o91rytA3svq1dNHOHhKkQnqlD2zX8Ntym9x/7Fm4fW2XYuG'),
    ('fakeuser2', '$2y$10$tUS44aP8K7T9CZlKCtpfAu3P/ymX3EIxdIdZdFJ.TUOJsL71WieeK');

INSERT INTO
    roles (id,roleString)
VALUES
    ((SELECT id from user WHERE username = "fakeuser1"), 'user'),
    ((SELECT id from user WHERE username = "fakeuser2"), 'admin');

GRANT SELECT ON securehash.* TO 'agent'@'%';
FLUSH PRIVILEGES;