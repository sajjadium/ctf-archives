### get the source

```
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.12.tar.xz
```

### make

```
git apply < diff
echo "source \"kernel/bpf/Kconfig\"" >> ./Kconfig
make menuconfig # enter BPF subsystem, excludes the "Disable unprivileged BPF by default", save and exit
sed -i 's/CONFIG_SYSTEM_TRUSTED_KEYS=/#&/' ./.config
sed -i 's/CONFIG_SYSTEM_REVOCATION_KEYS=/#&/' ./.config
make bzImage -j$(nproc)
```
