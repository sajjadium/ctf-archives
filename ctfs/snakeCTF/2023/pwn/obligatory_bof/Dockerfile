FROM pwn.red/jail

COPY --from=ubuntu@sha256:218bb51abbd1864df8be26166f847547b3851a89999ca7bfceb85ca9b5d2e95d / /srv
COPY obligatory_bof /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
