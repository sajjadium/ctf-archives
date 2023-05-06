FROM nginx:1.23.3-alpine-slim

COPY nginx.conf /etc/nginx/nginx.conf
COPY flag.txt /usr/share/nginx/html/flag.txt

RUN cd /usr/share/nginx/html && \
    dd if=/dev/random of=2gb.txt bs=1M count=2048 && \
    cat flag.txt >> 2gb.txt && \
    rm flag.txt
