FROM pwn.red/jail

# copy / from <some image> to /srv
COPY --from=ubuntu@sha256:2f18a21d414ad3c0a8eea08fec8f98d730c5c02ddb0d5fef9c60ca72ac53329c / /srv

COPY dist/pureland /srv/app/run
COPY flag.txt /srv/app/flag.txt