#!/bin/sh

#https://hashtoolkit.com/common-passwords/
sqlite3 /srv/app/dbs/hashes.db <<EOF
CREATE TABLE UnsecurePasswordsHash (value);
INSERT INTO UnsecurePasswordsHash (value) VALUES ('e10adc3949ba59abbe56e057f20f883e');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('d8578edf8458ce06fbc5bb76a58c5ca4');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('25f9e794323b453885f5181f1b624d0b');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('827ccb0eea8a706c4c34a16891f84e7b');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('81dc9bdb52d04dc20036dbd8313ed055');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('96e79218965eb72c92a549dd5a330112');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('fcea920f7412b5da7be0cf42b8c93759');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('8621ffdbc5698829397d97767ac13db3');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('4297f44b13955235245b2497399d7a93');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('276f8db0b86edaa7fc805516c852c889');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('e99a18c428cb38d5f260853678922e03');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('d0763edaa9d9bd2a9516280e9044d885');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('6eea9b7ef19179a06954edd0f6c05ceb');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('c8837b23ff8aaa8a2dde915473ce0991');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('bee783ee2974595487357e195ef38ca2');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('e807f1fcf82d132f9bb018ca6738a19f');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('0acf4539a14b3aa27deeb4cbdf6e989f');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('596a96cc7bf9108cd896f33c44aedc8a');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('b36d331451a61eb2d76860e00c347396');
INSERT INTO UnsecurePasswordsHash (value) VALUES ('ef4cdd3117793b9fd593d7488409626d');
.exit
EOF

