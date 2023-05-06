FROM ubuntu:17.10

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y xinetd dos2unix

WORKDIR /home/arbitrary_null_byte_write
ADD arbitrary_null_byte_write .
RUN chmod 555 ./arbitrary_null_byte_write
RUN chmod 555 .
RUN chmod 555 /home

ADD flag.txt /flag.txt
RUN chmod 444 /flag.txt

RUN useradd -ms /bin/bash arbitrary_null_byte_write
ADD arbitrary_null_byte_write.xinetd /etc/xinetd.d/arbitrary_null_byte_write
RUN dos2unix /etc/xinetd.d/arbitrary_null_byte_write
RUN chmod 444 /etc/xinetd.d/arbitrary_null_byte_write
RUN echo "arbitrary_null_byte_write         60010/tcp" >> /etc/services

RUN service xinetd restart

RUN chown -R root:root .

EXPOSE 60010

CMD service xinetd restart && sleep infinity
