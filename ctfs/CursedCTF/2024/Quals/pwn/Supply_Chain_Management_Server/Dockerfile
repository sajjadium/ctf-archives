FROM debian:unstable as buildor
COPY sources.list /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get install -y build-essential fakeroot devscripts
RUN apt-get build-dep -y xz-utils
RUN git clone https://salsa.debian.org/debian/xz-utils 
WORKDIR /xz-utils
RUN git switch -d 46cb28adbbfb8f50a10704c1b86f107d077878e6
RUN debuild -b -uc -us

FROM debian:unstable
COPY --from=buildor /liblzma5_5.6.1-1_amd64.deb /liblzma5_5.6.1-1_amd64.deb
COPY flag /flag
RUN dpkg -i /liblzma5_5.6.1-1_amd64.deb
RUN apt-get update -y
RUN apt-get install -y ssh
CMD ["sh", "-c", "mkdir -p /run/sshd && /usr/sbin/sshd -D"]
