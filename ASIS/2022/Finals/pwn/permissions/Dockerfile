FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y curl xvfb procps unzip ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release xdg-utils wget
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update -y
RUN apt-get install -y nodejs
RUN mkdir /chrome/
WORKDIR /chrome/
RUN wget 'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F961656%2Fchrome-linux.zip?generation=1642723767466615&alt=media' -O ./chrome.zip
# COPY ./chrome.zip ./chrome.zip
# 3467146abacd8fae1f2af72f5b51635b1e4e050e67a3ab4589a8cabf6937b8b5 chrome.zip
RUN unzip -q ./chrome.zip
RUN ln -s /chrome/chrome-linux/chrome /usr/bin/google-chrome-stable

WORKDIR /app
COPY ./stuff /app
COPY ./flag.txt /flag.txt
COPY ./stuff/tini /bin/tini
RUN chmod +x /app/index.js
RUN PUPPETEER_SKIP_DOWNLOAD=1 npm install
RUN useradd -m www
RUN chown www /app -R
RUN chmod +x /bin/tini

USER www

ENTRYPOINT ["/bin/tini","--"]