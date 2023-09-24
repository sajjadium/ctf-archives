FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

RUN apt update
RUN apt install socat -yyq

RUN useradd -M -s /bin/false ctf

WORKDIR /app
COPY vuln flag.txt /app

USER ctf

CMD ["socat", "TCP-LISTEN:13003,reuseaddr,fork", "EXEC:/app/vuln"]
