DROP database IF EXISTS ctf;
CREATE database ctf;
USE ctf;
CREATE TABLE secrets 
(
    flag TEXT
);
CREATE TABLE cats 
(
    name TEXT
);
-- flag format: /^ASIS{[a-z]+}$/ 
INSERT INTO secrets VALUES ('ASIS{testflag}');
INSERT INTO cats VALUES ('pishi');
INSERT INTO cats VALUES ('majid');
CREATE USER ctf@'%' IDENTIFIED BY 'ctf';
GRANT SELECT ON ctf.secrets TO 'ctf'@'%';
GRANT SELECT ON ctf.cats TO 'ctf'@'%';
FLUSH PRIVILEGES;

