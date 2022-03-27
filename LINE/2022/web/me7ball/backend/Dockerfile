# FROM python:3
# FROM alpine:uwsgi-python3

FROM ubuntu:20.04

RUN apt-get update                           && \
    apt-get upgrade -y                       && \
    apt-get install -y python3               && \
    apt-get install -y python3-pip           && \
    apt-get install -y libmysqlclient-dev    && \
    DEBIAN_FRONTEND="noninteractive"   apt-get install -y uwsgi    && \
    apt-get install -y uwsgi-plugin-python3  && \
    echo done


ADD ./src /src/
ADD ./logs /logs/
ADD ./conf /conf/

WORKDIR /src

COPY uwsgi.ini .

RUN addgroup --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 appuser

RUN chown -R appuser:appuser /src && \
    chown -R appuser:appuser /logs && \
    find /src -type d -exec chmod 550 {} + && \
    find /src -type f -exec chmod 660 {} + && \
    chmod 770 -R /logs

RUN apt-get install tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone

RUN pip install -r requirements.txt
RUN pip install uwsgi 

RUN service uwsgi start

CMD ["uwsgi", "uwsgi.ini"]
