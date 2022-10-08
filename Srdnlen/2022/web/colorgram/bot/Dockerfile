FROM node:17

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app
COPY package*.json ./

RUN npm install

RUN groupadd appgroup && useradd -g appgroup appuser 

COPY *.js ./

EXPOSE 8888

USER appuser

CMD ["node", "server.js"]
