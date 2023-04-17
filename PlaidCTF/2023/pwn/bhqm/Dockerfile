FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wine
COPY baby-heap-question-mark.exe /baby-heap-question-mark.exe

COPY getFlag /getFlag
COPY flag /flag
RUN chmod +s /getFlag
RUN chmod 400 /flag

RUN useradd -m user
USER user
RUN wine nonexistent || true # Just speed up wine execution afterwards

CMD wine /baby-heap-question-mark.exe 2>/dev/null
