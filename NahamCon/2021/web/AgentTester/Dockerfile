FROM python:3.8-slim

RUN apt update -y && apt install -y gcc libssl-dev nodejs npm nginx curl
RUN apt-get -y install chromium\
    chromium-l10n \
    fonts-liberation \
    fonts-roboto \
    hicolor-icon-theme \
    libcanberra-gtk-module \
    libexif-dev \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libpangox-1.0-0 \
    libv4l-0 \
    fonts-symbola \
    --no-install-recommends

WORKDIR /app

COPY app/ .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN echo -e "uwsgi\nuwsgi" | adduser uwsgi

RUN chmod -R 777 /app/backend/DB

WORKDIR /app/browser

# Install puppeteer so it's available in the container.
RUN npm i puppeteer

WORKDIR /app

RUN rm /etc/nginx/sites-enabled/default

# Replace with our own nginx.conf
COPY ./nginx.conf /etc/nginx/sites-enabled/

ADD ./run.sh /root
RUN chmod +x /root/run.sh

ENV BASE_URL "<REDACTED>"
EXPOSE 80
CMD ["/root/run.sh"]
