FROM node:16
  
COPY ./source /app
WORKDIR /app
RUN npm config set loglevel=http
RUN npm config set registry https://registry.npm.taobao.org

RUN npm install && npm install pm2 -g
RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && rm -Rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

ENV FLAG="ACTF{********}" LISTEN="0.0.0.0"

CMD ["/bin/bash", "./start.sh"]