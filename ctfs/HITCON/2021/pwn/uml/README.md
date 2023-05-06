# UML

```
$ git submodule status
 a2547651bc896f95a3680a6a0a27401e7c7a1080 linux (v5.15.6)
$ make ARCH=um defconfig
$ make ARCH=um
$ strip -s linux
```

A tiny hint for you:
```
$ tree -L 1
.
├── flag-<hash of flag>
├── fs
├── linux
└── run.sh
```
