FROM php:8.1.18-apache-bullseye

RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN sed -i "s/Listen 80/Listen 8080/" /etc/apache2/ports.conf

RUN chmod -R 755 /etc/apache2 &&\
    chmod -R 755 /var/www/

COPY flag.txt /flag.txt
RUN chown admin:admin /flag.txt &&\
    chmod 440 /flag.txt

COPY make_abyss_entry /make_abyss_entry
RUN chown root:root /make_abyss_entry &&\
    chmod 111 /make_abyss_entry &&\
    chmod g+s /make_abyss_entry

COPY list_uploads /list_uploads
RUN chown admin:admin /list_uploads &&\
    chmod 111 /list_uploads &&\
    chmod g+s /list_uploads

COPY src /var/www/html

RUN mkdir /abyss &&\
    chown -R root:root /abyss &&\
    chmod -R 331 /abyss

RUN chown -R root:root /var/www/html &&\
    chmod -R 555 /var/www/html

RUN rm -rf /var/www/html/uploads

RUn mkdir /var/www/html/uploads &&\
    chmod -R 333 /var/www/html/uploads

RUN rm -f /bin/chmod /usr/bin/chmod /bin/chown /usr/bin/chown

USER ctf

EXPOSE 8080