FROM debian:bookworm

ENV DEBIAN_FRONTEND noninteractive
ENV XDG_CURRENT_DESKTOP XFCE


RUN apt-get update && \
    apt-get install -y --no-install-recommends curl jq libnss3 libgbm1 libasound2 xvfb xfce4 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup ctf && \
    adduser --disabled-password --gecos "" --ingroup ctf ctf

WORKDIR /home/ctf
COPY linux-unpacked run.sh ./
RUN chmod 4755 chrome-sandbox
COPY readflag /readflag
RUN chmod 111 /readflag

USER ctf
CMD ["sh", "-c", "timeout $TIMEOUT /home/ctf/run.sh"]
