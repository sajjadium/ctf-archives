FROM mcr.microsoft.com/playwright:jammy
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get update && apt-get install -y  \
  openjdk-17-jre-headless \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/app
RUN mkdir /var/log/adminplz/
WORKDIR /usr/src/app

RUN npm i playwright-chromium

COPY adminplz-0.0.1-SNAPSHOT.jar ./
COPY bot.js ./
COPY public ./public
COPY flag.html /flag.html

ENV ADMIN_PASSWORD=fake_password

CMD ["java", "-jar", "adminplz-0.0.1-SNAPSHOT.jar"]
