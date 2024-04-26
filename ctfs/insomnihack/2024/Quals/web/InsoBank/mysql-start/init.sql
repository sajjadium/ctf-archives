use inso24;

CREATE TABLE users(id integer auto_increment, username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT, primary key(id));
CREATE TABLE accounts(id varchar(36), name text, userid integer references users, balance DECIMAL(10,2), primary key (id));
CREATE TABLE batches(id varchar(36), locked boolean default false, senderid varchar(36) references accounts, userid integer references users, verified boolean default false, executed boolean default false, primary key(id));
CREATE TABLE batch_transactions(id varchar(36), batchid varchar(36) references batches, recipient varchar(36) references accounts, amount DECIMAL(10,2), verified boolean default false, executed boolean default false, primary key(id));