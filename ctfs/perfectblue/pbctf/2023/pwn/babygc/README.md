commit: 1fdbfd80de70e622ef15360b8cc069e72432c99e

build instructions:
```
# in webkit source dir
patch -p1 < ../path/to/challenge.diff
CC=clang CXX=clang++ CXXFLAGS="-Wno-error -Wno-cast-align -g" CFLAGS="-Wno-error -Wno-cast-align -g" ./Tools/Scripts/build-webkit --jsc-only --release
```

To get flag, run `/readflag` on remote.
