FROM ubuntu:bionic

# example:
RUN apt-get -qq update && apt-get install -qq --no-install-recommends xinetd net-tools libglib2.0-0
# python3-pip, etc.

# Note: anything that goes in public_files must be pre-built and checked in git

# If desired, the deployment tester can pass in the flag from the yaml
ARG THE_FLAG="OOO{this is only a test flag, sorry}"
RUN touch /flag && chmod 644 /flag && echo $THE_FLAG > /flag

RUN md5sum /flag|cut -d " " -f1 > /lic

COPY service.conf /service.conf
COPY banner_fail /banner_fail
COPY wrapper /wrapper

COPY liccheck.bin /liccheck.bin

COPY qemooo /qemooo
COPY games /games

RUN /bin/bash -c 'for x in {1,2,3,4,5,6,7,8,9,a,b,c,d,e,f}; do printf "STRANGE GAME\nTHE ONLY WINNING MOVE IS\nNOT TO PLAY.\n" > /$x.mz; done'

EXPOSE 5000

CMD ["/usr/sbin/xinetd", "-filelog", "/dev/stderr", "-dontfork", "-f", "/service.conf"]
#CMD ["/usr/sbin/xinetd", "-syslog", "local0", "-dontfork", "-f", "/service.conf"]
# ^^ If ps would be too revealing, replace with the line below.
#    AFAIK, this also disables the built-in printf(%n) protection, so YMMV.
#cmd chmod go-rwx /proc && /usr/sbin/xinetd -filelog /dev/stderr -dontfork -f /service.conf
