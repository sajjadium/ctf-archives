You can compile your own kernel as follows:

```
# wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.58.tar.gz
wget https://mirrors.tuna.tsinghua.edu.cn/kernel/v6.x/linux-6.1.58.tar.gz
tar -xzvf linux-6.1.58.tar.gz
patch -p0 < n1ctf.diff
cp n1ctf-Kconfig ./linux-6.1.58/.config
cd linux-6.1.58
make bzImage -j`nproc`
```