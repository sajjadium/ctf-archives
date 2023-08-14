FROM mono:6.12.0.107

RUN apt update && apt install -y python3 mono-fastcgi-server nginx
COPY PagelessNotebook /app/
COPY nginx/default /etc/nginx/sites-available/default
COPY nginx/fastcgi_params /etc/nginx/fastcgi_params
COPY flag.txt /tmp/
COPY wrapper.sh /tmp/
RUN adduser appuser

EXPOSE 80
CMD [ "/tmp/wrapper.sh" ]