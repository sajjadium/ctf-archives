FROM python:3.8.5-slim-buster

RUN pip install flask gunicorn requests
WORKDIR /app
COPY . .

EXPOSE 5000

ENTRYPOINT ["./run.sh"]
