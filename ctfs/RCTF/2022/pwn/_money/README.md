# ctf_xinetd

> A docker repository for deploying CTF challenges

## Configuration

Put files to floder `bin`. They'll be copied to /home/ctf. **Update the flag** at the same time.

Edit `ctf.xinetd`. replace `./helloworld` to your command.

You can also edit `Dockerfile, ctf.xinetd, start.sh` to custom your environment.

## Build

```bash
docker build -t "helloworld" .
```

DO NOT use *bin* as challenge's name

## Run

```bash
docker run -d -p "0.0.0.0:pub_port:9999" -h "helloworld" --name="helloworld" helloworld
```

`pub_port` is the port you want to expose to the public network.

## Capture traffic

If you want to capture challenge traffic, just run `tcpdump` on the host. Here is an example.

```bash
tcpdump -w helloworld.pcap -i eth0 port pub_port
```
