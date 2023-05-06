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
REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
hidden-css        1         83cbce6baae1   17 minutes ago   405MB
```

# Run Image Locally

Assumes no process is already listening on port 80.

```
docker compose up
```

Should see something like:

```
[+] Running 1/0
 ⠿ Container hidden-css  Created                                                                                                                          0.0s
Attaching to hidden-css
```
