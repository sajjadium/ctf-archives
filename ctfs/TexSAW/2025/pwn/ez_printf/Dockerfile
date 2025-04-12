from pwn.red/jail

COPY --from=ubuntu:latest / /srv

COPY vuln /srv/app/run
COPY flag.txt /srv/app/flag.txt

