FROM node:18-alpine


RUN apk update && apk upgrade
RUN apk add chromium python3 py3-pip

WORKDIR /app/
RUN pip3 install flask gunicorn
ENV PUPPETEER_EXECUTABLE_PATH /usr/bin/chromium-browser

RUN PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true npm install puppeteer
COPY . /app/
EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 app:app


