FROM mcr.microsoft.com/playwright:focal
ARG DEBIAN_FRONTEND=noninteractive

# build wiby via instructions from http://wiby.me/about/guide.html
# note: the build is "standard", and is not important for solving the challenge. there is no (intentional) bug within the build itself
# relevant changes are marked with !!! comments
RUN apt-get update && apt-get install -y  \
  nginx \
  mysql-server \
  php-fpm \
  php-mysql \
  php-gd \
  build-essential \
  libcurl4-openssl-dev \
  libmysqlclient-dev \
  golang \
  git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN git clone https://github.com/wibyweb/wiby.git

ENV FLAG1="uiuctf{this_isnt"
ENV FLAG2="_the_real_flag!}"
ENV ADMIN_PASSWORD="not_real_admin_password"

# minor modifications
RUN find ./ -type f -exec sed -i -e "s/'localhost'/'127.0.0.1'/g" {} \; && \
  find ./ -type f -exec sed -i -e 's/"localhost"/"127.0.0.1"/g' {} \; && \
  find ./ -type f -exec sed -i -e 's/>name</>woeby</gi' {} \;

# build binaries
RUN cd wiby/c && \
  gcc cr.c -o cr -I/usr/include/mysql -lmysqlclient -lcurl -std=c99 -O3 && \
  gcc rs.c -o rs -I/usr/include/mysql -lmysqlclient -std=c99 -O3 && \
  gcc rt.c -o rt -I/usr/include/mysql -lmysqlclient -std=c99 -O3
RUN cd wiby/go/core && \
  go mod init core && \
  go get -u github.com/go-sql-driver/mysql@latest && \
  sed -i 's/0.0.0.0/127.0.0.1/g' 1core.go && \
  go build 1core.go

# nginx configuration, head cmd is to get rid of https block
RUN mkdir /etc/nginx/phpcache /etc/nginx/cache && \
  sed 's/server_name[^;]*;/server_name woeby.chal.uiuc.tf;/g;s/return 301/#return 301/g' wiby/etc/nginx/sites-available/default_example | head -n 148 > /etc/nginx/sites-available/default

# mysql configuration
RUN printf '\n\n[client]\ndefault-character-set=utf8mb4\n\n[mysql]\ndefault-character-set = utf8mb4\n\n[mysqld]\nmax_connections = 2000\nft_min_word_len=2\nsql_mode = "NO_BACKSLASH_ESCAPES"\ncharacter-set-server = utf8mb4\ncollation-server = utf8mb4_0900_ai_ci\nskip-character-set-client-handshake\ndefault-authentication-plugin=mysql_native_password\nwait_timeout = 800\n\n#memory use settings, you should adjust this based on your hardware\ninnodb_buffer_pool_size = 1342177280\ninnodb_buffer_pool_instances = 2' >> /etc/mysql/my.cnf && \
  service mysql start && \
  mysql -u root -e "create database wiby; create database wibytemp;" && \
  mysql -u root wiby < wiby/db/wiby.sql && \
  mysql -u root wibytemp < wiby/db/wibytemp.sql &&  \
  mysql -u root -e "create user 'guest'@'localhost' identified by 'qwer'; create user 'approver'@'localhost' identified by 'foobar'; create user 'crawler'@'localhost' identified by 'seekout'; use wiby; grant select on accounts to 'approver'@'localhost'; grant select on reviewqueue to 'approver'@'localhost'; grant insert on indexqueue to 'approver'@'localhost'; grant delete on reviewqueue to 'approver'@'localhost'; grant update on reviewqueue to 'approver'@'localhost'; grant select on indexqueue to 'crawler'@'localhost'; grant insert on windex to 'crawler'@'localhost'; grant insert on indexqueue to 'crawler'@'localhost'; grant update on windex to 'crawler'@'localhost'; grant delete on indexqueue to 'crawler'@'localhost'; grant delete on windex to 'crawler'@'localhost'; grant select on windex to 'crawler'@'localhost'; grant insert on reviewqueue to 'crawler'@'localhost'; grant select on windex to 'guest'@'localhost'; grant insert on reviewqueue to 'guest'@'localhost'; grant insert on feedback to 'guest'@'localhost'; grant select on feedback to 'approver'@'localhost'; grant delete on feedback to 'approver'@'localhost'; grant insert on graveyard to 'approver'@'localhost'; grant update on graveyard to 'approver'@'localhost'; grant delete on graveyard to 'approver'@'localhost'; grant select on graveyard to 'approver'@'localhost'; grant update on accounts to 'approver'@'localhost'; grant insert on accounts to 'approver'@'localhost'; grant delete on accounts to 'approver'@'localhost'; use wibytemp; grant select on titlecheck to 'crawler'@'localhost'; grant insert on titlecheck to 'crawler'@'localhost'; grant delete on titlecheck to 'crawler'@'localhost'; grant select on rejected to 'approver'@'localhost'; grant insert on rejected to 'approver'@'localhost'; grant delete on rejected to 'approver'@'localhost'; grant select on reserve_id to 'crawler'@'localhost'; grant insert on reserve_id to 'crawler'@'localhost'; grant delete on reserve_id to 'crawler'@'localhost'; FLUSH PRIVILEGES;" && \
  mysql -u root wiby -e "INSERT INTO accounts (name, hash, level) VALUES ('admin','`php -r 'echo password_hash(getenv("ADMIN_PASSWORD"), PASSWORD_DEFAULT);'`', 'admin');" && \
  # !!! FLAGS ADDED HERE !!!
  mysql -u root wiby -e "INSERT INTO windex (url,title,description,body,http,surprise,worksafe,enable,updatable,approver) VALUES ('https://www.youtube.com/watch?v=dQw4w9WgXcQ','flag','flag','flag',0,1,1,1,1,'admin');" && \
  mysql -u root wiby -e "create table flag1 (flag text); insert into flag1 values ('$FLAG1'); grant select on flag1 to 'approver'@'localhost';" && \
  mysql -u root wiby -e "create table flag2 (flag text); insert into flag2 values ('$FLAG2'); grant select on flag2 to 'crawler'@'localhost';"

# !!! we add an admin bot to review your submitted urls !!!
COPY bot.js /tmp/bot.js
RUN npm i playwright-chromium && \
  printf "\nenv[PLAYWRIGHT_BROWSERS_PATH] = /ms-playwright\nenv[ADMIN_PASSWORD] = $ADMIN_PASSWORD\n" >> /etc/php/7.4/fpm/php-fpm.conf && \
  sed -i 's/\$output.*$/$output = "Thank you for submitting \$url. An admin will review it shortly."; exec("node \/tmp\/bot.js > \/dev\/null 2>\&1 \&");/g' wiby/html/submit/index.php && \
  rm -r wiby/html/hash/ && \
  mv wiby/html/* /var/www/html/

# start services!
CMD service nginx start && service mysql start && service php7.4-fpm start && cd wiby/c && (./rs & ./cr &) && cd ../go/core && echo "running..." && ./1core
