# Wild DevTools

## Setup a local environment

1. Install Docker
2. Add `DEV=1` environment variable to the `screenshoter` service in `docker-compose.yaml` file.
3. Run `docker-compose up`
4. Once setup is complete, you may access the app at http://localhost

## Proof of work

**This have nothing to do with the challenge, we only use this as a rate limiting mechanism. Please work locally untill you are confident you have a working solution.**

Before making a request to the `/screenshot` in production you would have to solve a proof of work puzzle.

To get the puzzle make a GET request to `/screenshot` and extract the following response headers.

1. `X-PUZZLE` - 32 random bytes
2. `X-PUZZLE-EXPIRATION` - puzzle expiration in seconds
3. `X-DIFFICULTY` - the minimum number of leading zeros required

To solve the proof of work challenge, you would have to find 16 bytes that when appended to the puzzle and hashed using sha256 produce a hash that start with at least `X-DIFFICULTY` zeroes.

You do not need to implement this, use the `pow/pow.go` CLI.

```sh
$: go run pow.go <puzzle> <difficulty>
```

The `/pow` directory also contains a Dockerfile. If you like to use it from a Docker container, follow the steps below:

```sh
cd /pow
docker build . -t pow
docker run pow <puzzle> <difficulty>
```

Typically, finding the solution should take 10 to 30 seconds. Each solution can only be used once as long as the puzzle have not expire.

Once you have the solution make a GET request to `/screenshot` with the following headers:

1. `X-PUZZLE` - the puzzle you solved
2. `X-PROOF-OF-WORK` - the 16 bytes you found in hex format. (This is the output of `pow.go` script)

## SmokeScreen

**This service have nothing to do with the intended solution of the challenge.**

## Redis

**This service have nothing to do with the intended solution of the challenge.**
