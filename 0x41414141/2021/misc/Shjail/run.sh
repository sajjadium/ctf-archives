docker build -t shjail .
docker run -it --rm -p 9998:9998 -p 4545:4545 --name shjail shjail
