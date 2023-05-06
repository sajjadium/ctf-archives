FROM mongo:latest

COPY start.sh /
RUN chmod 777 /start.sh
ENV password=fakepassword
EXPOSE 27017
ENTRYPOINT ["bash", "/start.sh" ]