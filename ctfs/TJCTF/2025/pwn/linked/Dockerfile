FROM pwn.red/jail:0.3.0
COPY --from=ubuntu@sha256:6015f66923d7afbc53558d7ccffd325d43b4e249f41a6e93eef074c9505d2233 / /srv
COPY chall /srv/app/run
RUN chmod +x /srv/app/run
COPY flag.txt /srv/app/
ENV JAIL_TIME=60