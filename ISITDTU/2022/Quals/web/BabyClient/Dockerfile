FROM node:current-buster-slim

# Install packages
RUN apt-get update \
    && apt-get install -y wget supervisor gnupg nginx \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libx11-xcb1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
    
# Setup app
RUN mkdir -p /app

# Add application
WORKDIR /app
COPY challenge .

# Set ENV variables
ENV PORT 9000

# Point Puppeteer automated scanner to use downloaded chrome
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

# Install dependencies
RUN yarn

# Setup superivsord
COPY config/supervisord.conf /etc/supervisord.conf

EXPOSE 9000
# Start supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]