#!/bin/bash

service mysql start
service apache2 start

# admin pw = U6jJxLzEreSV1CjShdM4, different on real server
mysql -e "UPDATE zm.Config SET Value = '8kjQJQg7GB4vfu8yFE7WjzWfhHYMXYC3' WHERE Config.Name = 'ZM_AUTH_HASH_SECRET';"
mysql -e "UPDATE zm.Config SET Value = '1' WHERE Config.Name = 'ZM_OPT_USE_AUTH';"
mysql -e "UPDATE zm.Users SET Password = '\$2y\$10\$/S1zBzOnz8oUDQFlQvUqteZbs8EDErR8Y3mWZFeM03ZZUCeWVQdJm' WHERE Users.Username = 'admin';"

chmod 740 /etc/zm/zm.conf
chown root:www-data /etc/zm/zm.conf
chown -R www-data:www-data /usr/share/zoneminder/

a2enmod cgi
a2enmod rewrite
a2enconf zoneminder

service apache2 reload
service zoneminder start
