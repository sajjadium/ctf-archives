FROM node:10

RUN groupadd -g 99999 justctf && \
    useradd --uid 99999 --gid 99999 justctf && \
    mkdir /home/justctf && \
    chown justctf /home/justctf -R && \
    chmod 755 /home/justctf -R
USER justctf

WORKDIR /home/justctf

COPY package*.json ./

RUN npm ci --only=production

COPY . .

CMD [ "node", "bin/www" ]