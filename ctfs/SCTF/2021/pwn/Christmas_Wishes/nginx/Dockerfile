FROM nginx

COPY static /var/www/html
RUN rm -rf /etc/nginx/conf.d/*.conf &&\
    chmod -R 555 /var/www/html

COPY nginx.conf /etc/nginx/nginx.conf
COPY pwn.conf /etc/nginx/conf.d/pwn.conf