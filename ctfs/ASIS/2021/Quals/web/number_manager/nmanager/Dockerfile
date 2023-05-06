FROM ubuntu:21.10

ENV debian_frontend=noninteractive
RUN apt update
RUN apt upgrade -y
RUN apt install build-essential git -y

WORKDIR /app
COPY ./stuff/ /app
RUN git clone https://github.com/embedthis/goahead.git
WORKDIR /app/goahead
RUN git checkout d8ae25c5f8cc1b78207b078ebfac25e0332f96c6
RUN patch -s -p0 < ../main.patch
RUN make compile
WORKDIR /app
RUN mkdir ./static/descriptions
RUN chmod 777 ./static/descriptions
RUN chmod +x ./run.sh

RUN useradd www
USER www

CMD ./run.sh
