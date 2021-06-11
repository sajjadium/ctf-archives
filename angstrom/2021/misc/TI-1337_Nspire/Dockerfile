# build: docker build . -t ti1337nspire
# run: docker run --rm --name ti1337nspire -p 1337:1337 ti1337nspire
# connect: nc localhost 1337
# stop: docker kill ti1337nspire
FROM python:3.9.2-slim
RUN apt-get update && apt-get install -y socat git build-essential
WORKDIR /run
RUN git clone --single-branch --branch v3.9.2 --depth 1 https://github.com/python/cpython.git
WORKDIR /run/cpython
COPY patch.diff .
RUN git apply patch.diff && ./configure && make
RUN echo 1337:x:1337:1337::: >> /etc/passwd
COPY ti1337nspire.py /run
COPY constants.py /run
RUN chmod +x /run/ti1337nspire.py
COPY flag.txt /flag.txt
RUN mv /flag.txt /flag.`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`.txt
EXPOSE 1337
LABEL options='{"ports": {"1337": 21337}}'
CMD while :; do socat TCP-LISTEN:1337,fork,reuseaddr,su=1337 EXEC:"/run/ti1337nspire.py"; done
