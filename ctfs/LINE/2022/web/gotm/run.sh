docker build -t gotm .
docker run -it -d -p 11000:11000 --name linectf_gotm gotm
