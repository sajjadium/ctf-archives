nohup php-fpm > /dev/null 2>&1 &
nginx -g 'daemon off;'

while true
do
  sleep 1
done
