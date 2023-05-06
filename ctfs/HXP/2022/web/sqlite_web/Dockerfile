# see docker-compose.yml

FROM debian:bullseye

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        python3 python3-pip \
        git \
        wget \
        unzip \
        coreutils \
    && rm -rf /var/lib/apt/lists/

RUN pip3 install flask peewee pygments

#  # Permission
#  7 rwx
#  6 rw-
#  5 r-x
#  4 r--
#  3 -wx
#  2 -w-
#  1 --x
#  0 ---

COPY flag.txt readflag proxy /
RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag /proxy

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY encrypted.db patch.py /home/ctf/

RUN git clone https://github.com/coleifer/sqlite-web.git && \
    cd sqlite-web && \
    git checkout 72ae4bd921c996be85a95eb7a202d46f4a438701 && \
    python3 ../patch.py && \
    pip3 install .

RUN rm patch.py && \
    rm -r sqlite-web

RUN wget https://github.com/nalgeon/sqlean/releases/download/0.19.2/sqlean-linux-x86.zip && \
    unzip sqlean-linux-x86.zip -d ext && \
    mv ext/crypto.so . && \
    rm -rf ext && \
    rm -f sqlean-linux-x86.zip

RUN chmod 444 encrypted.db && \
    chmod 444 crypto.so

USER ctf

EXPOSE 8080
CMD nohup sqlite_web encrypted.db -x -r -e ./crypto -H 0.0.0.0 -p 80 & \
    /proxy 8080 80