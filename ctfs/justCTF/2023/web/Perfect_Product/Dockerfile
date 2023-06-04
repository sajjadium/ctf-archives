FROM debian:sid

ENV NODE_ENV "production"

RUN apt update && \
    apt install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt install -y nodejs

RUN groupadd -g 99999 justctf && \
    useradd --uid 99999 --gid 99999 justctf && \
    mkdir /home/justctf && \
    chown justctf /home/justctf -R && \
    chmod 755 /home/justctf -R

WORKDIR /home/justctf/

COPY src/ /home/justctf/
COPY flag.txt /flag

RUN mv readflag /readflag

RUN chown root:root /flag && chmod 700 /flag
RUN chown root:root /readflag && chmod 4755 /readflag


RUN npm install

USER justctf

EXPOSE 80
CMD [ "node", "app.js" ]