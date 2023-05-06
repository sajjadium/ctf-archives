CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    author VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    texts VARCHAR(2048) NOT NULL
);

CREATE TABLE IF NOT EXISTS requests (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    book_id INT NOT NULL
);

INSERT INTO books(title, author, price, texts) VALUES('Maple Stories', 'Maple-Chan', 0, 'FLAGE');
INSERT INTO books(title, author, price, texts) VALUES('Beating Me: Three essentials for playing the honk market', 'Sir Bacon', 0, 'Dont, dont, dont');
INSERT INTO books(title, author, price, texts) VALUES('Tetrio Strategy Guide', 'Addicted folks @ Maple Bacon', 0, 'Press 4, mind your own business, ???, win game');
INSERT INTO books(title, author, price, texts) VALUES('Midnight Owos - Maple Land Bestiary', 'Syrup', 0, 'TBD');

CREATE USER 'player'@'%' IDENTIFIED WITH mysql_native_password BY 'Player123!';
GRANT INSERT ON requests TO 'player'@'%';
GRANT SELECT ON *.* TO 'player'@'%';
FLUSH PRIVILEGES;