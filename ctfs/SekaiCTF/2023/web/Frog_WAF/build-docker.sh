docker build -t sekai_web_waffrog .
docker run  --name=sekai_web_waffrog --rm -p1337:1337 -it sekai_web_waffrog