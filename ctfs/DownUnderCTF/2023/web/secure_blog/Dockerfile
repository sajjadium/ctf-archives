FROM python:3.10-slim-bullseye


##
# Install dependencies
## 
RUN apt update && \
    apt install -y  --no-install-recommends \
    python3-dev default-libmysqlclient-dev pkg-config nginx supervisor build-essential lsb-release netcat

##
# Install dependencies for Django App
##
RUN mkdir -p /djangoapp
COPY ./djangoapp/requirements.txt /djangoapp/requirements.txt
RUN pip install -r /djangoapp/requirements.txt && \
    apt -y purge build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

##
# Configure Supervisor and Nginx
##
COPY configs/supervisord.conf /etc/supervisord.conf
COPY configs/nginx.conf /etc/nginx/sites-enabled/default

##
# Copy Django app and collect static
##
COPY ./djangoapp/ /djangoapp
RUN chmod +x /djangoapp/start_django.sh && \
    python3 /djangoapp/manage.py collectstatic

##
# Copy static files
##
COPY ./html/ /var/www/html

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]