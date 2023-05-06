FROM openjdk:15-jdk-alpine

RUN apk add --no-cache bash

WORKDIR /home/app

COPY requester.jar ./requester.jar
COPY wait-for-it.sh ./wait-for-it.sh

RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "couchdb:5984", "--", "java","-jar","/home/app/requester.jar"]