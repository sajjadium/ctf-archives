FROM debian:bullseye-20230411

RUN apt update -y --fix-missing
RUN apt -y upgrade
RUN apt install -y trafficserver &&\
    sed -i -e "s/CONFIG proxy.config.http.insert_client_ip INT 1/CONFIG proxy.config.http.insert_client_ip INT 2/" /etc/trafficserver/records.config &&\
    sed -i -e "s/CONFIG proxy.config.http.server_ports STRING 8080 8080:ipv6/CONFIG proxy.config.http.server_ports STRING 3000 3000:ipv6/" /etc/trafficserver/records.config
COPY remap.config /etc/trafficserver/remap.config
CMD bash -c "service trafficserver start; sleep infinity"
EXPOSE 3000
