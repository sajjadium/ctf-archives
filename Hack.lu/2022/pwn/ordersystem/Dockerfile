# docker build -t ordersystem . && docker run -p 4444:4444 --rm -it ordersystem
# tip: watch out for appending vs overwriting
 
FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y ncat python3


RUN useradd -ms /bin/bash user

RUN mkdir /work
WORKDIR /work
RUN mkdir storage plugins


COPY main.py .
COPY disk.py .
COPY plugin.py .
ENV flag="flag{fakeflag}"


RUN chown -R user:user /work
USER user
CMD python3 main.py
