from python:2.7.16-alpine

EXPOSE 8080

WORKDIR /usr/src/app

RUN apk add build-base linux-headers

COPY challenge/requirements.txt .

RUN pip install -r requirements.txt

COPY challenge/. .

RUN pip install .

CMD glacier-blog
