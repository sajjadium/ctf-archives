FROM node:latest

COPY app /www
WORKDIR /www

RUN npm install
RUN echo "hitcon{REDACTED}" > "/flag-$(head -c 32 /dev/random | sha1sum | cut -d ' ' -f 1 | tr -d '\n')"

ARG AUTO_DESTROY
ENV AUTO_DESTROY=$AUTO_DESTROY
CMD ["bash", "-c", "timeout $(($AUTO_DESTROY*60)) node app.js"]

