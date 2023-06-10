USE bank_db;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(200) NOT NULL,
    password_hash CHAR(64) NOT NULL,
    salt CHAR(10),
    credit INT NOT NULL DEFAULT 0,
    totp_secret CHAR(32),

    PRIMARY KEY (id)
);

INSERT INTO user VALUES
    (DEFAULT, 'admin', 'admin_password', 'admin_salt', 10000000, NULL);
