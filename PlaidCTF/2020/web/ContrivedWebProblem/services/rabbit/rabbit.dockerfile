FROM rabbitmq:3.8-management

WORKDIR /ppp
ADD init.sh ./
RUN chmod +x ./init.sh

CMD ["./init.sh"]