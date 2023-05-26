FROM python:3.8.5-slim-buster

RUN pip install flask gunicorn
WORKDIR /app
COPY . .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-t", "4", "app:app"]

