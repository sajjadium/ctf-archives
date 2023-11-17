mkdir -p /tmp/smarty/templates /tmp/smarty/templates_c /tmp/smarty/cache /tmp/smarty/configs
chmod 777 /tmp/smarty/templates /tmp/smarty/templates_c /tmp/smarty/cache
mv /var/www/html/index.tpl /tmp/smarty/templates/
apache2-foreground