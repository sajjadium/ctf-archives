FROM node:latest

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

RUN apt-get update && apt-get install -y libnss3-dev libgtk-3-dev libxss-dev libasound2 chromium xvfb
RUN groupadd -r bot && useradd bot -g bot && mkdir /home/bot && chown -R bot:bot /home/bot

COPY . /bot

RUN chown bot:bot /bot && mkdir /bot/dist && chown bot:bot /bot/dist

USER bot

ENTRYPOINT /bot/entrypoint.sh