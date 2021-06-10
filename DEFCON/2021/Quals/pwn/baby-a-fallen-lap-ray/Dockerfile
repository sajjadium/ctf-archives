from --platform=linux/amd64 ubuntu:18.04

# example:
run apt-get -qq update && apt-get install -qq --no-install-recommends xinetd sudo
# python3-pip, etc.

copy schitzo /

RUN mkdir /service
copy sh /service
copy os /service
copy quit /service
copy vm /service
copy p /service
copy manchester /service

RUN chmod 644 /service/sh /service/os /service/vm /service/p && chmod 666 /service/quit && chmod 755 /service/manchester

# If desired, the deployment tester can pass in the flag from the yaml
ARG THE_FLAG="OOO{this is a test flag}"
RUN touch /service/flag && chmod 644 /service/flag && echo $THE_FLAG > /service/flag

copy service.conf /service.conf
copy banner_fail /banner_fail
copy wrapper /wrapper

expose 5000
cmd ["/usr/sbin/xinetd", "-filelog", "/dev/stderr", "-dontfork", "-f", "/service.conf"]
