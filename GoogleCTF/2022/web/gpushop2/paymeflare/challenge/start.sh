#!/bin/bash

for i in {1..100}; do echo "waiting for mysql..."; sleep 5; if mysqladmin ping -h "$DB_HOST" --silent; then break; fi; done;
if [ $i -eq 100 ]; then
    echo "waiting for mysql failed"
    exit 1
fi

cd /lv
php artisan config:cache
yes | php artisan migrate:fresh || exit 1
yes | php artisan db:seed --class=ProdDatabaseSeeder || exit 1

php-fpm7.4

while [ 1 ]; do
    rm -f /var/run/socket/nginx.socket
    /usr/sbin/nginx -g "daemon off;"
done
