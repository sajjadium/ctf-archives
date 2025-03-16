FROM python:3.12

RUN apt-get update && apt-get install -y socat

WORKDIR /app
COPY . .
RUN chmod 444 flag.txt

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:'python3 jail.py'"]