FROM httpd:2.4.49

RUN apt update && apt install libapache2-mod-security2 libapache2-mod-qos -y
RUN rm -rf /usr/share/modsecurity-crs/rules/*

ADD src /var/www
ADD conf/modsecurity.conf /etc/modsecurity/modsecurity.conf
ADD conf/waf.conf /usr/share/modsecurity-crs/rules/waf.conf
ADD conf/modsecurity_crs_21_protocol_anomalies.conf /usr/share/modsecurity-crs/rules/modsecurity_crs_21_protocol_anomalies.conf
ADD conf/httpd.conf /usr/local/apache2/conf/httpd.conf
