FROM python:3.9-buster

ARG USERNAME

RUN true \
    && mkdir /var/log/Draupnir \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update \
    && apt-get install -y xinetd tini nodejs \
    && apt-get install -y nodejs \
    && rm -rf /var/cache/apt/archives \
    && useradd -m Draupnir \
    && npm install -g ganache-cli \
    && pip install web3 flask flask_cors gunicorn \
    && true

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt 

ENV PYTHONPATH /home/Draupnir

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/home/Draupnir/entrypoint.sh"]
