FROM mcr.microsoft.com/playwright:focal

RUN mkdir /app && mkdir /app/sessions && chmod 333 /app/sessions
WORKDIR /app
COPY package*.json .
RUN npm i

# Bundle app source
COPY *.js .
COPY *.html .

# For handout:
ENV FLAG=uiuctf{REDACTED}
ENV HCAPTCHA_SECRET=REDACTED
ENV SECRET=REDACTED
ENV NODE_ENV=production
# the below envvar is NOT set in prod, only for your testing purposes (to bypass hCaptcha)
ENV DEBUG=1

CMD mount -t tmpfs none /tmp && mount -t tmpfs none /app/sessions && node /app/server.js
