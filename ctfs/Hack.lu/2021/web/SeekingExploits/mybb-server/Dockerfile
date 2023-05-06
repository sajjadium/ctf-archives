FROM ubuntu:20.10

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# download mybb
WORKDIR /var/www/html
RUN apt update && apt install -y unzip apache2 php curl python3 python3-requests python3-pymysql
RUN apt install -y libapache2-mod-php php-xml php-mysqli php-gd
RUN a2enmod rewrite
RUN curl https://resources.mybb.com/downloads/mybb_1829.zip -o mybb_1829.zip
RUN unzip mybb_1829.zip && rm mybb_1829.zip && cp -r Upload/** .
RUN rm -rf Upload Documentation
RUN chown -R www-data .
RUN rm index.html

# install the integration plugin
COPY ./exploit_market/emarket-api.php .
COPY ./exploit_market/inc/plugins/emarket.php ./inc/plugins/
RUN mkdir /opt/emarket-data/ && chown www-data /opt/emarket-data/

# deny all requests until the installer finished!
COPY .htaccess .htaccess
COPY apache2.conf /etc/apache2/

# prepare the installation scripts
COPY install.py /opt/installer/install.py

# install mybb, the installer handles the rest
ENTRYPOINT service apache2 start && python3 /opt/installer/install.py
