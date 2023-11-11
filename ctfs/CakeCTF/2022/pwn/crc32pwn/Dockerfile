FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get -y update --fix-missing && apt-get -y upgrade

# Add users
RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd pwn && useradd -g pwn pwn
RUN printf "/bin/bash\n" | chsh pwn

# Add crc32sum
ADD crc32sum  /usr/bin/crc32sum
RUN chmod 555 /usr/bin/crc32sum
RUN chown admin:root /usr/bin/crc32sum
RUN chmod +s         /usr/bin/crc32sum

RUN mkdir -p /home/pwn
RUN chown -R pwn:pwn /home/pwn
WORKDIR /home/pwn/

# Add flag
ADD flag.txt  /home/pwn/flag.txt
RUN chmod 440 /home/pwn/flag.txt
RUN chown admin:root /home/pwn/flag.txt

USER pwn
