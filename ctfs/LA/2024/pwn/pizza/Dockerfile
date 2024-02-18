FROM pwn.red/jail

COPY --from=debian@sha256:36a9d3bcaaec706e27b973bb303018002633fd3be7c2ac367d174bafce52e84e / /srv
COPY pizza /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
