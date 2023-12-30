FROM node@sha256:73a9c498369c6e6f864359979c8f4895f28323c07411605e6c870d696a0143fa

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y 
RUN apt-get install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release xdg-utils wget

WORKDIR /tmp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -q
RUN apt install -y libu2f-udev libvulkan1 
RUN dpkg -i ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

WORKDIR /app
COPY ./stuff/ /app/
RUN PUPPETEER_SKIP_DOWNLOAD=1 npm ci
RUN chmod +x /app/index.js
RUN useradd -m www
RUN chmod 777 /home/www/ -R
USER www
CMD NODE_ENV=production /app/index.js
