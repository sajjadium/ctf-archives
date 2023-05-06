FROM mcr.microsoft.com/playwright:focal

RUN mkdir /app && mkdir /files
WORKDIR /app
COPY package*.json .
RUN npm i && npm i -g tcpslow

COPY start.sh .

COPY *.js .
COPY static static

ENV FLAG=uiuctf{REDACTED}
ENV HCAPTCHA_SECRET=REDACTED
ENV ADMIN_TOKEN=REDACTED
# Turn this on when testing locally to bypass hCaptcha
# ENV DEBUG=1
CMD mount -t tmpfs none /tmp && mount -t tmpfs none /files && ./start.sh
