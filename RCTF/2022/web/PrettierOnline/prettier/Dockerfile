FROM node:19.2.0-bullseye-slim
COPY package.json package-lock.json /app/
RUN cd /app && \
    npm config set registry https://registry.npmmirror.com && \
    npm install
COPY . /app/
WORKDIR /app
COPY flag /flag
COPY readflag /readflag
RUN chmod 0600 /flag && \
    chmod u+s /readflag
USER nobody
CMD [ "node", "index.js" ]
