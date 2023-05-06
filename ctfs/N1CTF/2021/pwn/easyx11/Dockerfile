FROM debian:unstable

#RUN sed -i "s/http:\/\/deb.debian.org/http:\/\/mirrors.tencentyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd build-essential python3 socat libx11-dev locales

RUN useradd -m ctf && \
    echo 'ctf - nproc 1500' >>/etc/security/limits.conf && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
COPY ./flag /flag
COPY ./x11 /x11
COPY ./run.py /run.py
RUN chmod 755 ./run.py && \
    chmod 755 /x11
USER ctf
CMD socat tcp-listen:8888,fork,reuseaddr EXEC:"/run.py"
EXPOSE 8888