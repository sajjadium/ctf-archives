FROM node:slim

RUN apt update
RUN apt install -y nginx
COPY nginx.conf /etc/nginx/sites-available/default

COPY app /app
WORKDIR /app
RUN npm i

ENV NODE_ENV=production

RUN useradd ctf
RUN chown -R ctf `ls -I node_modules`

COPY run.sh run.sh
RUN chmod +x ./run.sh

ENTRYPOINT ["bash", "./run.sh"]
