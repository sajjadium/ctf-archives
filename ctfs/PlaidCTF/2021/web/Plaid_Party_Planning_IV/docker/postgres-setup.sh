#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER pppiv;

    CREATE TABLE flag ( flag varchar(255) );

    CREATE TABLE submissions (
        id serial primary key,
        "time" timestamp with time zone DEFAULT clock_timestamp(),
        team varchar(255),
        score double precision,
        assignment text,
        flag_worthy boolean
    );

    CREATE VIEW scoreboard AS
    SELECT min(time) AS time, team, score
    FROM submissions
    INNER JOIN ( 
        SELECT team AS team_max, max(score) AS score_max
        FROM submissions 
        WHERE (flag_worthy = false)
        GROUP BY team
    ) AS best 
    ON (best.team_max = submissions.team) AND (best.score_max = submissions.score)
    GROUP BY team, score
    ORDER BY score DESC, time ASC;

    GRANT SELECT ON TABLE flag TO pppiv;
    GRANT INSERT ON TABLE submissions TO pppiv;
    GRANT SELECT ON TABLE scoreboard TO pppiv;
    GRANT USAGE ON SEQUENCE submissions_id_seq TO pppiv;
EOSQL

flag="$(cat /run/secrets/flag)"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    -c "INSERT INTO flag (flag) VALUES ('$flag')"

sed -i '
/host all all all/c\
host all pppiv samenet trust
' $PGDATA/pg_hba.conf