FROM ubuntu:20.04

RUN useradd --create-home --shell /bin/bash compfest12
RUN useradd --create-home --shell /bin/bash flag
RUN apt-get update
RUN apt-get install -y --no-install-recommends xinetd

COPY share/files/* /home/compfest12/
COPY share/flag/* /home/flag/

RUN chmod 555 /home/compfest12/
RUN chmod 555 /home/flag/
RUN chmod 400 /home/flag/flag.txt && chmod 555 /home/flag/readFlag
RUN chown flag:flag /home/flag/flag.txt && chown flag:flag /home/flag/readFlag
RUN chmod +s /home/flag/readFlag

WORKDIR /home/compfest12
USER compfest12

CMD ["xinetd", "-dontfork"]
