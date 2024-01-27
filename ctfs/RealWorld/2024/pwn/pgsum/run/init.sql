CREATE TABLE RWCTF (Points varchar);
INSERT INTO RWCTF VALUES ('1'), ('337'), ('3.1e4'), ('-1.0');
CREATE USER ctf WITH password '123qwe!@#QWE';
ALTER USER ctf SET default_transaction_read_only=on;
GRANT USAGE ON SCHEMA public to ctf;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ctf;


