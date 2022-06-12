FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir /bot
WORKDIR /bot
RUN apt update
RUN apt-get install -yqq unzip wget curl xvfb python3-pip python3 libglib2.0-0 libnss3
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable
RUN pip3 install selenium crx_unpack flask
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN wget https://clients2.googleusercontent.com/crx/blobs/Acy1k0bbwG5Wh-qGH0oyX5LPntIE4Wi9eTn_ZuX5x5LaoXvw_QjbpxTLFRQhNKw21zwQGKoQKj15juiCYWd7fsMgYH4vI6P5EOV-MxdYaHLJvZtmO741AMZSmuVP2rX1JQYYqqQF6ByWWLosRAsMGQ/extension_0_7_0_0.crx
RUN python3 -m crx_unpack xo extension_0_7_0_0.crx ninja-cookie

COPY bot.py /bot/bot.py
EXPOSE 8000
ENTRYPOINT FLASK_APP=bot.py xvfb-run flask run --host 0.0.0.0 --port 8000
