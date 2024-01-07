FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
COPY flag / 
RUN sh -c 'dst=$(head -c 10 /dev/urandom | base32); mkdir $dst; mv flag $dst/flag' 

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y build-essential wget unzip

COPY chal.c /home/user/
WORKDIR /home/user/
RUN wget https://www.sqlite.org/2023/sqlite-amalgamation-3440200.zip
RUN unzip sqlite-amalgamation-3440200.zip
RUN mv sqlite-amalgamation-3440200/* .
RUN gcc chal.c sqlite3.c -lpthread -DSQLITE_OMIT_LOAD_EXTENSION -o chal -lm

CMD ./chal
