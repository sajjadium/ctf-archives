FROM node:lts-buster
WORKDIR /app/

COPY ./app/ /app
RUN cd /app && npm install

RUN useradd ctf
RUN chown -R root:ctf /app/ && \
    chmod -R 755 /app/
RUN apt update && apt -y install sudo
RUN mkdir -p /home/ctf && \
    chmod 755 /home/ctf && \
    chown -R root:ctf /home/ctf

RUN chmod 1733 /tmp /var/tmp /dev/shm /proc && \
    chmod go-rx /usr/bin/wall && \
    chmod go-rx /usr/bin/ch* && \
    chmod go-rx /bin/ch*

USER ctf
CMD ["sh", "-c", "NODE_ENV=production node main.js 2>&1 >/dev/null"]
