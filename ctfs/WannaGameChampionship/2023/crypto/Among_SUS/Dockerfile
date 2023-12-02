FROM python:3.10-alpine
RUN apk add --no-cache --update socat py3-pip

WORKDIR /chal
COPY ./requirements.txt /chal/
COPY ./server.py /chal/
COPY ./utils.py /chal/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["socat", "-t", "900", "-T", "120", "TCP4-LISTEN:12001,reuseaddr,fork", "EXEC:env PYTHONUNBUFFERED=1 python3 /chal/server.py"]