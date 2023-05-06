# ctf_xinetd

> A docker repository for deploying CTF challenges

## Configuration

Put files to floder `bin`. They'll be copied to /home/ctf. **Update the flag** at the same time.

Edit `ctf.xinetd`. replace `./helloworld` to your command.

You can also edit `Dockerfile, ctf.xinetd, start.sh` to custom your environment.

## Build

```bash
docker build -t "speed_game" .
```

DO NOT use *bin* as challenge's name

## Run

```bash
docker run -d -p "0.0.0.0:pub_port:9999" -h "speed_game" --name="speed_game" speed_game
```

`pub_port` is the port you want to expose to the public network.


