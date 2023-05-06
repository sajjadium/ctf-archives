FROM node:14

RUN mkdir -p /usr/src/app

RUN apt-get update -y && apt-get install python -y && apt-get install python-pip -y

WORKDIR /usr/src/app

COPY ./container/images-services/src/ .

RUN npm install
RUN pip install requests

COPY ./container/images-services/flag.txt /usr/src/app/fl4gg_tetCTF

EXPOSE 3000

CMD [ "node", "index.js" ]