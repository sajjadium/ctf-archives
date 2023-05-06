# alpine:alpine:3.12.11
FROM alpine@sha256:6634c44a5e60f5d3f0934922deb1cbded22a4aead6fbaae4ea1b8c6981459233 AS app
RUN apk add --update libseccomp

FROM redpwn/jail:0.1.3

COPY --from=app / /srv

# create bin/flag.txt with whatever inside
COPY bin/flag.txt /srv/app/
COPY bin/chall /srv/app/run
