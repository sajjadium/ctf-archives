KERNEL_VERSION="linux-6.1.39"

# Make sure clang 17 is installed
if [[ `which clang` == "" || `which lld` == "" || `clang --version | grep 17` == "" ]]; then
    echo "[x] clang/lld 17 not installed!"
    exit 1
fi

# Download kernel and unpack it
wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/snapshot/$KERNEL_VERSION.tar.gz
tar -xzvf $KERNEL_VERSION.tar.gz && rm $KERNEL_VERSION.tar.gz

# Copy config and apply patch
cd $KERNEL_VERSION
cp -av ../kernel.config .config
patch -p1 < ../cor.patch

# Compile
make CC=clang HOSTCC=clang LLVM=1 KBUILD_BUILD_TIMESTAMP='Tue January 1 00:00:00 UTC 2030' KBUILD_BUILD_USER=d KBUILD_BUILD_HOST=corOS -j `nproc`

cd ../
