FROM node:12.16.3-stretch

COPY . /code
WORKDIR /code

RUN yarn && yarn run build
EXPOSE 5000

CMD [ "yarn", "start" ]
