Heap notes have become very repitive :(
How about adding a few layers of abstraction fun in between :D


# Remote instance
 - Docker container w/ ubuntu:22.04
 - Solve PoW and provide download link to exploit (can be archive)

# Compile QEMU
 - git clone -b stable-8.2 --depth=5 https://github.com/qemu/qemu.git
 - git checkout f48c205fb42be48e2e47b7e1cd9a2802e5ca17b0
 - git apply virtio-note.diff
 - mkdir build; cd build
 - ../configure --target-list=x86_64-softmmu --disable-xen --disable-spice --static --enable-seccomp
 - make

# For module compilation (if needed)
 - git clone -b v6.7.2 --depth=20 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
 - git checkout 7bbf3b67cb49d0f8a20e64b7473923041b758211
 - make defconfig
 - make prepare
 - make modules_prepare
 - make
