FROM ubuntu:22.10
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update
RUN apt-get install -y nginx
COPY default /etc/nginx/sites-available/default
EXPOSE 80

CMD nginx -g 'daemon off;'
