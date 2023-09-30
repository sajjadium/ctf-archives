FROM node:latest

WORKDIR /app

RUN apt-get update && apt-get install -y supervisor
RUN apt-get update && apt-get install -y chromium
ENV CHROME_BIN /usr/bin/chromium

ENV LOTTERY_PORT 4402
ENV INTERNAL_PORT 4401
ENV WEBSITE_PORT 1337
ENV SECRET "verysecretsecret"
ENV INTERNAL_SERVER "http://localhost"
ENV LOTTERY_SERVER "http://localhost"

COPY ./website/package.json ./website/
COPY ./plate-lottery/package.json ./plate-lottery/
COPY ./registration/package.json ./registration/

RUN cd ./website && npm install
RUN cd ./registration && npm install
RUN cd ./plate-lottery && npm install

COPY ./website ./website
COPY ./registration ./registration
COPY ./plate-lottery ./plate-lottery

COPY supervisord.conf /etc/supervisord.conf

# # https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container
# RUN apt-get update && apt-get install -y cron
# COPY ./cron.conf /etc/cron.d/cronjob
# COPY ./cleanup.sh /app/cleanup.sh
# RUN chmod 0644 /etc/cron.d/cronjob
# RUN chmod +x /app/cleanup.sh
# RUN crontab /etc/cron.d/cronjob

EXPOSE 1337

ENV FLAG "maple{test_flag}"

CMD /usr/bin/supervisord -c /etc/supervisord.conf
