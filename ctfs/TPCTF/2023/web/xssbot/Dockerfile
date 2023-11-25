FROM debian:buster-slim

RUN sed -i "s@http://.*deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN sed -i "s@http://.*security.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN apt update && apt install -y --no-install-recommends python3 python3-pip python3-selenium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY bot.py /app
WORKDIR /app
RUN echo TPCTF{test} > /flag

ENTRYPOINT ["python3", "-u", "bot.py"]