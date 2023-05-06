#!/bin/bash

cd /docker-entrypoint-initdb.d

if [ -f flag.txt ]; then
  read flag < flag.txt
  mysql -u root -p"$MYSQL_ROOT_PASSWORD" analects -e "UPDATE flag SET flag='$flag';"
fi
