FROM node:18-bullseye-slim

RUN apt-get update && \
apt-get install -y dumb-init gcc && \
rm -rf /var/lib/apt/lists/*

RUN addgroup ejs && \
adduser --disabled-password --gecos "" --ingroup ejs ejs

WORKDIR /home/ejs/app
RUN chown -R ejs:ejs .

COPY views ./views
COPY main.js package.json ./

RUN npm install

COPY flag.txt /root/flag.txt

COPY readflag.c /readflag.c
RUN gcc -o /readflag /readflag.c && rm /readflag.c
RUN chmod +rxs /readflag

USER ejs

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]
