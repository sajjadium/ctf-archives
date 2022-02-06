FROM denoland/deno

RUN apt update && apt install -y supervisor nginx

COPY flag.txt /flag.txt
COPY readflag /readflag

RUN chmod 400 /flag.txt
RUN chmod 6755 /readflag

RUN mkdir -p /app
WORKDIR /app

COPY challenge .

RUN deno compile --allow-read --allow-write --allow-net app.ts
RUN chmod 755 /app/app

COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]