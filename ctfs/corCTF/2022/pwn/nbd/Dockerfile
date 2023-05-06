FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3

WORKDIR /app
COPY ./flag.txt .
COPY ./nbd-client .
COPY ./serv.py .

RUN useradd -m ctf
USER ctf

EXPOSE 5000
CMD ["python3", "serv.py"]
