FROM alpine AS chroot
#    ^- musl is required

RUN addgroup -g 1337 ctf && adduser -S -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

COPY files/mkleak /home/ctf
COPY files/flag.txt /home/ctf

FROM ghcr.io/google/nsjail/nsjail:latest

COPY --from=chroot / /chroot

CMD nsjail --disable_clone_newcgroup --port 1337 --chroot /chroot --user 1337 --group 1337 --cwd /home/ctf/ --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf /home/ctf/mkleak
