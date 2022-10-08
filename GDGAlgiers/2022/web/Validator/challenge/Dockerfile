FROM python:3.10

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install nginx

COPY requirements.txt /tmp/

RUN python -m pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    useradd ctf && \
    mkdir -p /ctf

COPY nginx.conf entrypoint.sh /ctf/

COPY app /ctf/app/

WORKDIR /ctf

RUN chmod +x entrypoint.sh

USER ctf

ENTRYPOINT ["./entrypoint.sh"]
