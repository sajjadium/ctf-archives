#!/bin/sh
cd /files
# setup www
rm /var/www/html/*
mv html/* /var/www/html
chown -R root:root /var/www/html
chmod 755 -R /var/www/html
chmod 666 /var/www/html/cgidata
chmod 777 /var/www/html/data

# setup flag
mv flag getflag /
chown root:root /flag /getflag
chmod 400 /flag
chmod 4555 /getflag

# setup nginx
mv default /etc/nginx/sites-enabled/
mv nginx.conf /etc/nginx
chown root:root /etc/nginx/sites-enabled/default /etc/nginx/nginx.conf
chmod 755 /etc/nginx/sites-enabled/default /etc/nginx/nginx.conf

# setup cgi
mv cgi /opt
chown root:root /opt/cgi
chmod 755 /opt/cgi

mv start.sh /
chown root:root /start.sh
chmod 755 /start.sh

rm setup.sh
rmdir html
