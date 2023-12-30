FROM ubuntu@sha256:6042500cf4b44023ea1894effe7890666b0c5c7871ed83a97c36c76ae560bb9b

ENV DEBIAN_FRONTEND noninteractive
ENV XDG_CURRENT_DESKTOP XFCE

RUN apt-get update && \
    apt-get install -y --no-install-recommends libnss3 libgbm1 libasound2 xvfb xfce4 ca-certificates python3 socat
RUN useradd -m pwn
COPY ./flag.txt /flag.txt
COPY ./stuff/libs /home/pwn/libs
COPY ./stuff/libs/swrast_dri.so /usr/lib/x86_64-linux-gnu/dri/swrast_dri.so
COPY ./stuff/SimpleNES /home/pwn/SimpleNES
COPY ./stuff/run.py /home/pwn/run.py
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:/home/pwn/run.py"]

