FROM node:lts-buster
WORKDIR /app/

COPY ./app/ /app
RUN cd /app && npm install

RUN useradd ctf
RUN chown -R root:ctf /app/ && \
    chmod -R 755 /app/
RUN apt update && apt -y install sudo
RUN mkdir -p /home/ctf/.npm && \
    chmod 755 /home/ctf && chmod 775 /home/ctf/.npm && \
    chown -R root:ctf /home/ctf

RUN chmod 1733 /tmp /var/tmp /dev/shm /proc && \
    chmod go-rx /usr/bin/wall && \
    chmod go-rx /usr/bin/ch* && \
    chmod go-rx /bin/ch*

USER ctf
CMD ["sh", "-c", "NODE_ENV=production npm run start 2>&1 >/dev/null"]
