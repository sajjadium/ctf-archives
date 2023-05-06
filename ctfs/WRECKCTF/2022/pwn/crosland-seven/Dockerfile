FROM pwn.red/jail:0.3.0

COPY --from=ubuntu@sha256:a0a45bd8c6c4acd6967396366f01f2a68f73406327285edc5b7b07cb1cf073db / /srv
COPY flag.txt /srv/app/
COPY crosland /srv/app/run
