FROM redpwn/jail

# Ensure that it's Ubuntu 20
COPY --from=ubuntu:20.04 / /srv
COPY ./vuln /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_CONNS_PER_IP 1
ENV JAIL_MEM 20M