FROM python:3.8-slim-buster

RUN apt update && \
      apt install -y curl gnupg2
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

RUN apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y google-chrome-stable nodejs npm && \
      apt update && \
      rm -rf /var/lib/apt/lists/*


RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true npm install puppeteer@11.0.0

WORKDIR /app

RUN pip3 install flask gunicorn

COPY . /app

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

EXPOSE 1337

CMD gunicorn -b 0.0.0.0:1337 app:app
