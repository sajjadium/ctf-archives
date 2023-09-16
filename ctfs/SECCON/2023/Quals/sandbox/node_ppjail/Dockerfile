FROM node:20.6.0-slim
WORKDIR /app

RUN apt-get update && apt-get install -yq socat procps

COPY ["package.json", "package-lock.json", "./"]
RUN npm install

COPY flag.txt .
RUN mv flag.txt /flag-$(md5sum flag.txt | cut -c-32).txt

COPY index.ts .
RUN npm run build

USER 404:404

CMD socat -T30 tcp-listen:1337,fork,reuseaddr exec:"node index.js",pty,raw,echo=0
