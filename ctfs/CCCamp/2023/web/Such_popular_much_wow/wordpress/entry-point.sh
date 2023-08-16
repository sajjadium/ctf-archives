#!/bin/bash
echo "Going to sleep for 20 seconds to wait for mysqld to initialize"

sleep 20

cd /var/www/html/

while ! mysqladmin ping -h"$WORDPRESS_DB_HOST" -p$WORDPRESS_DB_PASSWORD -u$WORDPRESS_DB_USER  --silent; do
    echo "mysql not up yet. Waiting..."
    sleep 1
done

php wp-cli.phar core download --version=5.9.3 
php wp-cli.phar config create --dbname=$WORDPRESS_DB_NAME --dbuser=$WORDPRESS_DB_USER --dbpass=$WORDPRESS_DB_PASSWORD --dbhost=$WORDPRESS_DB_HOST --skip-check

# On remote:
#URL=https://$SESSIONID-1024-diff-the-patch.$CHALLENGE_DOMAIN:$WORDPRESS_PORT

# On local (docker-compose)
URL=http://localhost:1024

php wp-cli.phar core install --allow-root --url=$URL --title=Diff-the-patch --admin_user=admin --admin_password=$ADMINPW --admin_email=info@example.com


php wp-cli.phar --allow-root user create bob-the-author bob@cscg.live --role=author --user_pass=s3cur3PW
php wp-cli.phar --allow-root plugin install https://github.com/cabrerahector/wordpress-popular-posts/archive/refs/tags/4.2.2.zip --activate

sed -i '2i define( "FORCE_SSL_ADMIN", false );' /var/www/html/wp-config.php

# On remote
#sed -i '2i $_SERVER["HTTPS"]="on";' /var/www/html/wp-config.php
# On local
sed -i '2i $_SERVER["HTTPS"]="off";' /var/www/html/wp-config.php

apache2-foreground &

python3 /usr/bin/firefox-script.py $URL $ADMINPW