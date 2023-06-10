FROM pwn.red/jail

# copy / from <some image> to /srv
# ubuntu 22.04: https://hub.docker.com/layers/library/ubuntu/jammy-20230522/images/sha256-2fdb1cf4995abb74c035e5f520c0f3a46f12b3377a59e86ecca66d8606ad64f9?context=explore
COPY --from=ubuntu@sha256:2fdb1cf4995abb74c035e5f520c0f3a46f12b3377a59e86ecca66d8606ad64f9 / /srv
COPY dist/server /srv/app/run
COPY flag.txt /srv/app/flag.txt