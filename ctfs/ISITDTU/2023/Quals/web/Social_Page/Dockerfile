FROM node:14

RUN mkdir -p /home/node/app
WORKDIR /home/node/app
COPY ./src/ .
RUN npm install
RUN npm install lodash@4.15.0
ENV JWT_SECRET_KEY="redacted"
RUN echo "ISITDTU{redacted}" > flag
RUN chmod -R 777 /home/node/app
USER node
EXPOSE 3000

CMD [ "node", "index.js" ]