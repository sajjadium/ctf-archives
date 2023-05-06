# Binary Container Copy
FROM warning:static as binary

WORKDIR /bins
RUN ls -la /home/builder/build/
RUN cp /home/builder/build/warning /bins/

# Actual Challenge Container
FROM ubuntu:22.04

RUN apt update &&\
    apt install -y tini gdb python3 python3-pip git

RUN pip3 install pwntools
WORKDIR /challenge/ptools/
RUN git clone https://github.com/pwndbg/pwndbg.git && cd pwndbg && ./setup.sh

WORKDIR /challenge

COPY warning ./

# If you'd like to use your own copy of the challenge uncomment this line out
# This is the binary from the static container
# COPY --from=binary  /bins/warning ./

RUN useradd -ms /bin/bash challenge
RUN chown -R challenge:challenge /challenge

USER challenge

CMD ["tini", "--", "./warning"]