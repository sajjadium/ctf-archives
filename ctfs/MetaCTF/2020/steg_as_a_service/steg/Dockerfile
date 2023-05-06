FROM debian:bullseye

RUN apt-get update -y && apt-get install python3-pip libjpeg62 libmcrypt4 libmhash2 -y
RUN python3 -m pip install flask
RUN mkdir -p /steg

ADD steghide /usr/bin/steghide
ADD flag.txt /steg/flag.txt
ADD www /steg/www
ADD init.sh /bin/init.sh

RUN groupadd -r steg && useradd -r -g steg steg && \
    chown -R root:steg /steg && \
    chmod -R 750 /steg/www/ && \
    chown root:root /steg/www/uploads && \
    chmod 440 /steg/flag.txt && \
    chmod 777 /steg/www/uploads && \
    chmod 555 /usr/bin/steghide && \
    chmod 550 /bin/init.sh
    

ENTRYPOINT [ "/bin/init.sh" ]

EXPOSE 8000
