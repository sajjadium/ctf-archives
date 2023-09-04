FROM ghcr.io/downunderctf/docker-vendor/nsjail:ubuntu-22.04

ENV TMP_ENABLED=1

COPY ./flag.txt /home/ctf/chal
COPY ./daas.py /home/ctf/chal/pwn

RUN chmod +x /home/ctf/chal/pwn

# decompyle3 only supports python <= 3.8
RUN apt-get update \
    && apt-get install -y libssl-dev openssl build-essential zlib1g-dev wget \
	&& cd /tmp \
	&& wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz \
	&& tar xzvf Python-3.8.10.tgz \
	&& cd Python-3.8.10 \
	&& ./configure \
	&& make \
	&& make install \
	&& rm -rf /var/lib/apt/lists/*

# 3.9.0 is latest version of decompyle3 as of writing this challenge
RUN /usr/local/bin/python3.8 -m pip install decompyle3==3.9.0 
RUN mv /home/ctf/chal/flag.txt /home/ctf/chal/flag_$(tr -dc a-f0-9 < /dev/urandom | head -c32)