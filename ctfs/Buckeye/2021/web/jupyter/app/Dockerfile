FROM python:3-slim
RUN pip install notebook fastapi uvicorn python-multipart requests
RUN apt-get update
RUN apt-get -y install nginx xxd
RUN useradd -m ctf
WORKDIR /home/ctf
COPY . ./
RUN rm -rf /var/www/html && \
mv static/ /var/www/html && \
mv nginx.conf /etc/nginx/nginx.conf
CMD timeout 300 /home/ctf/run.sh
