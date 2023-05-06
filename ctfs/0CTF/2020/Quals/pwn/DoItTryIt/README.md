## build

Ubuntu 18.04

```
git clone https://github.com/microsoft/ChakraCore.git
cd ChakraCore
git reset --hard 33db8efd9f02cd528a7305391d7d10765a2e85f3
patch -p1 < ../patch.diff
./build.sh --static
```
