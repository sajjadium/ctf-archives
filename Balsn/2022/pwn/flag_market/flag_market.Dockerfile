FROM ubuntu:20.04
MAINTAINER how2hack
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install -y xinetd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git libtool pkg-config make python3 python3-pip help2man
RUN pip install -U pip pycrypto
RUN useradd -m flag_market
WORKDIR /home/flag_market
RUN git clone https://github.com/frankmorgner/vsmartcard.git
WORKDIR /home/flag_market/vsmartcard
RUN git checkout 8b4aa3e7bfe891d986237759576b5ebf0e4ed42b
COPY src/patch.diff /home/flag_market/vsmartcard/
RUN git apply patch.diff
WORKDIR /home/flag_market/vsmartcard/virtualsmartcard
RUN autoreconf --verbose --install
RUN ./configure --sysconfdir=/etc --enable-libpcsclite
RUN make
RUN make install
COPY src/flag_market /home/flag_market/
COPY src/run.sh /home/flag_market/
COPY src/flag3 /home/flag_market/
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/flag_market
USER flag_market
CMD ["/home/flag_market/run.sh"]
