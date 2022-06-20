FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY server server
COPY python3.7 python3.7

RUN apt-get update -y && \
  apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed" && \
  apt-get install -y --no-install-recommends build-essential libssl-dev && \
  apt-get clean

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    beautifier
USER 1001

ENV PATH="/opt/app/python3.7/bin:${PATH}"
RUN python3.7 -m pip install -U --force-reinstall pip
RUN python3.7 -m pip install aiohttp gunicorn Pillow filelock

EXPOSE 80
ENTRYPOINT ["server/docker.sh"]