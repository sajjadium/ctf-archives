#!/bin/sh

set -e

chmod 600 /entrypoint.sh

echo "Starting MongoDB"
su -c "mkdir /tmp/mongodb && mongod --noauth --dbpath /tmp/mongodb/" mongo &

echo "Waiting for mongodb..."
mongo --nodb /wait_for_mongo.js

echo "MongoDB started, adding users"
mongo area51 --eval "var FLAG = '$FLAG'" /init_users.js

echo "Starting web server"
su -c "npm start" area51