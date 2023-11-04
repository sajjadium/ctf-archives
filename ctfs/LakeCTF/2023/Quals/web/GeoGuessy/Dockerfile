from ubuntu:latest

RUN apt update -y && apt install -y npm curl wget
RUN  npm cache clean -f
RUN  npm install -g n
RUN  n stable
RUN mkdir /app
RUN apt install xvfb -y

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libx11-xcb1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

COPY ./GeoGuessy/ /app
WORKDIR /app/
RUN npm install

CMD rm -rf /tmp/.X* && sleep 1 && DISPLAY=:0 Xvfb :0 -screen 0 1024x768x24 & DISPLAY=:0 NODE_ENV=production node /app/app.js
