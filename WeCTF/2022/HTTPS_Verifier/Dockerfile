FROM node:18

WORKDIR /app

RUN wget https://artifacts.elastic.co/downloads/logstash/logstash-7.15.0-linux-x86_64.tar.gz

RUN tar xzvf logstash-7.15.0-linux-x86_64.tar.gz && mv logstash-7.15.0 logstash

COPY log.conf .
COPY package.json .
RUN npm i
COPY server.js .
COPY views/ ./views

COPY start.sh .
RUN chmod +x start.sh

RUN echo "we{test}"

CMD ./start.sh
