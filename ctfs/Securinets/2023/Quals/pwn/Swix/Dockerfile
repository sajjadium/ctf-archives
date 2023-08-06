FROM ubuntu@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508 AS app

RUN apt-get upgrade
RUN apt-get update

RUN dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt install -y \
    libc6:i386 \
    libc6-dbg:i386 \
    libc6-dbg \
    lib32stdc++6 \
    g++-multilib

RUN useradd -p ctf ctf

# FROM pwn.red/jail
# COPY --from=app / /srv

COPY main /app/main
COPY flag.txt /app/flag.txt

RUN mv /app/flag.txt /app/flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt

COPY menu /app/menu
COPY msg2 /app/msg2
COPY msg3 /app/msg3
COPY age /app/age
COPY logo /app/logo
COPY uname /app/uname

COPY run.sh /app/run.sh
COPY ynetd /app/ynetd

WORKDIR /app
USER ctf

CMD ./ynetd -p 5000 ./run.sh
