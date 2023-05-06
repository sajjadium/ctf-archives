CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name text NOT NULL UNIQUE,
	password text NOT NULL -- bcrypt hash
);

CREATE TABLE shows (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name text NOT NULL,
	cover_url text NOT NULL,
	description text NOT NULL,
	owner uuid NOT NULL REFERENCES users(id)
);

CREATE TABLE episodes (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name text NOT NULL,
	description text NOT NULL,
	url text NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	show uuid NOT NULL REFERENCES shows(id),
	index int NOT NULL CHECK (index >= 0),
	CONSTRAINT show_episode UNIQUE (show, index)
);

CREATE TABLE user_episode_ratings (
	"user" uuid NOT NULL REFERENCES users(id),
	episode uuid NOT NULL REFERENCES episodes(id),
	rating int NOT NULL CHECK (rating >= 0 AND rating <= 5),
	CONSTRAINT user_episode_rating UNIQUE ("user", episode)
);

CREATE TABLE genres (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name text NOT NULL
);

CREATE TABLE show_genres (
	show uuid NOT NULL REFERENCES shows(id),
	genre uuid NOT NULL REFERENCES genres(id),
	CONSTRAINT show_genre UNIQUE (show, genre)
);

CREATE TABLE playlists (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	owner uuid NOT NULL REFERENCES users(id),
	name text NOT NULL,
	description text NOT NULL
);

CREATE TABLE playlist_episodes (
	playlist uuid NOT NULL REFERENCES playlists(id),
	episode uuid NOT NULL REFERENCES episodes(id),
	index int NOT NULL CHECK (index >= 0),
	CONSTRAINT playlist_episode UNIQUE (playlist, episode),
	CONSTRAINT playlist_episode_index UNIQUE (playlist, index)
);

-- Seed data

INSERT INTO users (name, password) VALUES ('admin', 'thisisnotavalidpasswordhash'); -- password is reset by the server on startup

INSERT INTO shows (id, name, cover_url, description, owner)
VALUES
	(
		'647f1187-28c6-4c5d-91d2-1ec895fcb8db',
		'The Seagull''s Nest',
		'/the-seagulls-nest.png',
		'Follow the adventures of a plucky young seagull named Skye, who dreams of becoming a pirate! When Skye discovers a magical amulet that transports her to a strange and mysterious island, she befriends a rebellious pirate captain named Edie and an adorably tiny first mate named Squawk. Despite not having any pirate skills and having to pose as a seasoned pirate due to the prejudice towards seagulls, Skye pursues her dream of becoming a pirate by serving as Edie''s apprentice at the Seagull''s Nest and ultimately finds a new family in an unlikely setting. Along the way, Skye and her new friends must face dangerous sea creatures, navigate treacherous waters, and outwit rival pirate crews in order to protect their home and claim their place on the high seas.',
		(SELECT id FROM users WHERE name = 'admin')
	),
	(
		'162f015d-b1ff-47b6-b26b-1c1471f9f7c6',
		'Over the Deck Rail',
		'/over-the-deck-rail.png',
		'The show follows two brothers, Deck and Rail, who become lost at sea and are swept into a strange and mysterious world called the Uncharted. In order to find their way back home, the brothers must navigate the treacherous waters of the Uncharted with the help of a wise, elderly Pirate Captain and Bertie, an irritable parrot who travels with the brothers in order to undo a curse that has affected her whole family. Deck, the elder brother, is self-absorbed and would rather keep to himself than to have to make a decision. His two passions are treasure hunting and nautical charting, but he keeps this private out of fear of being mocked. On the other hand, Rail, the younger brother, is all about adventure and being carefree, much to Deck''s chagrin and the danger of himself and others. Rail carries a monkey, whose name is undetermined and can communicate only through drumming. Stalking the main cast is the Kraken, an ancient sea monster who leads lost sailors astray until they give up and turn into "Barnacle-encrusted shipwrecks".',
		(SELECT id FROM users WHERE name = 'admin')
	),
	(
		'48affca1-68bf-46c7-916b-213824e7dd67',
		'Brilliant Beetle',
		'/brilliant-beetle.png',
		'The show follows the exploits of two teenage pirates, Marie and Aaron, who transform into the legendary duo, Brilliant Beetle and Black Cat, to fight against the notorious pirate captain, Butterfly Baron.\n\nButterfly Baron is a notorious pirate who commands a formidable fleet of ships and seeks to dominate the seas. Marinette and Adrien must use their wits and skills to outsmart Butterfly Baron''s schemes and protect innocent ships and sailors from his attacks.\n\nAlong the way, they must face a variety of eccentric villains, including the hypnotic Squid Queen and the clumsy duo of Plank and Plunder. With the help of their trusty ship and crew, Brilliant Beetle and Black Cat must outwit Butterfly Baron and his minions to ensure that the seas remain free and open to all.',
		(SELECT id FROM users WHERE name = 'admin')
	),
	(
		'7f274e25-1a9f-456b-b859-5d77125139cd',
		'Eternal Cruise',
		'/eternal-cruise.png',
		'The show follows the adventures of a young pirate named Jack and his talking parrot, Polly, as they navigate through a never-ending cruise ship that sails through the vast ocean. Jack and Polly confront their own fears and shortcomings while helping their fellow passengers overcome their own challenges.',
		(SELECT id FROM users WHERE name = 'admin')
	),
	(
		'0e9f0972-8644-4fdd-8034-4e43dc01fc28',
		'Mermaidsea',
		'/mermaidsea.png',
		'"Mermaidsea" is an animated series set in a fantastical pirate world where we follow the adventures of a battle-hardened fish who is transported to a land inhabited by silly, singing hybrid fish-people creatures. Together with her new friends, she embarks on a journey of self-discovery and exploration as they face challenges and dangers that come their way.',
		(SELECT id FROM users WHERE name = 'admin')
	);

