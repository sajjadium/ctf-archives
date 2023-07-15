FROM mcr.microsoft.com/playwright:v1.34.0-jammy

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install
RUN npx playwright install

RUN apt update -y && apt install -y xvfb

RUN groupadd -r bot && useradd -r -g bot -G audio,video bot \
    && mkdir -p /home/bot/Downloads \
    && chown -R bot:bot /home/bot \
    && chown -R bot:bot /app/node_modules

USER bot
ADD index.js /app/
ADD run.sh /app/

CMD [ "/bin/bash", "/app/run.sh" ]