## myfuse

this is for my OS lecture file system lab

I intend to implement a XV6-like file system on fuse that can work in a real Linux machine

到目前为止已经基本完成，此项目只是玩具（还挺好玩的），并且存在许多 bug，我会尽量慢慢修复，虽然只是可能。虽然有单元测试，但是覆盖面并不全（写测试还是有点困难，特别是如果想要 cover 所有的 cases）

当然有许多许多细节还没有做好，比如权限控制，目前并没有鉴权，chmod 的存在只是为了让文件可执行；比如调用的返回值（errno）并没有按照文档一个个配好。由于这里比较繁琐，并且超出了我玩一玩的需求，所以可能不准备搞了

### make

```
mkdir build && cd ./build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
```

### format a disk(or any file/block device)

```
./build/mkfs/mkfs.myfuse <path to file>
```

### mount!

```
./build/myfuse /path/to/mount --device_path <path to formated device>
```

### demo


https://user-images.githubusercontent.com/32593305/192845502-802580a8-9f33-4f7e-a973-1fd49230277d.mp4



