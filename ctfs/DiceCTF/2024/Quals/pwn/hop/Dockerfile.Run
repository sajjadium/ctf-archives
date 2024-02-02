FROM debian:bookworm-slim as base
RUN apt update && apt install -y libcrypt1 && rm -rf /var/lib/apt/lists/*


FROM pwn.red/jail
COPY --from=base / /srv
COPY flag.txt /srv
COPY hook.sh /jail/hook.sh
COPY out/ /srv/app
COPY run_inner.sh /srv/app/run
ENV JAIL_ENV_LIBJS_JIT=1
ENV JAIL_TMP_SIZE=4096
