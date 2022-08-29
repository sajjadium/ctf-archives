#!/bin/sh

cd /usr/src/app/ftp
node ftpserver.js &

cd ../http
node app.js &

redis-server