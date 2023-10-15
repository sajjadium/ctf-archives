Unfortunately, your future looks very bleak. Even the fortune teller was scared off. Also they took the flag with them.
Hint: Executing code from /dev/urandom like it's 1990 is a good start.


# Misfortune Box

The setup for this is essentially the same as a for _Fortune Box_.

You can grab QEMU for this architecture at [https://github.com/img-meta/qemu](https://github.com/img-meta/qemu). We disabled most of the features that are annoying to build:

    ./configure --target-list=meta-softmmu \
                --disable-debug-tcg --disable-sparse --disable-sdl --disable-virtfs \
                --disable-vnc --disable-cocoa --disable-xen --disable-xen-pci-passthrough \
                --disable-brlapi --disable-vnc-tls --disable-vnc-sasl --disable-vnc-jpeg \
                --disable-vnc-png --disable-curses --disable-curl --disable-fdt \
                --disable-bluez --disable-slirp --disable-kvm --disable-nptl --disable-vde \
                --disable-blobs --disable-docs --disable-vhost-net --disable-spice \
                --disable-libiscsi --disable-smartcard --disable-smartcard-nss \
                --disable-usb-redir --disable-guest-agent --disable-glusterfs
    make -j

Unfortunately, the build system is quite old, so you may need to fix a few things.

The flag is in `/flag`, on the host.
