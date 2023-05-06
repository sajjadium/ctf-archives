# Build

```
docker compose build
```

# Confirm Docker Image

```
docker images
```

Should see something like:

```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
zombie-101   1         13f4a862e467   7 minutes ago    275MB
```

# Run Image Locally

Assumes no process is already listening on port 80.

```
docker compose up
```

Should see something like:

```
[+] Running 1/0
 ⠿ Container zombie-101  Recreated                                                                                                                                                                                  0.1s
Attaching to zombie-101
zombie-101  | Running on 80
```
