# build bot
FROM golang:1.18.2 as builder_manager
WORKDIR /code/
COPY . .
RUN go build -v .


FROM ubuntu:22.04
RUN apt-get update -y && apt-get install -y wget curl unzip gnupg

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
        unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

COPY --from=builder_manager /code/bot /bin/bot

ENTRYPOINT ["/bin/bot"]
