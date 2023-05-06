# Deployment

## go to /waf

```
docker build -t waf .
docker run -d -p 5555:5555 waf
```

## go to /app

```
docker build -t app .
docker run -d -p 8088:8088 app
```

## challenge @ http://localhost:8088/
