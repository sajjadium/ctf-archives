FROM python:3.11

RUN pip install gunicorn
RUN apt-get update && apt-get install -y p7zip-full

WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "main:app"]
