FROM debian:bookworm-slim@sha256:24c92a69df28b21676d721fe18c0bf64138bfc69b486746ad935b49cc31b0b91 as build

RUN apt update -y && apt upgrade -y && \
    apt-get install -y wget build-essential checkinstall libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    wget https://github.com/python/cpython/archive/3538930d87e6bdd2bfffa3f674a62cc91d359d31.tar.gz && \
    tar -xzf 3538930d87e6bdd2bfffa3f674a62cc91d359d31.tar.gz && \
    cd cpython-3538930d87e6bdd2bfffa3f674a62cc91d359d31 && \
    ./configure --enable-optimizations && \
    make -j 8 && \
    make install

WORKDIR /app


FROM debian:bookworm-slim@sha256:24c92a69df28b21676d721fe18c0bf64138bfc69b486746ad935b49cc31b0b91 as prod

RUN apt update -y && apt upgrade -y && \
    apt-get install -y openssl

COPY --from=build /usr/local/bin/python3 /usr/local/bin/python3.13 /usr/local/bin/
COPY --from=build /usr/local/lib/python3.13 /usr/local/lib/python3.13

WORKDIR /app

COPY requirements/prod.txt prod.txt
RUN python3 -m pip install -r prod.txt

COPY chal/ /app/

RUN python3 -m pip install .

ENV FLAG "bctf{fAk3_f1@g}"
CMD gunicorn -b 0.0.0.0 skribl:app

