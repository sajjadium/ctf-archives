FROM nginx:stable-alpine
MAINTAINER peterjson

RUN rm /etc/nginx/conf.d/default.conf

COPY ./container/nginx/default.conf /etc/nginx/conf.d

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
