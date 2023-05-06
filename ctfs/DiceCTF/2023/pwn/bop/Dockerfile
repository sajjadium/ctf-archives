FROM pwn.red/jail:0.3.1

COPY --from=ubuntu@sha256:bffb6799d706144f263f4b91e1226745ffb5643ea0ea89c2f709208e8d70c999 / /srv
COPY flag.txt /srv/app/
COPY bop /srv/app/run
