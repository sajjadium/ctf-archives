USE comic_catalog;

CREATE TABLE user (
	id serial primary key,
	username varchar(24) not null unique,
	password text not null,
	is_admin boolean default false
);

CREATE TABLE issue (
	id serial primary key,
	author_id int not null references user (id),
	draft boolean not null default true,
	title text not null,
	content text not null,
	image text not null
);

CREATE TABLE admin_queue (
	id serial primary key,
	issue_id int not null references issue (id)
);

INSERT INTO user (username, password, is_admin) VALUES ('admin', 'nope', false);

INSERT INTO issue (author_id, draft, title, content, image)
SELECT
	id,
	false,
	'Action Comics No. 1',
	'The first issue of Action Comics, including the first appearance of many superheroes, such as Superman and Chuck Dawson.  [POW!]',
	'https://images-na.ssl-images-amazon.com/images/S/cmx-images-prod/Item/12613/12613._SX1600_QL80_TTD_.jpg'
FROM
	user;

INSERT INTO issue (author_id, draft, title, content, image)
SELECT
	id,
	false,
	'The Amazing Spider Man No. 1',
	'Features the first appearance of Batman in "The Case of the Chemical Syndicate", among other tales of mystery and intrigue.',
	'https://images-na.ssl-images-amazon.com/images/S/cmx-images-prod/Item/10900/ICO001306_2._SX1600_QL80_TTD_.jpg'
FROM
	user;

INSERT INTO issue (author_id, draft, title, content, image)
SELECT
	id,
	false,
	'Plaid Comics No. 1',
	'The flag is https://www.youtube.com/watch?v=dQw4w9WgXcQ, jk id=4 is flag',
	'https://previews.123rf.com/images/roywylam/roywylam1505/roywylam150500001/39898173-checkered-flag-chequered-flag.jpg'
FROM
	user;

INSERT INTO issue (author_id, title, content, image)
SELECT
	id,
	'BsidesA Comics No. 1',
	'The flag is NEKO{THIS_IS_FAKE_FLAG}',
	'https://previews.123rf.com/images/roywylam/roywylam1505/roywylam150500001/39898173-checkered-flag-chequered-flag.jpg'
FROM
	user;
