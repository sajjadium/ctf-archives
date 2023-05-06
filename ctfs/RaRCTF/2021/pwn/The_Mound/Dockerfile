FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y \
    lib32z1 xinetd xxd \
 && rm -rf /var/lib/apt/lists/*
RUN useradd day
RUN mkdir /pwn
RUN echo "You've been blocked by our xinetd - try again, and report if this repeats." > /etc/banner_fail
COPY ./ctf.xinetd /etc/xinetd.d/pwn
COPY ./start.sh /start.sh
COPY ./setup.sh /setup.sh
COPY ./mound/mound /pwn/mound
COPY ./flag.txt /pwn/flag.txt
RUN chown -R root:day /pwn && chmod -R 750 /pwn
RUN chmod +x /setup.sh
RUN chown root:day /start.sh && chmod 750 /start.sh
CMD ["/setup.sh"]

EXPOSE 8888        