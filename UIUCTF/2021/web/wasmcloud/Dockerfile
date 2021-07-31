FROM node:14-alpine as chroot

COPY flag.txt sandbox.js /

FROM disconnect3d/nsjail

RUN apt-get update && apt-get install -y curl sudo
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
RUN sudo apt-get install -y nodejs

# chromium deps for admin bot
RUN sudo apt-get install -y ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 \
    libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
    libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils

COPY --from=chroot / /chroot

RUN mkdir /app && mkdir /files
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY index.js bot.js ./
COPY static/ ./static

EXPOSE 1337/tcp

ENV HCAPTCHA_BYPASS=redacted
ENV HCAPTCHA_SECRET=redacted
ENV HCAPTCHA_ENABLE=false

CMD node index.js
