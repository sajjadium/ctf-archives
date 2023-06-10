FROM pwn.red/jail

# copy / from <some image> to /srv
# ubuntu 22.04: https://hub.docker.com/layers/library/ubuntu/jammy-20230522/images/sha256-2fdb1cf4995abb74c035e5f520c0f3a46f12b3377a59e86ecca66d8606ad64f9?context=explore
COPY --from=ubuntu@sha256:2fdb1cf4995abb74c035e5f520c0f3a46f12b3377a59e86ecca66d8606ad64f9 / /srv

COPY chall/relocs /srv/app/rel
COPY run.sh /srv/app/run
COPY chall/flag_real.elf /srv/app/flag.elf
RUN chmod +x /srv/app/run
RUN chmod +x /srv/app/rel

ENV JAIL_TMP_SIZE=1M