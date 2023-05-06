FROM node:18-alpine3.14

ENV flag "we{test}"

COPY certs app/certs

WORKDIR /app
COPY package.json /app
RUN npm i

COPY flag_server.js /app

COPY index_server.js /app

COPY proxy.js /app

COPY start.sh /app
RUN chmod +x start.sh

CMD ./start.sh