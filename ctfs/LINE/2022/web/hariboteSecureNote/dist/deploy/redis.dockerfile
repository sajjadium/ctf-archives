FROM redis:5
COPY ./deploy/conf/redis.conf /redis.conf
CMD ["redis-server", "/redis.conf"]