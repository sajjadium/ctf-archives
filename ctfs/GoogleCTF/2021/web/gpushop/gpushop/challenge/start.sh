#!/bin/bash

for i in {1..100}; do echo "waiting for mysql..."; sleep 5; if mysqladmin ping -h "$DB_HOST" --silent; then break; fi; done;
if [ $i -eq 100 ]; then
    echo "waiting for mysql failed"
    exit 1
fi

cd /lv
php artisan config:cache
yes | php artisan migrate:fresh
yes | php artisan db:seed --class=ProdDatabaseSeeder

php-fpm7.4
/usr/sbin/nginx -g "daemon off;"
