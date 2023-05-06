#!/bin/bash

#server
cat init.sql | sqlite3 simple_blogger.db
mv simple_blogger.db ./server/

#agent
export ADMIN_USER='admin'
export ADMIN_PASS=$(sqlite3 ./server/simple_blogger.db "SELECT pass FROM account WHERE user = 'admin'")

docker-compose -p linectf_simple_blogger up --force-recreate --build -d
docker image prune -f