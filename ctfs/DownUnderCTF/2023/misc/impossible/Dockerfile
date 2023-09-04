FROM python:3.10-slim-bullseye

COPY ./app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app/ .

CMD ["python3", "/app/main.py"]