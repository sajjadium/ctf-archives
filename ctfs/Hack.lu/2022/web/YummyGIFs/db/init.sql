CREATE TABLE users (
      id INTEGER AUTO_INCREMENT PRIMARY KEY,
      name TEXT,
      password TEXT
    )
    DEFAULT CHARSET=utf8;

CREATE TABLE gifs (
      id INTEGER AUTO_INCREMENT PRIMARY KEY,
      random_id TEXT,
      name TEXT,
      title TEXT,
      description TEXT,
      user_id INTEGER,
      timestamp TIMESTAMP DEFAULT (UTC_TIMESTAMP()),
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
    DEFAULT CHARSET=utf8;  

INSERT INTO users (name, password) VALUES ('admin', '$argon2id$v=19$m=65536,t=4,p=1$YWhMVEEwWHBYM210WmNXLg$pgkCvfZCx86AWyy+FQz5QbuW8Bh3zAOSZeuceZzUGRE');
INSERT INTO gifs (random_id, name, title, description, user_id) VALUES ('RANDOM_ID', 'flag.gif', 'Cool flag', '', 1);