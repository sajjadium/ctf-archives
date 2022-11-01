# YummyGIFs

Host your yummy GIFs of delicious food with us and share them around the internet!

Our service is still in beta. To save disk space costs (and prevent DOS) our service will delete your GIFs after 15 minutes. (It's really just DOS prevention)

`adminbot/*` is just your average bot and not part of the challenge.

## Setup locally without bot

Just remove the `bot` service from `docker-compose.yml`

## Setup locally with bot

1. `docker build -t bot-worker adminbot/bot-worker/`
2. Disable recaptcha in `adminbot/bot-master/bot-master-config.json`
3. Change link pattern in `adminbot/bot-master/bot-master-config.json`
4. In `.env`, change `LOGIN_URL` to `http://web/login.php`
5. Report links to the bot as `http://web/...`, the internal Docker host