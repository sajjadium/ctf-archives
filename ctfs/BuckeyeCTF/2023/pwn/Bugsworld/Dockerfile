FROM ubuntu:jammy-20230816 AS app
RUN apt-get update && apt-get install -y gcc make

WORKDIR /app
COPY Makefile flag.txt bugsworld.c ./
RUN make

FROM pwn.red/jail
COPY --from=app / /srv
RUN mv /srv/app/bugsworld /srv/app/run