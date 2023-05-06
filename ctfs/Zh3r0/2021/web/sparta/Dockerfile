FROM node
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app
COPY flag.txt /
COPY files .
USER node
RUN npm install
COPY --chown=node:node files .
EXPOSE 7777
CMD [ "node", "server.js" ]
