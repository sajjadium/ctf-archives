nohup node /bot/bot.js & > /app/nohup.out
nohup node app & > /app/nohup.out

redis-server /etc/redis/redis.conf

tail -f /app/nohup.out
