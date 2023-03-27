CREATE TABLE blog(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20), message VARCHAR(500));
INSERT INTO blog(name, message) VALUES('Super Admin', '<script>alert("XSS")</script>');

CREATE TABLE account(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20), user VARCHAR(20), pass VARCHAR(20));
INSERT INTO account(name, user, pass) VALUES('super_admin', 'super_admin', HEX(RANDOMBLOB(16)));
INSERT INTO account(name, user, pass) VALUES('admin', 'admin', HEX(RANDOMBLOB(16)));
INSERT INTO account(name, user, pass) VALUES('guest', 'guest', 'guest');

CREATE TABLE sess(token BLOB, priv INT);
INSERT INTO sess(token, priv) VALUES(RANDOMBLOB(16), 1);