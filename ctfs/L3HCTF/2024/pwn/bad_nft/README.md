# Deployment 

Download source

```shell
wget https://gitee.com/openeuler/kernel/repository/archive/5.10.0-153.37.0 -O openeuler-5.10.0-153.37.0.zip
unzip -q openeuler-5.10.0-153.37.0.zip
```

Patch the kernel and compile it

```shell
cd kernel-5.10.0-153.37.0
patch -p1 -i ../vuln.patch
cp ../config .config
make oldconfig
make
```

Local debugging
```
cp kernel-5.10.0-153.37.0/vmlinux .
cp kernel-5.10.0-153.37.0/arch/arm64/boot/Image .
./run.sh
```

You may need `libmnl` and `libnftnl` to compile your exploit
