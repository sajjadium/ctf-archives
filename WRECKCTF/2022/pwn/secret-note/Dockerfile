FROM pwn.red/jail:0.3.0

COPY --from=ubuntu@sha256:d5c260797a173fe5852953656a15a9e58ba14c5306c175305b3a05e0303416db / /srv
COPY flag.txt /srv/app/
COPY notebook /srv/app/run
