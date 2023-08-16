#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS game;
    
    CREATE OR REPLACE TABLE game.users 
    (
        uuid UUID,
        username String,
        x Float64,
        y Float64,
        rotation Float64,
        money UInt64,
        inventory String,
        health UInt64,
        last_death Float64,
        last_ping Float64
    )
    ENGINE = ReplacingMergeTree ORDER BY (username);

    CREATE OR REPLACE TABLE game.users_history
    (
        date DateTime,
        uuid UUID,
        username String,
        x Float64,
        y Float64,
        rotation Float64,
        money UInt64,
        inventory String,
        health UInt64,
        last_death Float64,
        last_ping Float64
    )
    ENGINE = MergeTree ORDER BY (date, username);

    CREATE MATERIALIZED VIEW IF NOT EXISTS game.users_history_mv TO game.users_history AS
    SELECT now(), uuid, username, x, y, rotation, money, inventory, health, last_death, last_ping FROM game.users;

    CREATE OR REPLACE TABLE game.scoreboard 
    (
        username String,
        start Float64,
        end Float64
    )
    ENGINE = ReplacingMergeTree ORDER BY (username);

    CREATE OR REPLACE TABLE game.scoreboard_history
    (
        date DateTime,
        username String,
        start Float64,
        end Float64
    )
    ENGINE = MergeTree ORDER BY (date, username);

    CREATE MATERIALIZED VIEW IF NOT EXISTS game.scoreboard_history_mv TO game.scoreboard_history AS
    SELECT now(), username, start, end FROM game.scoreboard;
EOSQL
