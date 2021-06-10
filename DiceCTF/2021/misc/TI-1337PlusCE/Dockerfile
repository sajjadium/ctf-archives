FROM python:3.9.1-slim
RUN apt-get update && apt-get install -y socat git build-essential
WORKDIR /run
RUN git clone --single-branch --branch v3.9.1 --depth 1 https://github.com/python/cpython.git
WORKDIR /run/cpython
COPY patch.diff .
RUN git apply patch.diff && ./configure --prefix=/opt/python && export COMPILE_SECRET=`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20` && make CFLAGS="-D FROZEN_SECRET=\\\"`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`\\\" -D COMPILE_SECRET=\\\"$COMPILE_SECRET\\\"" && unset COMPILE_SECRET
RUN python3 -m pip install colr
RUN echo 1337:x:1337:1337::: >> /etc/passwd
COPY ti1337plusce.py /run
RUN chmod +x /run/ti1337plusce.py && mkdir /tmp/ti1337 && chmod 733 /tmp/ti1337
COPY flag.txt /flag.txt
RUN mv /flag.txt /flag.`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`.txt
WORKDIR /tmp/ti1337
EXPOSE 1337
CMD while :; do socat TCP-LISTEN:1337,fork,reuseaddr,su=1337 EXEC:"/run/ti1337plusce.py"; done
