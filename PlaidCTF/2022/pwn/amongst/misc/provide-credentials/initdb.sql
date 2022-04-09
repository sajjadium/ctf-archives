CREATE TABLE users (id serial primary key, username text, password text);
INSERT INTO users (username, password) VALUES ('zuck', 'hunter2');
INSERT INTO users (username, password) VALUES ('randall', 'correcthorsebatterystaple');
INSERT INTO users (username, password) VALUES ('richard', 'cowabunga');

CREATE TABLE flag (flag text);
INSERT INTO flag (flag) VALUES ('PCTF{SAMPLE_WEB_FLAG}');

CREATE USER amongst WITH PASSWORD 'amongst';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO amongst;
