#!/bin/sh

# wait a bit.
sleep 2

# init WP installation + loop until db is up
until sudo -E -u www-data php /tmp/wp-cli-2.5.0.phar --path=/var/www/html/ \
     core install \
     --url=localhost:8080 \
     --title=ALLES!-CTF-Shop \
     --admin_user=ADMINUSER \
     --admin_password=ADMINPW \
     --admin_email=noo@mail.invalid
do
  echo "Waiting for DB to be up..."
  sleep 2
done


# install woocommerce plugin
sudo -E -u www-data php /tmp/wp-cli-2.5.0.phar --path=/var/www/html/ \
    plugin install woocommerce --activate


# create new role. Can create products, but not manage the whole shop. Just to reduce accidental surface area.
sudo -E -u www-data php /tmp/wp-cli-2.5.0.phar --path=/var/www/html/ \
    role create productmanager Productmanager --clone=author
sudo -E -u www-data php /tmp/wp-cli-2.5.0.phar --path=/var/www/html/ \
    cap add productmanager \
    edit_product \
    read_product \
    delete_product \
    edit_products \
    publish_products \
    delete_products \
    delete_published_products \
    edit_published_products


# create shop-manager user
sudo -E -u www-data php /tmp/wp-cli-2.5.0.phar --path=/var/www/html/ \
    user create \
    SHOPUSER \
    shop@mail.invalid \
    --user_pass=SHOPPW \
    --role=productmanager

# publish flag
ln -s /flag.php /var/www/html/flag.php

# configure wordpress to use https (remote only)
#sed -i "s/\/\* That's all, stop editing! Happy publishing. \*\//\$_SERVER['HTTPS'] = 'on';/" /var/www/html/wp-config.php

# start apache (original Dockerfile CMD)
exec apache2-foreground "$@"