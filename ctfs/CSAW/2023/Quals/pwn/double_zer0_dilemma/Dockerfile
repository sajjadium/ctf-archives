FROM ubuntu:20.04 as ctf

# Set environment variables.
ENV HOME /root
RUN id

#install gcc
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y g++-multilib
RUN apt-get install -y socat

RUN sysctl kernel.randomize_va_space=0

RUN groupadd --gid 995 ctf
RUN useradd -m --uid 995 --gid 995 ctf

COPY ./ /home/ctf/

WORKDIR /home/ctf/

RUN chmod +x run.sh

EXPOSE 9999:9999

#once compiled, change to that user
USER ctf

CMD ["./run.sh"]