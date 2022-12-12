FROM node

RUN apt-get update \
    && apt-get install -y wget supervisor gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
    
RUN mkdir -p /app

WORKDIR /app
COPY challenge .

RUN yarn
RUN npm i ejs @fastify/view @fastify/formbody @fastify/static dompurify@2.0.16 jsdom

ENV FLAG="hctf{wish_this_was_the_flag}"

COPY config/supervisord.conf /etc/supervisord.conf

EXPOSE 1337

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
