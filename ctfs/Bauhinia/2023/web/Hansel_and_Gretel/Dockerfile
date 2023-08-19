FROM ubuntu:20.04

ENV FLAG b6actf{test_flag}

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install requests flask flask-session

RUN mkdir /app
COPY app /app
COPY start.sh /start.sh
RUN chmod 555 /start.sh

WORKDIR /app

CMD [ "/start.sh" ]