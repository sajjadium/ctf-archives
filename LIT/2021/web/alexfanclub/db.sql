PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE achievements(
achievement TEXT PRIMARY KEY NOT NULL
);
INSERT INTO achievements VALUES('CF Master');
INSERT INTO achievements VALUES('USACO camper');
INSERT INTO achievements VALUES('pro skillz piano player');
INSERT INTO achievements VALUES('Actually bought sublime text :o');
INSERT INTO achievements VALUES('Knows more chinese than you');
INSERT INTO achievements VALUES('Supreme Leader/Cult Leader of LexMACS');
INSERT INTO achievements VALUES('Organized LIT');
INSERT INTO achievements VALUES('OP at web development');
INSERT INTO achievements VALUES('Puts using namespace std; as the FIRST LINE in his code :O');
INSERT INTO achievements VALUES('Too cool for #include <bits/stdc++.h>');
INSERT INTO achievements VALUES('Top tier MS Paint skills');
INSERT INTO achievements VALUES('Has an informative Youtube channel');
INSERT INTO achievements VALUES('Carried OlyFans during mBIT');
INSERT INTO achievements VALUES('Got top 10 for HSCTF 8');
INSERT INTO achievements VALUES('Is super cool');
INSERT INTO achievements VALUES('Knows fishy15 :yum:');
INSERT INTO achievements VALUES('Has discord nitro');
INSERT INTO achievements VALUES('Beat lots of IGMs in CF Round 728');
INSERT INTO achievements VALUES('Went from pupil to master in ONE year');
INSERT INTO achievements VALUES('Practices consistently orz');
INSERT INTO achievements VALUES('Created USACO Rating');
INSERT INTO achievements VALUES('Able to make better website designs than this');
INSERT INTO achievements VALUES('Able to get AC while using Scanner instead of BufferedReader in Java/Kotlin');
INSERT INTO achievements VALUES('Has a cool profile picture');
CREATE TABLE redacted(
redacted TEXT PRIMARY KEY NOT NULL
);
INSERT INTO redacted VALUES('flag{redacted}');
COMMIT;
