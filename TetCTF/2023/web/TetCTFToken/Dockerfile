FROM ubuntu:latest
RUN apt-get update && apt-get install python3 python3-pip libcurl4-openssl-dev libssl-dev -y
COPY ./flag.txt /flag.txt
COPY ./TetCTFToken /home/TetCTFToken
WORKDIR /home/TetCTFToken
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]
