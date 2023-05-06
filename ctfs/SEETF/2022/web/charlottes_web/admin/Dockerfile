FROM node:16-buster-slim

RUN apt-get update && \
apt-get install -y chromium dumb-init unzip xvfb && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production

RUN addgroup inmate && \
adduser --disabled-password --gecos "" --ingroup inmate inmate

WORKDIR /home/inmate/app
COPY . ./

RUN chown -R inmate:inmate .
USER inmate
RUN npm install && \
mkdir -p /home/inmate/Downloads

RUN unzip vuln.zip
RUN chmod -R +rx ./vuln
RUN chmod +x ./start.sh

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./start.sh"]
