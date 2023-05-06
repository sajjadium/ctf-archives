# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM gcr.io/kctf-docker/challenge@sha256:56f7dddff69d08d4d19f4921c724d438cf4d59e434c601f9776fd818368b7107


RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
       curl ca-certificates gnupg lsb-release software-properties-common

RUN curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
    && (echo "deb https://deb.nodesource.com/node_14.x $(lsb_release -s -c) main";\
        echo "deb-src https://deb.nodesource.com/node_14.x $(lsb_release -s -c) main") \
       > /etc/apt/sources.list.d/nodesource.list \
    && add-apt-repository universe

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
       php7.4 php7.4-bcmath php7.4-fpm php7.4-gmp php7.4-sqlite3 php7.4-mysql php7.4-xml php7.4-mbstring php7.4-zip php7.4-curl \
       nginx composer nodejs git unzip mysql-client

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*


COPY nginx-site.conf /etc/nginx/sites-available/paymeflare
RUN ln -s /etc/nginx/sites-available/paymeflare /etc/nginx/sites-enabled/paymeflare
RUN rm /etc/nginx/sites-enabled/default

RUN echo "clear_env = no" >> /etc/php/7.4/fpm/pool.d/www.conf

VOLUME /tmp
VOLUME /var/lib/nginx
VOLUME /var/log
VOLUME /var/log/nginx
VOLUME /run
VOLUME /run/php
VOLUME /lv/storage
VOLUME /lv/resources/views
VOLUME /lv/bootstrap/cache
VOLUME /root/.config

COPY src /lv
RUN chown -R www-data:www-data /lv/storage
WORKDIR /lv
RUN composer install --optimize-autoloader --no-dev
RUN php artisan view:cache
RUN npm install --production
RUN npm run prod

copy ./start.sh /tmp    

CMD kctf_setup && /tmp/start.sh

