FROM alpine:latest

#install packages
COPY app/ /app/
RUN apk --no-cache add uwsgi-python3 nginx py-pip py3-pillow
RUN pip install -r /app/requirements.txt
RUN cp /app/web/nginx-site.conf /etc/nginx/http.d/default.conf

#configure permissions
RUN chown -R nginx:nginx /app/web/static/uploads
RUN chown -R nginx:nginx /app/web/whitelist.db
RUN chown -R nginx:nginx /app/web/
RUN chmod 755 /app/web/static/uploads
RUN chmod 750 /app/web/whitelist.db

#run services
RUN chmod 700 /app/ctrl/start-services.sh
CMD /app/ctrl/start-services.sh
