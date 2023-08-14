FROM node:20

RUN apt update
RUN apt -y install libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev libasound2 sudo

RUN useradd -rm -d /home/ubuntu -s /bin/bash -u 1001 ubuntu
RUN chown ubuntu /home/ubuntu

RUN echo "ctfzone{REDACTED}" > /root/flag.txt
RUN echo "ubuntu ALL = (root) NOPASSWD: /bin/cat /root/flag.txt" >> /etc/sudoers

USER ubuntu
WORKDIR /home/ubuntu
COPY package.json ./
RUN npm install
RUN mkdir app
COPY app/ app/
COPY worker.js ./worker.js
COPY app.js ./app.js

EXPOSE 3000
CMD ["bash","-c","node --inspect app.js  1>app-logs.out 2>app-logs.err"]