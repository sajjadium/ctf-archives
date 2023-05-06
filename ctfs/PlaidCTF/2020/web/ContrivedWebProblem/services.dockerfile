FROM node:12

WORKDIR /service/

RUN yarn global add typescript

ADD package.json ./
RUN yarn install

ADD . ./
RUN yarn run build

ARG FLAG

RUN echo $FLAG > /flag.txt

CMD ["node", "index.js"]