CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    uuid TEXT NOT NULL,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    last_update TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');
INSERT INTO notes (uuid, username, title, content, last_update) VALUES ('11111111-1111-1111-1111-111111111111', 'admin', 'Flag', 'Hero{FAKE_FLAG}', 'Sun Mar 26 23:39:11 2023');
