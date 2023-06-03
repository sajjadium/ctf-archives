CREATE USER 'agent' IDENTIFIED BY 'SUPERSECUREUNCRACKABLEPASSWORD';

CREATE DATABASE IF NOT EXISTS cryptomarket;

USE cryptomarket;

DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user
(
        id int AUTO_INCREMENT,
        username varchar(255),
        password varchar(255),
        identifier varchar(800),
        PRIMARY KEY(id)
);

DROP TABLE IF EXISTS products;

CREATE TABLE IF NOT EXISTS products
(
        id int AUTO_INCREMENT,
        name varchar(255),
        price varchar(255),
        PRIMARY KEY(id)
);

DROP TABLE IF EXISTS cart;

CREATE TABLE IF NOT EXISTS cart
(
        id int AUTO_INCREMENT,
        productid int,
        userid int,
        PRIMARY KEY(id)
);

INSERT INTO products(name,price) VALUES
        ('bitcoin','50000'),
        ('ethereum','20000'),
        ('monero','15000'),
        ('dogecoin','0.000000000013');

GRANT ALL PRIVILEGES ON cryptomarket.* TO 'agent'@'%';
FLUSH PRIVILEGES;