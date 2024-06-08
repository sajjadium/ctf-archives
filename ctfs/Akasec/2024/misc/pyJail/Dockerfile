FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /usr/src/app

COPY chall.py flag.txt ./

RUN chmod 500 chall.py \
    && chown ctf:root chall.py \
    && chmod 444 flag.txt

USER ctf

EXPOSE 4444

CMD socat -T120 TCP-L:4444,fork,reuseaddr EXEC:"python3 chall.py",pty,stderr,setsid,sane,raw,echo=0
