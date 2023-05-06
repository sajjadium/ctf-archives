#FROM ubuntu:22.04
FROM python:slim-bullseye
#FROM python:3.11-bullseye

RUN apt update && apt-get install --no-install-recommends -y \
  build-essential \
  python3-dev \
  uwsgi \
  uwsgi-plugin-python3 \
  && rm -rf /var/lib/apt/lists/*

COPY flag /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chown root:root /flag     && chmod 400 /flag
RUN chown root:root /readflag && chmod 4755 /readflag

COPY ./chall.py /app/
COPY ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt
#RUN pip3 install --no-cache-dir 'Flask==2.2.2' 'celery==5.2.7'

RUN useradd --no-create-home --home-dir / --shell /bin/false kalmar

ENTRYPOINT ["uwsgi", "--http-socket", ":5000", "--master", "--processes", "8", "--threads", "4", "--uid", "kalmar", "--gid", "kalmar", "--wsgi-file", "/app/chall.py"]
