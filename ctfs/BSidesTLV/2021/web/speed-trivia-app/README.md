# Speed Trivia 

## how to run:

```
docker-compose up
```

The app will be available at http://localhost:3000



## Env vars
The docker container starts with the following Environment variables:
 * ``REDIS_HOST``: host address of the redis DB the web-app backend will connect to (default is _localhost_)
 * ``REDIS_PORT``: Redis DB port (default is 6379)
 * ``JWT_SECRET``: JWT secret
 * ``ANALYTICS_LIMIT``: How many analytics event a client can send in one request
 * ``DEFAULT_TTL``: Time (in seconds) for a single game session
 * ``FLAG``: flag content

