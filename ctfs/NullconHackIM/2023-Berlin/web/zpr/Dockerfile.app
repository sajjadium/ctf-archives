FROM python:latest

RUN apt-get update -y && apt-get install -y unzip

WORKDIR /app
COPY ./code/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD python app.py