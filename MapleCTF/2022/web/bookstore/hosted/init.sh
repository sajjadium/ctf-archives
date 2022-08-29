#!/bin/bash

mysqld --user=root &
sleep 5
mysql -u root < /init.sql
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Rooted123!';"
mysql -e "FLUSH PRIVILEGES"

npm start
