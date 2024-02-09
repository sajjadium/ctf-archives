#!/bin/sh
service mariadb start && service apache2 start
USER="ctf"
PASSWORD="ctf123"

echo "Creating new user ${MYSQL_USER} ..."
mysql -uroot -e "CREATE USER '${USER}'@'localhost' IDENTIFIED BY '${PASSWORD}';"
echo "Granting privileges..."
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '${USER}'@'localhost';"
mysql -uroot -e "GRANT FILE ON *.* TO '${USER}'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"
echo "Done! Permissions granted"
mysql -u$USER -p$PASSWORD -e "CREATE database CTF;"
mysql -u$USER -p$PASSWORD CTF  < /init.db
echo "All done."
sleep 5
python3 -u /app.py