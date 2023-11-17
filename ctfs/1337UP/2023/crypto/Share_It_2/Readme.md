I heard some people were able to tamper with the IV, so I removed it from the cookie. I even did some debug testing and discovered that even if the IV could be modified it is not enough to set the admin attribute of the new tokens!


# Crypto level 2 - 1337UP LIVE CTF 2023

This repo contains the code for the ShareIt 2 challenge made for the 1337UP LIVE CTF 2023.

## Challenge text

I heard some people were able to tamper with the IV, so I removed it from the cookie. I even did some debug testing and discovered that even if the IV could be modified it is not enough to set the `admin` attribute of the new tokens!

## Build docker image

```bash
docker build -t share-it-2 .
```

## Run docker image

Replace `<PORT>` with the host port

```bash
docker run -dp <PORT>:5000 -e FLAG='FLAG{some_cool_ctf_flag}' share-it-2
```
