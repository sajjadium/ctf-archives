# alpine:alpine:3.15.4
FROM alpine@sha256:a777c9c66ba177ccfea23f2a216ff6721e78a662cd17019488c417135299cd89 AS app
RUN apk add --update libseccomp

FROM redpwn/jail:0.1.3

COPY --from=app / /srv

# create bin/flag.txt with whatever inside
COPY bin/flag.txt /srv/app/
COPY bin/chall /srv/app/run
