FROM httpd:2.4
RUN useradd -d /home/ctf -m -s /bin/bash ctf
RUN apt-get update && apt-get install apache2-dev make build-essential -y

WORKDIR /home/ctf

COPY mod_pwnable.c .
COPY httpd.conf .
COPY Makefile .

RUN chmod -R 755 /home/ctf
RUN make && make install
RUN rm -f Makefile mod_pwnable.c

RUN chown -R root:root /home/ctf
ENTRYPOINT ["httpd", "-f" , "/home/ctf/httpd.conf", "-D", "FOREGROUND"]

EXPOSE 1337
