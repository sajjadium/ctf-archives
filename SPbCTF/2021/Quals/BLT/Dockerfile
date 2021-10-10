FROM httpd:latest

COPY flag.txt /flag.txt

RUN echo "<VirtualHost *:80>\n \
DocumentRoot /var/www/html/\n \
<Directory \"/\">\n \
 Require all granted\n \
</Directory>\n \
</VirtualHost>" > /usr/local/apache2/conf/apache.conf

RUN echo "Include /usr/local/apache2/conf/apache.conf" >> /usr/local/apache2/conf/httpd.conf
