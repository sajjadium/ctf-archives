FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install ncat python3.12 -y

COPY ./src/main.py ./main.py

EXPOSE 1234

CMD ncat -l -p 1234 --sh-exec "python3.12 /app/main.py" --keep-open