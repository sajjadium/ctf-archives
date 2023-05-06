Run the following commands to set up the environment:
1. `docker build -t d3fuse_env .`
2. `docker run -d --rm --privileged -p 9999:9999 d3fuse_env`
2. `nc 127.0.0.1 9999`

