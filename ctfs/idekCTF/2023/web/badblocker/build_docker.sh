docker kill badblocker
docker rm badblocker
docker build . -t badblocker
docker run -p 1337:1337 -it --name=badblocker badblocker