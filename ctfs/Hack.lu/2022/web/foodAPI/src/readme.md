# FoodAPI


## Just run the Challenge Website
```
cd browser-bot/challenge-image/foodAPI
deno run --allow-write --allow-read --allow-env --allow-net --import-map ./import_map.json server.js
```
Note: import-map is just here to make the challenge work, as deno std was updated yesterday and is now broken XDD

##  Run the whole Setup
```
cd browser-bot/challenge-image
docker build -t challenge_image .
cd ..
docker-compose up
```


Note: bot-master is not supposed to be vuln it is just used to queue the requests to the challenge-image
Note: only .env-challenge and bot-master-config.json have been changed to hide secrets
