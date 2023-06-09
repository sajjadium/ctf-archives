# docker build -t wanky-mail . && docker run -p 5000:5000 -p 8025:8025 wanky-mail

FROM python:3.9-slim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

ARG FLAG=GPNCTF{fake_flag}
RUN echo ${FLAG} > flag-$(cat /dev/urandom | tr -cd "a-f0-9" | head -c10).txt
RUN chmod 444 flag*

RUN adduser --disabled-password --gecos "" user
USER user

COPY . .

CMD ["flask", "run"]