FROM python:3.10.8-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . .
CMD ["waitress-serve", "--host=0.0.0.0", "--port=3000", "--threads=16", "app:app"]
