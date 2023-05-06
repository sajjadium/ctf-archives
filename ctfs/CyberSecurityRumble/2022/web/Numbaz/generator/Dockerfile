FROM ubuntu:20.10

RUN apt-get update
RUN apt-get install python3-dev python3-pip gunicorn3 build-essential cmake libicu-dev libxerces-c-dev tar wget libexpat1-dev -y
ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt


RUN mkdir /xalan
WORKDIR /xalan

ADD https://github.com/apache/xalan-c/releases/download/Xalan-C_1_12_0/xalan_c-1.12.tar.gz .
RUN tar -xvf xalan_c-1.12.tar.gz
WORKDIR /xalan/xalan_c-1.12
RUN mkdir build && cd build && cmake ..
WORKDIR /xalan/xalan_c-1.12/build
RUN make -j4 2> /dev/null

ADD . /app/
WORKDIR /app/

RUN cp /xalan/xalan_c-1.12/build/src/xalanc/Xalan /app/Xalan

WORKDIR /app
EXPOSE 1024
ENTRYPOINT gunicorn --bind 0.0.0.0:5001 server:app