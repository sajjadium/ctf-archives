#!/bin/bash

flag="TetCTF{......}"
echo $flag > simpleweb/flag
mkdir -p simpleweb/log simpleweb/session simpleweb/uploads
chown -R 0:1000 simpleweb/
chmod -R 744 simpleweb/users
chmod -R 400 simpleweb/flag
chmod u+s simpleweb/readflag
chmod -R 777 simpleweb/session simpleweb/uploads
chmod -R 755 simpleweb/web simpleweb/www
chmod 755 simpleweb/webcgi.cgi
docker-compose up -d
