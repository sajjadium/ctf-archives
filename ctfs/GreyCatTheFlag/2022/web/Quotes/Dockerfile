FROM python:3.8.10-slim
ADD . /app
WORKDIR /app
RUN apt update \
    && apt install -y wget unzip bzip2 firefox-esr \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz \
    && tar xf geckodriver-v0.31.0-linux64.tar.gz \
    && rm geckodriver-v0.31.0-linux64.tar.gz \
    && pip install -r requirements.txt
