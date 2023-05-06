FROM python:3.10-bullseye

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY run.sh /
COPY app /app

ENV FLASK_ENV=production
CMD ["/run.sh"]
