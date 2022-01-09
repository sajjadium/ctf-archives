FROM node:14

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./animals/src/ .

RUN npm install

RUN echo "TetCTF{nodejs_1s_as0m3_pol}" > /flag
RUN chmod 0400 /flag
COPY ./animals/readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod 4755 /readflag

EXPOSE 3000

CMD [ "node", "index.js" ]