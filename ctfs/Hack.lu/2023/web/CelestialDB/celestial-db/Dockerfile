FROM alpine:3.18 as builder

RUN apk add --no-cache gcc musl-dev

WORKDIR /app
COPY readflag.c /app/
RUN gcc -o readflag readflag.c

FROM postgres:15.4-alpine3.18

COPY --from=builder /app/readflag /readflag
COPY flag /flag

RUN chown 0:0 /readflag \
    && chmod u+s /readflag \
    && chown 0:0 /flag \
    && chmod 400 /flag

COPY ./initdb-templates /templates
COPY celestial-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/celestial-entrypoint.sh"]
CMD ["postgres"]
