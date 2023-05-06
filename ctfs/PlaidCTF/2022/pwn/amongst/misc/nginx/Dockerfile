FROM nginx
ADD default.conf /etc/nginx/conf.d/default.conf
ADD htpasswd /etc/nginx/htpasswd
COPY --from=amongst-game /amongst/packages/client/dist /amongst
