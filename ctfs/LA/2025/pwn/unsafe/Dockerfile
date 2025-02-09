# This image has opam 2.1.0-1 installed, which is unfortunately no longer easily apt-installable since it's now 2.2.1-1, or smth
FROM asdiml/lactf-2025:unsafe as app

COPY unsafe.ml /app/chall.ml
RUN ocamlopt -o /app/run /app/chall.ml

COPY solve.py /app

FROM pwn.red/jail

COPY --from=app / /srv
COPY flag.txt /srv/app/
RUN chmod 755 /srv/app/run

ENV JAIL_TIME 60
ENV JAIL_MEM 200M
ENV JAIL_TMP_SIZE 20M
ENV JAIL_PIDS 200