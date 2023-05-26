FROM python:3.10-slim-buster

RUN pip install flask gunicorn cryptography

COPY . /app

WORKDIR /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "-t", "4"]