INSERT INTO episodes (show, index, name, description, url)
VALUES
	(
		'647f1187-28c6-4c5d-91d2-1ec895fcb8db',
		0,
		'Episode 1: Watch the Horizon',
		'When Skye and her pirate crew spot a mysterious ship on the horizon, they embark on a dangerous mission to investigate. But when they discover a sinister plot by a rival pirate crew, Skye must use her wits and bravery to outsmart them and protect her new family at the Seagull''s Nest.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=1'
	),
	(
		'647f1187-28c6-4c5d-91d2-1ec895fcb8db',
		1,
		'Episode 2: This Way to Adventure',
		'Skye and her crew get lost in a dense fog and end up stranded on an unfamiliar island, but they won''t let this setback stop them from seeking adventure and finding their way back to the Seagull''s Nest.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=2'
	),
	(
		'647f1187-28c6-4c5d-91d2-1ec895fcb8db',
		2,
		'Episode 3: Show Boating',
		'Edie receives a mysterious message in a bottle that leads the crew to a cursed island. Can Skye and her friends break the curse and save the island''s inhabitants before it''s too late?',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=3'
	),
	(
		'162f015d-b1ff-47b6-b26b-1c1471f9f7c6',
		0,
		'Episode 1: X Marks The Spot',
		'Deck and Rail stumble upon an old treasure map that leads them to a mysterious island, but they soon realize they''re not the only ones searching for the treasure.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=4'
	),
	(
		'162f015d-b1ff-47b6-b26b-1c1471f9f7c6',
		1,
		'Episode 2: Parrot Problems',
		'Bertie''s family curse becomes a major problem when the pirate crew is put in danger and only the brothers can help break the spell.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=5'
	),
	(
		'162f015d-b1ff-47b6-b26b-1c1471f9f7c6',
		2,
		'Episode 3: Kracken Attackin''',
		'The Kraken attacks the ship, leaving the brothers and crew stranded on a deserted island and fighting for survival.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'48affca1-68bf-46c7-916b-213824e7dd67',
		0,
		'Episode 1: Miraculous Beginnings',
		'Learn about the deep background and lore of all your favorite Brilliant Beetle characters! Here''s to hoping this episode airs first and not after the season finale!',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=4'
	),
	(
		'48affca1-68bf-46c7-916b-213824e7dd67',
		1,
		'Episode 57: Blunder Baron',
		'Foiled _once again_, Butterfly Baron has had enough! Again! This time his plans will succeed. This time...',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=5'
	),
	(
		'48affca1-68bf-46c7-916b-213824e7dd67',
		2,
		'Episode 203: The Forever Square',
		'Marie and Aaron still don''t know each other''s identities - or that they''re in love with each other! But things are afoot and maybe this time they''ll overcome their fears!',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'7f274e25-1a9f-456b-b859-5d77125139cd',
		0,
		'Episode 1: The Endless Deck',
		'Jack finds himself on a ship where the deck seems to stretch on forever.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'7f274e25-1a9f-456b-b859-5d77125139cd',
		1,
		'Episode 2: The Island Bargain',
		'Jack and Polly make a pitstop on a seemingly deserted island to restock their supplies. They discover the island is inhabited by a mischievous spirit who offers them a tempting bargain to get home. But is the price worth it?',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'7f274e25-1a9f-456b-b859-5d77125139cd',
		2,
		'Episode 8: The Perfectly Normal Fine Episode Where Nobody Dies',
		'Nothing ever goes wrong in Episode 8. Enjoy a fun episode!',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'0e9f0972-8644-4fdd-8034-4e43dc01fc28',
		0,
		'Episode 1: Hello Sparkling Currents',
		'Separated from her Fisher during battle, Fish wakes up in the colorful world filled with strange hybrid beasts. But where is her trusty friend?',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'0e9f0972-8644-4fdd-8034-4e43dc01fc28',
		1,
		'Episode 2: Lost in the Tides',
		'Fish and her crewmates get stranded on a deserted island after a violent storm. But when Fish''s impulsive nature leads her to venture further into the wilderness, she must face her fears before it''s too late.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	),
	(
		'0e9f0972-8644-4fdd-8034-4e43dc01fc28',
		2,
		'Episode 3: The Anchor',
		'Fish and her crewmates meet an ancient shaman who possesses a powerful item: an anchor that could reunite her with her Fisher.',
		'https://samplelib.com/lib/preview/mp4/sample-5s.mp4?id=6'
	);

INSERT INTO genres (id, name)
VALUES
	('aa1295ce-2090-4a2c-a6db-f2d68a3c772e', 'Action'),
	('e123df56-180a-477e-be58-f513736b2855', 'Adventure'),
	('cb233ddd-48da-4d2e-a34d-4b2a7bd856dd', 'Comedy'),
	('44149bed-c7b8-41c4-8b3e-ab36bcb68b63', 'Drama'),
	('04f3fdf0-b2af-43ec-b38a-5408f9ea02a9', 'Fantasy'),
	('437b4b09-16af-4d14-a45f-250fa11da903', 'Horror'),
	('c3c07ebb-efcf-47b9-b080-064e81d2a452', 'Mystery'),
	('0aa988c3-a9d8-42a1-887f-aeb86db0efd8', 'Romance'),
	('d32f8375-dbd8-45e9-8323-9d06f8f433b4', 'Sci-Fi'),
	('7147cfde-765d-4c47-91ac-a099889e3a61', 'Thriller');

INSERT INTO show_genres (show, genre)
VALUES
	('647f1187-28c6-4c5d-91d2-1ec895fcb8db', (SELECT id FROM genres WHERE name = 'Adventure')),
	('647f1187-28c6-4c5d-91d2-1ec895fcb8db', (SELECT id FROM genres WHERE name = 'Comedy')),
	('647f1187-28c6-4c5d-91d2-1ec895fcb8db', (SELECT id FROM genres WHERE name = 'Fantasy')),
	('162f015d-b1ff-47b6-b26b-1c1471f9f7c6', (SELECT id FROM genres WHERE name = 'Adventure')),
	('162f015d-b1ff-47b6-b26b-1c1471f9f7c6', (SELECT id FROM genres WHERE name = 'Comedy')),
	('162f015d-b1ff-47b6-b26b-1c1471f9f7c6', (SELECT id FROM genres WHERE name = 'Drama')),
	('48affca1-68bf-46c7-916b-213824e7dd67', (SELECT id FROM genres WHERE name = 'Action')),
	('48affca1-68bf-46c7-916b-213824e7dd67', (SELECT id FROM genres WHERE name = 'Comedy')),
	('48affca1-68bf-46c7-916b-213824e7dd67', (SELECT id FROM genres WHERE name = 'Romance')),
	('7f274e25-1a9f-456b-b859-5d77125139cd', (SELECT id FROM genres WHERE name = 'Adventure')),
	('7f274e25-1a9f-456b-b859-5d77125139cd', (SELECT id FROM genres WHERE name = 'Drama')),
	('7f274e25-1a9f-456b-b859-5d77125139cd', (SELECT id FROM genres WHERE name = 'Mystery')),
	('0e9f0972-8644-4fdd-8034-4e43dc01fc28', (SELECT id FROM genres WHERE name = 'Adventure')),
	('0e9f0972-8644-4fdd-8034-4e43dc01fc28', (SELECT id FROM genres WHERE name = 'Comedy'));
