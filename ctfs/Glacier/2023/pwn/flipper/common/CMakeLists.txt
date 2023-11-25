include_directories(
    include
    ../arch/common/include
    ../arch/${ARCH}/include
    ../arch/${ARCH}/common/include
    ../arch/${ARCH}/../common/include
    ../arch/${ARCH}/../../common/include
    include/kernel
    include/fs
    include/fs/devicefs
    include/fs/minixfs
    include/fs/pseudofs
    include/fs/ramfs
    include/util
    include/ustl
)

add_subdirectory(source)
