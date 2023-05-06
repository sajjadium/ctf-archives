FROM node as bot_env
COPY ./bot/bot.js /bot/bot.js
WORKDIR /bot
RUN npm i puppeteer
RUN npm i redis

FROM node

ENV REDIS_PASSWORD=redis_password \ 
    ADMIN_PASSWORD=fake_password \
    FLAG=rwctf{test_flag}

# Recaptcha keys
ENV RECAPTCHA_SITE_KEY=SITE_KEY \
     RECAPTCHA_SECRET_KEY=SECRET_KEY

RUN apt update && \
    apt install libgtk-3-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 redis-server -y && \
    echo "requirepass ${REDIS_PASSWORD}" >> /etc/redis/redis.conf 

COPY ./code /app
COPY ./setup.sh /app/setup.sh
COPY --from=bot_env /bot /bot
COPY --from=bot_env /root/.cache /root/.cache

WORKDIR /app

RUN npm i

EXPOSE 12345

CMD ["sh","-c","chmod +x ./setup.sh && ./setup.sh"]
