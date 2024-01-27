FROM node:21.5.0-bookworm

USER node
WORKDIR /home/node

COPY ./package.json .
RUN npm install

COPY ./setup.sh .
COPY ./circuit.circom .
RUN bash setup.sh

COPY . .
CMD node index.js