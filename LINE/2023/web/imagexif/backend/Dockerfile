FROM python:3.11.2

RUN apt-get update 

RUN apt-get install -y curl wget && \
    DEBIAN_FRONTEND="noninteractive"         && \
    echo done

RUN wget https://github.com/exiftool/exiftool/archive/refs/tags/12.22.tar.gz && \
    tar xvf 12.22.tar.gz && \
    cp -fr /exiftool-12.22/* /usr/bin && \
    rm -rf /exiftool-12.22 && \
    rm 12.22.tar.gz

ADD ./src /src/
ADD ./conf /conf/

WORKDIR /src

COPY uwsgi.ini .

RUN addgroup --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 -r -s /bin/false appuser

RUN find /src -type d -exec chmod 755 {} + && \
    find /src -type f -exec chmod 644 {} + && \
    find /src -type f -exec chattr +i {} \; && \
    find /src/tmp -type d -exec chmod 777 {} + && \ 
    find /src/*.sh -exec chmod +x {} \;

RUN apt-get install -y tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone

RUN python3.11 -m pip install -r requirements.txt
RUN python3.11 -m pip install uwsgi 
RUN apt-get purge -y curl wget

RUN ln -sf /bin/bash /bin/sh

CMD ["uwsgi", "uwsgi.ini"]

RUN chmod o-x /usr/local/bin/python3.11 && \ 
    rm /usr/lib/x86_64-linux-gnu/perl-base/Socket.pm 