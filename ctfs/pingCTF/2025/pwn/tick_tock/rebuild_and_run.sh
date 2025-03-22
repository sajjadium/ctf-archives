podman build  -t  tick-tock --platform linux/arm/v7 .

podman run -d -t --replace \
  --platform linux/arm/v7 \
  -p 20420:8080 \
  --name tick-tock\
  tick-tock