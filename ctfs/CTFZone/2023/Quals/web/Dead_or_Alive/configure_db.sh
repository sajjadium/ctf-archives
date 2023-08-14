#!/bin/bash
while true; do
    out=$(cypher-shell -u neo4j -p rootroot <<< "CREATE USER moderator SET PASSWORD 'moderator' CHANGE NOT REQUIRED;
    CREATE ROLE moderator;
    GRANT CREATE ON GRAPH hospitalgraph NODE Patient TO moderator;
    GRANT SET PROPERTY {ssn,name,yearOfBirth,since,weight} ON GRAPH hospitalgraph NODES Patient TO moderator;
    GRANT CREATE ON GRAPH hospitalgraph RELATIONSHIP HAS TO moderator;
    GRANT ROLE reader TO moderator;
    GRANT ROLE moderator TO moderator;" 2>&1)
    [ "$out" != "Connection refused" ] && break
done