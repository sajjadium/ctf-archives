FROM debian:buster-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs ffmpeg -y

WORKDIR /usr/src/app
COPY package.json .

RUN npm install

COPY . .

RUN chmod -R 644 /usr/src/app

# save disk space :^)
RUN dpkg --remove --force-depends python2.7-minimal python3-minimal python3.7-minimal 
RUN rm /usr/bin/perl
RUN apt-get clean && apt-get autoclean && rm -rf /var/lib/apt/lists/*

CMD ["node", "index.js"]