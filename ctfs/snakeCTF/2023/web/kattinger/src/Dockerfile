FROM ruby:3.0.6-bullseye

RUN gem install bundler:2.4.13

WORKDIR /usr/src/app


COPY . .
RUN bundle install

COPY flag /flag

EXPOSE 3000

RUN adduser ctf
RUN chmod -R 777 /usr/src/app/Gemfile.lock /usr/src/app/log /usr/src/app/db /usr/src/app/tmp
USER ctf

ENTRYPOINT ["./bin/rails","server", "-b", "0.0.0.0"]
