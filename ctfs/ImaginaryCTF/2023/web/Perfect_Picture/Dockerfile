FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libimage-exiftool-perl
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY flag.txt .

RUN mkdir templates
RUN mkdir uploads
RUN mkdir static
COPY templates/* templates
COPY static/* static

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
