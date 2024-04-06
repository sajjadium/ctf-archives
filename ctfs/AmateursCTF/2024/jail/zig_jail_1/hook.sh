#!/bin/sh

# zig needs a pts for some reason

chroot /srv /app/chroot.sh

echo 'mount: {
  dst: "/dev/pts"
  fstype: "devpts"
  nosuid: true
  noexec: true
  options: "newinstance"
}
' >> /tmp/nsjail.cfg