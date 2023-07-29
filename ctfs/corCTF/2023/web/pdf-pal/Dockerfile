FROM node:current-buster-slim

# Install packages
RUN apt-get update \
    && apt-get install -y python3 python3-pip wget supervisor gnupg nginx \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libx11-xcb1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
RUN mkdir -p /pdf-gen

COPY flag.txt /flag.txt

# python app setup
WORKDIR /app
COPY app/requirements.txt . 

RUN python3 -m pip install -r requirements.txt

COPY app .

# pdf-gen setup
WORKDIR /pdf-gen
COPY pdf-gen/package.json pdf-gen/package-lock.json ./

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

RUN npm ci

COPY pdf-gen .

# supervisord setup
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]