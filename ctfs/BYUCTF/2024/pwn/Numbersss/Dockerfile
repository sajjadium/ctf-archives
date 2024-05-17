FROM ubuntu:23.04

# update
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y xinetd
RUN rm -rf /var/lib/apt/lists/*

# set up user
RUN mkdir /ctf
RUN useradd -M -d /ctf ctf

# import files
RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./src /ctf/

# set permissions
RUN chown -R root:ctf /ctf
RUN chmod -R 750 /ctf

# start
CMD ["/usr/sbin/xinetd", "-dontfork"]
EXPOSE 40000