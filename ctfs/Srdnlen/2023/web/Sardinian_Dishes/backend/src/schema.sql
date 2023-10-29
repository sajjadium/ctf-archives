CREATE TABLE IF NOT EXISTS recipes (ID integer primary key, name varchar(20), details varchar(100));

CREATE TABLE IF NOT EXISTS illegalrecipes (ID integer primary key, name varchar(20), details varchar(100));


INSERT INTO recipes (name, details) VALUES ('malloreddus', 'https://ricette.giallozafferano.it/Malloreddus-alla-campidanese.html');
INSERT INTO recipes (name, details) VALUES ('seadas', 'https://ricette.giallozafferano.it/Seadas-sebadas.html');
INSERT INTO recipes (name, details) VALUES ('carasau bread', 'https://www.cookaround.com/ricetta/Pane-carasau.html');
INSERT INTO illegalrecipes (name, details) VALUES ('casu marzu', 'srdnlen{REDACTED}');

