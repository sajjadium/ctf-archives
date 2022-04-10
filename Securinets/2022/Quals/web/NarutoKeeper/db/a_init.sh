#!/bin/bash
USER="securinets"
PASSWORD="REDACTED"

echo "Creating new user ${MYSQL_USER} ..."
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '${USER}'@'%' IDENTIFIED BY '${PASSWORD}';"
echo "Granting privileges..."
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON *.* TO '${USER}'@'%';"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"
echo "All done."
