FROM python:alpine

WORKDIR /app
RUN apk add openssl
RUN pip install aiosmtpd dnspython flask
RUN openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -sha256 -days 365 -subj '/CN=localhost' && \
    chown nobody:nobody key.pem cert.pem
COPY relay.py app.py /app/
ENV FLAG=you-wish
CMD python -m aiosmtpd --tlscert cert.pem --tlskey key.pem -l 0.0.0.0:8025 -c relay.RelayHandler

# docker build -t image_name .
# docker run --rm -it -p 8025:8025 -p 5000:5000 image_name
