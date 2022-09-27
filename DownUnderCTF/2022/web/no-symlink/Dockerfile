FROM ruby:3.0

WORKDIR /srv
COPY . /srv
RUN mkdir /srv/uploads
RUN chmod a+rw -R /srv/uploads
COPY flag /flag

RUN /usr/sbin/useradd --no-create-home -u 1000 ctf

RUN gem install sinatra \
  && gem install thin \
  && gem install erubis

USER ctf

CMD ruby app.rb
