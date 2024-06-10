FROM --platform=linux/amd64 ubuntu@sha256:86ac87f73641c920fb42cc9612d4fb57b5626b56ea2a19b894d0673fd5b4f2e9 AS build

RUN apt-get update && apt-get install -y wget gcc && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c "https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c" \
    && gcc -o ynetd ynetd.c && rm ynetd.c && chmod +x ./ynetd

COPY chall.c .
RUN gcc -o chall chall.c


FROM --platform=linux/amd64 ubuntu@sha256:86ac87f73641c920fb42cc9612d4fb57b5626b56ea2a19b894d0673fd5b4f2e9

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

COPY --from=build ynetd .
RUN chmod +x ynetd

COPY --from=build chall chall
COPY flag.txt .
COPY secret_flag.txt .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 9999
CMD ./ynetd -p 9999 ./chall