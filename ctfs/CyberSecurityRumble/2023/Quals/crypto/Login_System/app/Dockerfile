FROM python:3.10-buster

RUN apt update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m ctf
USER ctf

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD socat TCP-LISTEN:1337,fork,reuseaddr EXEC:"/usr/bin/env python3 /app/main.py",pty,stderr