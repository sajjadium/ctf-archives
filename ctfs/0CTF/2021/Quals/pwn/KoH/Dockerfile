FROM httpd:2.4.48

RUN apt update && apt -y dist-upgrade

COPY mod_xss.so /usr/local/apache2/modules/
COPY server.key /usr/local/apache2/conf/
COPY server.crt /usr/local/apache2/conf/
COPY httpd.conf /usr/local/apache2/conf/
COPY httpd-mpm.conf /usr/local/apache2/conf/extra/
COPY httpd-ssl.conf /usr/local/apache2/conf/extra/
COPY html /usr/local/apache2/htdocs/
RUN rm /usr/local/apache2/htdocs/index.html
RUN chmod o-x /bin/* /sbin/* /usr/bin/* /usr/sbin/* /usr/local/bin/* /usr/local/apache2/bin/*

RUN useradd -m ctf
WORKDIR /home/ctf
COPY flag /home/ctf/
COPY readflag /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod 740 /home/ctf/flag && \
    chmod 2755 /home/ctf/readflag

WORKDIR /usr/local/apache2
