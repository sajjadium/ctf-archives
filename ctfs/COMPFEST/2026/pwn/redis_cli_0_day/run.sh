#!/bin/sh

HOST=127.0.0.1
PORT=6379

printf "Enter host address: "
read HOST
printf "Enter port number: "
read PORT

./redis-cli --user compfest --pass redis_cli_0_day_wow! --cluster info $HOST $PORT < /dev/null > /dev/null 2>&1
