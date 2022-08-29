# Ruby AND node :^)
FROM timbru31/ruby-node:3.1-slim-14

RUN apt update
RUN apt install coreutils

# Create node directory
WORKDIR /usr/src/vienelibrary/vieneclient

# env values
ENV PORT_NODE=8080

# Install rest of the packages
COPY vieneclient/package*.json ./
RUN npm install

# App src
COPY vieneclient/ .

# Expose port
EXPOSE 8080

ENV BUNDLER_VERSION=2.1.4
WORKDIR /usr/src/vienelibrary/vieneserver
COPY vieneserver/Gemfile /usr/src/vienelibrary/vieneserver/Gemfile
COPY vieneserver/Gemfile.lock /usr/src/vienelibrary/vieneserver/Gemfile.lock
COPY vieneserver/ .
RUN apt update
RUN apt install -y build-essential openssl curl git-core zlib1g zlib1g-dev libssl-dev libyaml-dev libxml2-dev autoconf libtool

RUN bundle install

ENV PORT_RUBY=3000
RUN chmod -R 555 /usr/src/vienelibrary/vieneserver
RUN chmod -R 557 /usr/src/vienelibrary/vieneserver/log
RUN chmod -R 557 /usr/src/vienelibrary/vieneserver/tmp

# Start
WORKDIR /
COPY run.sh .
RUN chmod +x run.sh

# User
RUN addgroup --system ctf && adduser --system --group ctf
RUN chmod -R 775 /usr/src/vienelibrary/vieneserver
USER ctf:ctf

CMD [ "/run.sh"]