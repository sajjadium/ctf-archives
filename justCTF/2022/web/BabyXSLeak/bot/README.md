
Just bot (google-chrome-stable), no bugs here.
You don't need to review this folder.

# Building/Running image locally
```
nix build .#defaultPackage.x86_64-linux
docker load < ./result
docker run --rm -it bot -url http://httpbin.org/ip
```
or 
```
docker build -t bot -f flake.nix .
docker run --rm -it bot -url http://httpbin.org/ip
```

# Building/Running app locally
```
nix build .#packages.x86_64-linux.app
./result/bin/bot -h
```