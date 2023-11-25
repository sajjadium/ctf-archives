FROM node:8-alpine
RUN apk add --no-cache git
RUN git clone https://gerrit.wikimedia.org/r/mediawiki/services/graphoid
WORKDIR /graphoid
RUN git checkout HEAD^
RUN npm i
EXPOSE 6927
CMD [ "npm", "start" ] 