FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get install -y wget

# Add users
RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd pwn && useradd -g pwn pwn
RUN printf "/bin/bash\n" | chsh pwn

RUN mkdir -p /home/pwn
RUN chown -R pwn:admin /home/pwn
RUN chmod 775 /home/pwn
WORKDIR /home/pwn/

# Add sharr
ADD sharr .
RUN chown admin:root sharr
RUN chmod 4555 sharr

# Add flag
RUN echo "nek0pts{*** REDACTED ***}" > flag.txt
RUN chmod 440 /home/pwn/flag.txt
RUN chown admin:root /home/pwn/flag.txt
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

USER pwn
