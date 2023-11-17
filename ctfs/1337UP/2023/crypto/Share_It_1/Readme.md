Check out my new cool platform for sharing your thoughts. I used my 1337 crypto skills to craft session tokens 🔐


# Crypto level 1 - 1337UP LIVE CTF 2023

This repo contains the code for the ShareIt 1 challenge made for the 1337UP LIVE CTF 2023.

## Challenge text

Check out my new cool platform for sharing your thoughts. I used my 1337 crypto skills to craft session tokens

## Build docker image

```bash
docker build -t share-it-1 .
```

## Run docker image

Replace `<PORT>` with the host port

```bash
docker run -dp <PORT>:5000 -e FLAG='FLAG{some_cool_ctf_flag}' share-it-1
```
