FROM python:slim

RUN pip3 install --no-cache flask gunicorn flask-wtf

RUN mkdir -p /var/www/chall
ADD src /var/www/chall
WORKDIR /var/www/chall

USER nobody
CMD python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app
