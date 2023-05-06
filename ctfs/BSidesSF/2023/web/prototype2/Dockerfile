FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY . /app

WORKDIR /app

RUN chmod 777 .
RUN chmod 777 sqlite.db

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]
