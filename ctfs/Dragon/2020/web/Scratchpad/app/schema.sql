create extension if not exists pgcrypto;
create table if not exists users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT UNIQUE NOT NULL, password TEXT NOT NULL);
create table if not exists notes (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, title TEXT NOT NULL, content TEXT NOT NULL, favourite BOOLEAN DEFAULT FALSE);
create table if not exists reports (id UUID UNIQUE NOT NULL REFERENCES notes(id) ON DELETE CASCADE);
create index if not exists index_notes_on_user_ids on notes(user_id) include (title, content);
