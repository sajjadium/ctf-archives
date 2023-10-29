CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, title TEXT NOT NULL, thread TEXT NOT NULL, verified INTEGER DEFAULT 0 NOT NULL);


INSERT INTO users (username, password) VALUES ('admin', 'srdnlen{REDACTED}');
INSERT OR REPLACE INTO threads (id, title, thread, verified) VALUES ('0', 'Patch Note', '<i style="color: cyan;">HTML support has been added,</i> <b style="color:red">enjoy ;)</b>', 1);
INSERT OR REPLACE INTO threads (id, title, thread, verified) VALUES ('1', 'DISCLAIMER', "Admin here! To avoid spam and phishing I've decided to approve every post/thread manually. Please submit your threads and wait for approval If you can't wait try sending them to me: I'll do my best.", 1);
INSERT OR REPLACE INTO threads (id, title, thread, verified) VALUES ('2', 'Welcome', "Welcome to my anonymous sharing community. You don't need all those onion things, post about anything, have fun!", 1);