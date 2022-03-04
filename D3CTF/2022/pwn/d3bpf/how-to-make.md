### get the source

```
wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/linux-hwe-5.11/5.11.0-60.60/linux-hwe-5.11_5.11.0.orig.tar.gz
```

### make

```
git apply < diff
make menuconfig # change nothing, save and exit
sed -i 's/CONFIG_SYSTEM_TRUSTED_KEYS=/#&/' ./.config
make bzImage -j$(nproc)
```
