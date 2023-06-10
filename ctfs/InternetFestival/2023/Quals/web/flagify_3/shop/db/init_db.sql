USE shop_db;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(200) NOT NULL,
    password_hash CHAR(64) NOT NULL,
    salt CHAR(10),

    PRIMARY KEY (id)
);

CREATE TABLE item(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    content VARCHAR(300) NOT NULL,
    cost INT NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE transaction(
    id VARCHAR(10) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    status BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);

INSERT INTO item VALUES
    (DEFAULT, 'Woman yelling at cat', 'https://imgflip.com/i/7o8gzg', 10),
    (DEFAULT, '0ni_giri', 'https://www.instagram.com/p/Cp7rQLQstbx/?igshid=MzRlODBiNWFlZA==', 10),
    (DEFAULT, 'anime_mortacci', 'https://www.instagram.com/p/CZPLYA7qfXb/?igshid=MzRlODBiNWFlZA==', 10),
    (DEFAULT, 'la.malevisione', 'https://www.instagram.com/p/CeirYKJshnq/?igshid=MzRlODBiNWFlZA==', 10),
    (DEFAULT, 'flag', 'flag{placeholder}', 100);
