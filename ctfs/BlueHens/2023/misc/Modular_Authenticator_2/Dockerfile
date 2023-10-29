FROM python:3.8
RUN apt update
RUN apt install -y socat
RUN mkdir /server
COPY server.sh /server
COPY public_key.json /server
COPY server.py /server
COPY server.sh /server
COPY flag.txt /server
WORKDIR /server
EXPOSE 3000
CMD /server/server.sh