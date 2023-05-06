#!/bin/bash

password="$(head -100 /dev/urandom | sha256sum | cut -f' ' -f1)"

echo 'Require ip 127.0.0.1' >> /var/www/html/.htaccess

service apache2 start

while :; do
  if curl 'http://localhost/install/install_db.php' -X POST -H 'Content-Type: application/x-www-form-urlencoded' --data-raw "mysql_host=db&mysql_user=gnuboard&mysql_pass=gnuboard&mysql_db=gnuboard&table_prefix=g5_&g5_shop_prefix=g5_shop_&g5_shop_install=1&ajax_token=1fea273eb9d28138f1292ec09ab007fd&admin_id=admin&admin_pass=$password&admin_name=%EC%B5%9C%EA%B3%A0%EA%B4%80%EB%A6%AC%EC%9E%90&admin_email=admin%40domain.com" 2>/dev/null | grep -q 'dbconfig'; then
    break
  fi
done

sed -i '$ d' /var/www/html/.htaccess

sleep inf
