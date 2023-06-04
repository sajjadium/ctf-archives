FROM golang:1.19

WORKDIR /app
COPY . .

RUN chmod 755 /app
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /app/main main.go
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /app/bot bot.go
RUN chmod 755 /app/main /app/bot

RUN apt-get update -y && apt-get install -y wget curl unzip gnupg

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable

# This could be done shorter but idk
RUN groupadd -g 99999 jailed
RUN useradd --uid 99999 --gid 99999 jailed
RUN mkdir /home/jailed
RUN chown jailed /home/jailed -R
RUN chmod 755 /home/jailed -R
USER jailed

EXPOSE 8000

# Run
CMD ["/app/main"]
