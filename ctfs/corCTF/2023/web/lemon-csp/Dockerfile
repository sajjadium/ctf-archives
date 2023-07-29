FROM caddy:builder AS builder
RUN xcaddy build --with github.com/mholt/caddy-webdav

FROM caddy
RUN mkdir /opt/static
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY ./Caddyfile /etc/caddy/Caddyfile

CMD caddy run --config /etc/caddy/Caddyfile