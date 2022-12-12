FROM node:19.2.0-bullseye-slim
COPY package.json package-lock.json /app/
RUN cd /app && \
    npm config set registry https://registry.npmmirror.com && \
    npm install
COPY . /app/
WORKDIR /app
CMD [ "node", "app.js" ]
