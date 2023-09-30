FROM python:3.10-slim-bullseye

RUN apt update && \
    apt install -y --no-install-recommends python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN mkdir -p /app/uploads

CMD ["python3","-u", "app.py"]
