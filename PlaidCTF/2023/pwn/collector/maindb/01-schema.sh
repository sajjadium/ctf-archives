#!/bin/sh

set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE hooks (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        kind TEXT NOT NULL,
        target TEXT NOT NULL,
        secret BIGINT NOT NULL
    );

    CREATE INDEX hooks_send_order ON hooks (kind, target, secret);
    CREATE INDEX hooks_kind ON hooks (kind);

    CREATE TABLE items (
        id BIGSERIAL PRIMARY KEY,
        kind TEXT NOT NULL,
        name TEXT NOT NULL
    );

    CREATE TABLE market (
        item_id BIGINT NOT NULL,
        bid_price BIGINT,
        bid_size BIGINT NOT NULL constraint bid_size_nonnegative check (bid_size >= 0),
        ask_price BIGINT,
        ask_size BIGINT NOT NULL constraint ask_size_nonnegative check (ask_size >= 0)
    );
    CREATE UNIQUE INDEX market_side ON market (item_id);

    CREATE TABLE initial_inventory (
        item_id BIGINT NOT NULL PRIMARY KEY,
        count BIGINT NOT NULL
    );

    CREATE TABLE inventory (
        user_id BIGINT NOT NULL,
        item_id BIGINT NOT NULL,
        count BIGINT NOT NULL constraint count_nonnegative check (count >= 0)
    );
    CREATE UNIQUE INDEX inventory_pkey ON inventory (user_id, item_id);
    CREATE INDEX inventory_user ON inventory (user_id);
    CREATE INDEX inventory_item ON inventory (item_id);

    CREATE TABLE users (
        id BIGSERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    CREATE UNIQUE INDEX users_username ON users (username);

    CREATE TABLE flag (
        flag TEXT
    );

    CREATE VIEW scoreboard AS
        WITH scores AS (
            SELECT user_id, COUNT(inventory.item_id) as unique, SUM(count * COALESCE(bid_price, 1)) as total FROM inventory
            LEFT JOIN market ON market.item_id = inventory.item_id
            WHERE count > 0
            GROUP BY user_id
        )
        SELECT scores.user_id, users.username, scores.unique, scores.total
        FROM scores
        INNER JOIN users
        ON users.id = scores.user_id
        ORDER BY scores.unique DESC, scores.total DESC, scores.user_id ASC;

    CREATE USER webhook WITH LOGIN ENCRYPTED PASSWORD '${DBUSER_WEBHOOK_PASSWORD}';
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO webhook;

    CREATE USER web WITH LOGIN ENCRYPTED PASSWORD '${DBUSER_WEB_PASSWORD}';
    GRANT SELECT, INSERT, UPDATE, DELETE
        ON ALL TABLES IN SCHEMA public
        TO web;
    GRANT USAGE, SELECT
        ON ALL SEQUENCES IN SCHEMA public
        TO web;
EOSQL