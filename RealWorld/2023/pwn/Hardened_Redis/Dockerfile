FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install  -qy redis 


COPY redis.conf /etc/redis.conf
COPY flag /flag
COPY readflag /readflag

RUN chown root:root /etc/redis.conf && chmod 0655 /etc/redis.conf
RUN chown root:root /flag && chmod 0600 /flag
RUN chmod u+s /readflag && chmod +x /readflag

USER redis
ENTRYPOINT [ "redis-server", "/etc/redis.conf"]
