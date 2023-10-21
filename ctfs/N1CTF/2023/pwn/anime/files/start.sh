#!/bin/sh
mkdir /run/cgi
chown www-data:www-data /run/cgi
rm /run/cgi/lua.sock
chroot --userspec=www-data:www-data / fcgiwrap -f -s unix:/run/cgi/lua.sock &
service nginx start
tail -f -
