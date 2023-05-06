# build/
The build directory contains all the files you need (except the linux kernel source) to create your own local setup for testing.  

## Cloning the repo and applying the patch

```bash
cd build/
git clone https://github.com/torvalds/linux/
cd linux
git checkout eb7081409f94a9a8608593d0fb63a1aa3d6f95d8
git apply ../sys_jail.patch
```

## Compiling the kernel

```bash
make menuconfig  # You don't need to configure anything. Just leave the default there and exit. This should create a .config file.
make bzImage -j $(nproc)
# You might need to set 
# CONFIG_SYSTEM_TRUSTED_KEYS="", CONFIG_SYSTEM_REVOCATION_KEYS="",  
# CONFIG_DEBUG_INFO_BTF=n
# in your .config if there is no bzImage in arch/x86/boot/ after the make and rerun the command above.
cp arch/x86/boot/bzImage ../
```

## Launching
You can modify the used filesystem by modifying files in the ``fs/`` directory and running ``./rebuild_fs.sh`` afterwards.  
``./launch.sh`` will invoke qemu with the built kernel and the filesystem.  
``./go.sh`` is just a shortcut for ``./rebuild_fs.sh`` and ``./launch.sh``.


# deploy/
The deploy directory contains the complete remote setup (flag.txt in initramfs.cpio.gz is different on the server of course).  
The kernel was built from commit eb7081409f94a9a8608593d0fb63a1aa3d6f95d8 and with the patch applied.

