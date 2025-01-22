#!/bin/bash

service mariadb start

sleep 5

mysqladmin -u root password "${MYSQL_PASSWORD}"

mysql -u root -p"${MYSQL_PASSWORD}" <<EOF
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

DB_EXISTS=$(mysql -u root -p"${MYSQL_PASSWORD}" -e "SHOW DATABASES LIKE '${MYSQL_DB}';" | grep "${MYSQL_DB}" > /dev/null; echo "$?")

if [ "$DB_EXISTS" -ne 0 ]; then
    echo "Initializing MariaDB database..."
    envsubst < /root/init.sql | mysql -u root -p"${MYSQL_PASSWORD}"
else
    echo "Database ${MYSQL_DB} already exists. Skipping initialization."
fi

su flask -c "python /app/app.py"