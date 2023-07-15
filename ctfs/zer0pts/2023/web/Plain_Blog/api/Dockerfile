FROM ruby:3

WORKDIR /app
RUN gem install sinatra puma
COPY . .

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

ENV APP_ENV production

CMD [ "ruby", "./app.rb" ]