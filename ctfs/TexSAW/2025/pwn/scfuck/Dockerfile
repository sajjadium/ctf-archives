FROM pwn.red/jail

# gcc:13.3.0
COPY --from=gcc@sha256:e19f51a9e2f80b02aaf89f64aad9865d445f6e2762267630aacec9c7029a0a2a / /srv

COPY main.py /srv/app/run
COPY flag.txt /srv/flag.txt
ENV JAIL_MEM=20M JAIL_PIDS=20 JAIL_TMP_SIZE=64K JAIL_ENV_PATH=/usr/local/bin:/usr/bin:/bin
