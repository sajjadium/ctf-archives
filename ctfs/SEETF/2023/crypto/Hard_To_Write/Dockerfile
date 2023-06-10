# Running locally:
# docker build -t chal-hard-to-write .
# docker run -d -p "0.0.0.0:1337:1337" -h "chal-hard-to-write" --name="chal-hard-to-write" chal-hard-to-write
# nc 0.0.0.0 1337

FROM python:3.10
WORKDIR /app

RUN useradd -m chall
RUN pip install numpy numba
RUN apt update
RUN apt install -y socat

COPY cipher_build.py .
COPY cipher.py .
COPY server_secrets.py .
COPY server.py .

RUN chmod -R 555 /app
RUN chmod +r cipher_build.py
RUN chmod +r cipher.py
RUN chmod +r server_secrets.py
RUN chmod +r server.py

RUN python cipher_build.py

USER chall

ENTRYPOINT socat tcp-l:1337,fork,reuseaddr exec:"python server.py"