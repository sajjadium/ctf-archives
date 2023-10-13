FROM python:alpine

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache socat
RUN pip install -r requirements.txt

COPY ./lucky_number.py /lucky_number.py

EXPOSE 1024

ENTRYPOINT [ "socat", "tcp-l:1024,reuseaddr,fork", "exec:'/lucky_number.py'" ]

