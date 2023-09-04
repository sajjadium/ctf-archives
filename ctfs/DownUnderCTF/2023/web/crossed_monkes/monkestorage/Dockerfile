FROM python:3.10-slim-bullseye

RUN apt update && \
    apt install -y --no-install-recommends cairosvg python3-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /monkestorage/requirements.txt
RUN pip3 install -r /monkestorage/requirements.txt

COPY . /monkestorage
WORKDIR /monkestorage

RUN /usr/sbin/useradd --no-create-home -u 1000 www-monke && \
    mkdir -p /storage && \
    chown www-monke:www-monke /storage
USER www-monke

CMD ["python3", "/monkestorage/main.py"]