FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive 
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apt-get update && apt-get install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

RUN apt-get update && apt-get install -y --no-install-recommends \
  libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 \
  libasound2 libxshmfence1 libx11-xcb1 && rm -rf /var/lib/apt/lists/*

RUN groupadd -r user && useradd --no-log-init -m -r -g user user

RUN mkdir /code
RUN chown user /code

USER user

WORKDIR /code

RUN curl -fsS https://files.be.ax/public/chromium-91.0.4472.148-2021-07-06.tar.bz2 | tar xj

COPY . /code

RUN npm install

CMD ["node", "index.js"]