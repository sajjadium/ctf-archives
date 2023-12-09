FROM ubuntu
FROM python:3.9

WORKDIR /app
COPY ./src /app

RUN pip install --requirement requirements.txt

CMD ["./run.sh"]
