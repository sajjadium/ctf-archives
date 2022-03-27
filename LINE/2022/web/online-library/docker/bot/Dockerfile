FROM node:latest

RUN apt-get update && apt-get install -y libnss3-dev libgtk-3-dev libxss-dev libasound2 
RUN groupadd -r bot && useradd bot -g bot && mkdir /home/bot && chown -R bot:bot /home/bot

USER bot

ENTRYPOINT /bot/entrypoint.sh