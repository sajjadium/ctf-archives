FROM python:3.9.4-slim-buster

WORKDIR /home/ctf

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY nft_src .
COPY nft_web .
COPY flag.txt flag.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
