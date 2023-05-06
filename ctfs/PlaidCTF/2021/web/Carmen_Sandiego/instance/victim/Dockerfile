FROM ubuntu:18.04

RUN apt update && apt install -y xvfb curl wget software-properties-common unzip
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs chromium-browser
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install -y yarn

RUN useradd bot
RUN mkdir -p /home/bot
WORKDIR /home/bot
COPY package.json .
RUN yarn install
COPY . .
RUN yarn build
RUN chown bot:bot /home/bot
USER bot
CMD yarn start
