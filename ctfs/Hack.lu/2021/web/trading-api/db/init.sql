CREATE DATABASE trading_api;
\connect trading_api;

CREATE TABLE IF NOT EXISTS transactions (
    id BIGINT NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    asset TEXT NOT NULL,
    amount INT NOT NULL
);

CREATE TABLE IF NOT EXISTS flag (flag TEXT PRIMARY KEY);
DELETE FROM flag;
INSERT INTO flag (flag) VALUES ('fakeflag{dummy}');

CREATE ROLE trading_api WITH LOGIN ENCRYPTED PASSWORD 'secret';
GRANT SELECT ON flag TO trading_api;
GRANT SELECT ON transactions TO trading_api;
GRANT INSERT ON transactions TO trading_api;
