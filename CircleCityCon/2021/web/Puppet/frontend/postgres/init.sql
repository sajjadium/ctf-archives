CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE challenge (
	uid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	prefix text NOT NULL,
	difficulty int NOT NULL,
	deadline timestamp NOT NULL
);

CREATE TABLE job (
	uid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	job json NOT NULL,
	socket_id text NOT NULL,
	created_at timestamp NOT NULL DEFAULT NOW(),
	completed_at timestamp
);
