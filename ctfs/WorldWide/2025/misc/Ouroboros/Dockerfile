FROM python:alpine
RUN apk update && \
    apk add --no-cache socat gcc nsjail
RUN passwd -l root \
    && adduser -S -D -H -u 1000 user
WORKDIR /home/user
ENV FLAG=wwf{this_is_not_a_flag}
COPY chall.py wrapper.sh /home/user/
RUN chmod -R 555 /home/user
USER user
CMD socat -dd TCP4-LISTEN:1337,fork,reuseaddr SYSTEM:/home/user/wrapper.sh