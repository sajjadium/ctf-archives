FROM python:3.11-alpine

# Install packages
RUN apk update \
    && apk add --no-cache --update chromium chromium-chromedriver

RUN mkdir -p /serv

WORKDIR /serv
COPY src .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV FLAG=<REDACTED>
ENV ADMIN_PASSWD=<REDACTED>

EXPOSE 1337

CMD [ "python3", "app.py"]  