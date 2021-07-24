FROM openresty/openresty

RUN apt-get update
RUN apt-get install -y iputils-ping

RUN rm /usr/bin/apt-get && rm /usr/bin/apt

RUN mkdir /tmp/cgi
COPY cgi /tmp/cgi
COPY nginx.conf /usr/local/openresty/nginx/conf
