# FROM python:3.8-alpine
FROM tiangolo/uwsgi-nginx-flask:python3.8

ADD ./app /app/
WORKDIR /app

RUN addgroup --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 appuser

RUN chown -R appuser:appuser /app && \
    find /app -type d -exec chmod 550 {} + && \
    find /app -type f -exec chmod 660 {} + && \
    chmod 770 /app/database && \
    chmod 770 /app/backup && \
    chmod 770 /app/logs

RUN apt-get install tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone

RUN pip install -r requirements.txt
