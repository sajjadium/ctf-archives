docker build -t bb .
docker run -it -d -p 12000:80 --name linectf_bb bb