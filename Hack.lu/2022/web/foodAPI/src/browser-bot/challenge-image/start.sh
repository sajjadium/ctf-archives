#!/bin/bash


# start the challenge
cd /app/foodAPI
deno run --allow-write --allow-read --allow-env --allow-net --import-map import_map.json server.js &

# wait until deno is ready
timeout 5 sh -c 'until nc -z $0 $1; do sleep 1; done' 127.0.0.1 443

# start the browser bot
cd /app
# node bot.js <url> <timeout>
node bot.js $1 $2