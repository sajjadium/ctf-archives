docker build -t nightmare .
docker run --rm -it --net=host --privileged -v $(pwd):/pwn $(docker build -q .)