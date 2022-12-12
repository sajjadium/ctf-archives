# PrettierOnline

Build:
Change `YOUR_TMP_PATH_HERE` in `docker-compose.yml` first, it should be absolute path.
Do not set to `/tmp` if using systemd or Docker for Mac, use the value of `TMPDIR` environment variable instead.

```bash
cd prettier && docker build . -t prettieronline
cd ..
docker-compose up
```
