1. 
```bash
docker build -t "picstore" .
```

2. 
```bash
docker run -d -p "0.0.0.0:3498:8888" -h "re_picstore" --name="re_picstore" re_picstore 
```

`pub_port` Replace with the port you want to open to players

