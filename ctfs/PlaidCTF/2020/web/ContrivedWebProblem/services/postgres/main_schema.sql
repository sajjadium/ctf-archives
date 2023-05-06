CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE user_auth (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name text NOT NULL,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    profile text
);

CREATE TABLE user_token (
    user_id uuid REFERENCES user_auth (id),
    token uuid DEFAULT uuid_generate_v4(),
    PRIMARY KEY (user_id, token)
);

CREATE TABLE posts (
    user_id uuid REFERENCES user_auth (id),
    message text NOT NULL,
    message_time timestamp DEFAULT now()
);
