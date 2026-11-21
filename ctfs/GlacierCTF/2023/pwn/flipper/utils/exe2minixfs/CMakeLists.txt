cmake_minimum_required(VERSION 3.1.0)

file(GLOB util_exe2minixfs_SOURCES *.cpp
                                   ../../common/source/util/Bitmap.cpp
                                   ../../common/source/fs/Inode.cpp
                                   ../../common/source/fs/Dentry.cpp
                                   ../../common/source/fs/FileDescriptor.cpp
                                   ../../common/source/fs/FileSystemInfo.cpp
                                   ../../common/source/fs/FileSystemType.cpp
                                   ../../common/source/fs/Superblock.cpp
                                   ../../common/source/fs/File.cpp
                                   ../../common/source/fs/PathWalker.cpp
                                   ../../common/source/fs/Path.cpp
                                   ../../common/source/fs/VfsMount.cpp
                                   ../../common/source/fs/VfsSyscall.cpp
                                   ../../common/source/fs/minixfs/MinixFSFile.cpp
                                   ../../common/source/fs/minixfs/MinixFSInode.cpp
                                   ../../common/source/fs/minixfs/MinixFSSuperblock.cpp
                                   ../../common/source/fs/minixfs/MinixFSZone.cpp
                                   ../../common/source/fs/minixfs/MinixStorageManager.cpp
                                   ../../common/source/fs/minixfs/StorageManager.cpp)

add_executable(exe2minixfs ${util_exe2minixfs_SOURCES})

target_include_directories(exe2minixfs
  PRIVATE
    .
    ustl
    ../../common/include/util
    ../../common/include/fs
    ../../common/include/fs/minixfs
    ../../common/include/console
)

target_compile_definitions(exe2minixfs PRIVATE EXE2MINIXFS=1)
