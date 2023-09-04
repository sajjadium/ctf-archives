FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

COPY src /app

WORKDIR /app

ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "8", "-b", "0.0.0.0:8002", "app:app"]