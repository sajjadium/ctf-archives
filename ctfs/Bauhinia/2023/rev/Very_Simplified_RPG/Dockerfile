FROM nginx:alpine

WORKDIR /etc/nginx/conf.d
COPY webgl.conf default.conf

WORKDIR /webgl
COPY webgl/ .
RUN chmod -R 755 /webgl