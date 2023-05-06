FROM httpd:alpine

RUN apk add perl-cgi

ADD ./main.pl /usr/local/apache2/cgi-bin/main.pl
RUN chmod +x /usr/local/apache2/cgi-bin/main.pl

CMD httpd-foreground -c "LoadModule cgid_module modules/mod_cgid.so"