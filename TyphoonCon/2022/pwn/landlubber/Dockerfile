FROM ubuntu:22.04

RUN dpkg --add-architecture i386 && apt-get update && apt-get -y install wine wine64 xvfb wine32

WORKDIR /app/data

COPY landlubber.exe ..
COPY flag.txt ..
CMD ls -R ../ && (Xvfb :1 & DISPLAY=:1 wine64 ../landlubber.exe)
