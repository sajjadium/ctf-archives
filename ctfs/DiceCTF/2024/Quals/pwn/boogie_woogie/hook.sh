#!/bin/sh
chroot /srv /app/chroot.sh
echo 'mount: {
  dst: "/dev/pts"
  fstype: "devpts"
  nosuid: true
  noexec: true
  options: "newinstance"
}' >> /tmp/nsjail.cfg
