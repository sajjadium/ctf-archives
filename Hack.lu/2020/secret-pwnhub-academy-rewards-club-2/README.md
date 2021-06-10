# Secret Pwnhub Academy Rewards Club
The docker container will expose the challenge on local port 4444.

To build the initial image, use: `./build_docker.sh`

## Challenge Setup
To connect to the original challenge, simply connect like the following:

```
# 1. Start docker
./start_docker.sh
# 2. Connect to Service
nc localhost 4444
```

## Debug Setup
To debug the target, you can use `./run_docker_gdbserver.sh` similarly

```
# 1. Start docker, exposing gdb server and waiting for connection.
./run_docker_gdbserver.sh
# 2. Connect to service from another shell and you will get gdb on the first one
nc localhost 4444
```