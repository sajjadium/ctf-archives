FROM httpd:2.4

# Remove all the default stuff, allow SSI and htaccess
RUN rm /usr/local/apache2/htdocs/* \
  && rm /usr/local/apache2/cgi-bin/* \
  && apt-get update \
  && apt-get install -y cpanminus \
  && rm -rf /var/lib/apt/lists/* \
  && cpanm CGI::Minimal \
  && sed -i 's/AllowOverride None/AllowOverride All/g' /usr/local/apache2/conf/httpd.conf \
  && sed -i '/LoadModule include_module/s/^#//g' /usr/local/apache2/conf/httpd.conf

# Add our wonderful secure app :)
COPY ./cgi-bin /usr/local/apache2/cgi-bin/
COPY ./htdocs /usr/local/apache2/htdocs/
COPY ./flag.txt /flag.txt

# Allow CGI scripts to run
RUN chmod +x /usr/local/apache2/cgi-bin/*
 
CMD httpd-foreground \
  -c "LoadModule cgid_module modules/mod_cgid.so"
