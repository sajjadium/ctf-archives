# echo 'hxp{FLAG}' > flag.txt && docker build -t hackme . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined  -ti -p 8080:80 hackme

# I really wanted to run this using their default image (FROM nabo.codimd.dev/hackmdio/hackmd:2.2.0).
# Unfortunately, they are still shipping jQuery 3.4.1 and some other stuff with published XSS CVEs.
# Instead, we have to clone their deployment process from
#   https://github.com/hackmdio/codimd/blob/master/deployments/{Dockerfile,build.sh}
# This should be identical to the 2.2.0 docker, but with fixed vulnerabilities in the dependencies.
# I'm sure I'm breaking some features here, but it still worked in our tests.
# Most of the ugliness comes from `npm audit`, and from a forced upgrade of `serialize-javascript`.
FROM hackmdio/buildpack:node-10-0baafb79 as BUILD
USER hackmd
RUN rmdir /home/hackmd/app && \
    cd / && \
    git clone https://github.com/hackmdio/codimd.git /home/hackmd/app && \
    cd /home/hackmd/app && \
    git checkout master
RUN npm install

RUN set -xe && \
    npm audit fix && \
    npm install helmet@4.2.0 && \
    npm update dot-prop --depth 7 && \
    npm update acorn --depth 4 && \
    npm update yargs-parser --depth 3 && \
    rm -rf node_modules/serialize-javascript && \
    sed -i -e 's/"serialize-javascript": "^.*"/"serialize-javascript": "^3.1.0"/' node_modules/uglifyjs-webpack-plugin/package.json node_modules/copy-webpack-plugin/package.json && \
    sed -i -En '$!N; /("serialize-javascript":\s+\{\s+"version": )"1.9.1"/{N;N;N;N;d} ; P ; D' package-lock.json && \
    npm cache clear --force && \
    npm install serialize-javascript@3.1.0 --no-save

RUN npm run build && \
    cp ./deployments/docker-entrypoint.sh ./ && \
    cp .sequelizerc.example .sequelizerc && \
    rm -rf .git .gitignore .travis.yml .dockerignore .editorconfig \
        .babelrc .mailmap .sequelizerc.example \
        test docs contribute \
        package-lock.json webpack.prod.js webpack.htmlexport.js webpack.dev.js webpack.common.js \
        config.json.example README.md CONTRIBUTING.md AUTHORS node_modules

FROM hackmdio/runtime:node-10-d27854ef
USER hackmd
WORKDIR /home/hackmd/app
COPY --chown=1500:1500 --from=BUILD /home/hackmd/app .
RUN npm install --production && \
    npm audit fix && \
    npm cache clean --force && \
    rm -rf /tmp/{core-js-banners,phantomjs}
# This is the end of the codimd Dockerfile.

# Database and reporting dependencies
USER root
RUN apt-get update && \
    < /dev/urandom tr -dc _A-Z-a-z0-9 | head -c32 > /root/mysql-password.txt && \
    echo "mariadb-server mysql-server/root_password password $(cat /root/mysql-password.txt)" | debconf-set-selections && \
    echo "mariadb-server mysql-server/root_password_again password $(cat /root/mysql-password.txt)" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        nginx \
        mariadb-server \
        python3-selenium \
        chromium-driver \
        uuid-runtime \
    && rm -rf /var/lib/apt/lists/

# Copy things we'll always need
COPY ynetd /sbin/
COPY docker-stuff/default /etc/nginx/sites-enabled/default
COPY docker-stuff/db.sql /root/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY admin.py /home/ctf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Set up entrypoint
COPY entrypoint.sh /sbin/

# Set up database
COPY setup.sql flag.txt /root/

WORKDIR /home/hackmd/app
RUN < /dev/urandom tr -dc _A-Z-a-z0-9 | head -c32 > /root/admin-password.txt && \
    node -e "let Scrypt = require('scrypt-kdf'); Scrypt.kdf('$(cat /root/admin-password.txt)', Scrypt.pickParams(0.1)).then(hash => {console.log(hash.toString('hex'))});" > /root/admin-password-hash.txt
    # NB: This is the same password hashing code that HackMD uses, don't blame me
WORKDIR /root

RUN mysqld_safe & \
    while ! mysqladmin --silent ping; do sleep 0.1; done && \
    mysql -u root -p$(cat /root/mysql-password.txt) < /root/db.sql && \
    replace "__DB_PASSWORD__" "$(< /dev/urandom tr -dc _A-Z-a-z0-9 | head -c32)" -- /root/setup.sql /sbin/entrypoint.sh && \
    replace "__ADMIN_EMAIL__" "$(< /dev/urandom tr -dc A-Za-z0-9 | head -c32)@hackme.2020.ctf.link" -- /home/ctf/admin.py /root/setup.sql && \
    replace "__ADMIN_PASSWORD__" "$(cat /root/admin-password.txt)" -- /home/ctf/admin.py && \
    replace "__ADMIN_PASSWORD_HASH__" "$(cat /root/admin-password-hash.txt)" -- /root/setup.sql && \
    replace "__FLAG__" "$(cat /root/flag.txt)" -- /root/setup.sql && \
    replace "__ADMIN_UUID__" "$(uuidgen)" -- /root/setup.sql && \
    replace "__ADMIN_DELETE_UUID__" "$(uuidgen)" -- /root/setup.sql && \
    replace "__NOTE_UUID__" "$(uuidgen)" -- /root/setup.sql && \
    replace "__REVISION_UUID__" "$(uuidgen)" -- /root/setup.sql && \
    mysql -u root -p$(cat /root/mysql-password.txt) < /root/setup.sql && \
    shred -fu /root/*

# Fix permissions
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 444 /etc/nginx/sites-enabled/default && \
    chmod 005 /home/ctf/admin.py && \
    chmod 500 /sbin/entrypoint.sh

# Launch everything
EXPOSE 80
ENTRYPOINT /sbin/entrypoint.sh
