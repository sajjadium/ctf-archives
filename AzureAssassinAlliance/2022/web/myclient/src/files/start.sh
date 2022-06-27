#!/bin/bash
mkdir /tmp/e10adc3949ba59abbe56e057f20f883e
chmod 1777 /tmp/e10adc3949ba59abbe56e057f20f883e
service mysql stop
usermod -d /var/lib/mysql/ mysql
service mysql start

watch -n 300 'rm -rf /tmp/e10adc3949ba59abbe56e057f20f883e/*' &>/dev/null &
mysql -u root -e "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASS';";
mysql -u root -e "GRANT SELECT on mysql.* to '$MYSQL_USER'@'%';FLUSH PRIVILEGES;";
mysql -u root -e "GRANT FILE on *.* to '$MYSQL_USER'@'%';FLUSH PRIVILEGES;";
service apache2 start
tail -f /dev/null