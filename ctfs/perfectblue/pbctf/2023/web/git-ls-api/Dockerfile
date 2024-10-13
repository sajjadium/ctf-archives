FROM ruby:3.1.1
WORKDIR /app
COPY src/Gemfile /app/Gemfile
COPY src/Gemfile.lock /app/Gemfile.lock
RUN bundle config set --local deployment 'true' && bundle install

COPY src/ /app/
COPY flag.txt /flag.txt
EXPOSE 3000
RUN useradd -ms /bin/bash git
RUN mkdir /app/tmp /app/log
RUN chown git:git /app/tmp /app/log

USER git

CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]