from ubuntu:18.04

# example:
run apt-get -qq update && apt-get install -qq --no-install-recommends xinetd rsyslog default-jre python3 locales sudo python lua5.2 \
	nodejs npm ocaml-nox emacs-nox
# python3-pip, etc.

# Install patched node
copy node-patched /usr/bin/node

# install npm module
run npm install -g bytenode

# install new ruby

run mkdir /ruby2.7 && chmod 755 /ruby2.7
ADD ruby-2.7.0.tar.bz2 /ruby2.7/

copy service.conf /service.conf
copy banner_fail /banner_fail
copy wrapper /wrapper

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Note: anything that goes in public_files must be pre-built and checked in git
copy src /root

# the deployment tester will pass in the flag from the yaml
ARG THE_FLAG="OOO{this is a test flag}"
RUN touch /flag && chmod 400 /flag && echo $THE_FLAG > /flag

expose 5000
#cmd chmod go-rwx /proc && /usr/sbin/xinetd -syslog local0 -dontfork -f /service.conf
cmd /usr/sbin/xinetd -syslog local0 -dontfork -f /service.conf
# ^^ If ps would be too revealing, replace with the line below.
#    AFAIK, this also disables the built-in printf(%n) protection, so YMMV.

