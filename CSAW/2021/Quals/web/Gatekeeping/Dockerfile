FROM python:3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
  && apt install -y nginx \
  && pip3 install gunicorn flask pycrypto supervisor \
  && useradd -m app

COPY supervisord.conf /supervisord.conf
COPY server/ /server
RUN "/server/setup.sh"

RUN chmod -w -R /server

CMD ["supervisord", "-c", "/supervisord.conf"]
