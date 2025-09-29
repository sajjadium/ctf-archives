FROM alpine:3.20
RUN apk add --no-cache socat ca-certificates && \
    adduser -D -u 10001 ctf
WORKDIR /app
COPY server /app/server
RUN chmod +x /app/server
USER ctf
EXPOSE 1337

ENTRYPOINT ["socat","-T60","tcp-l:1337,reuseaddr,fork","exec:/app/server"]
