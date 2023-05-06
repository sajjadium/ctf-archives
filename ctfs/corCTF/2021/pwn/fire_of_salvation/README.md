Elastic objects in kernel have more power than you think. Note that in addition to a standard initramfs and compressed kernel image, the kernel with symbols and debugging information is provided as well. A kernel config file is provided as well, but some of the important options include:

CONFIG_SLAB=y
CONFIG_SLAB_FREELIST_RANDOM=y
CONFIG_SLAB_FREELIST_HARDEN=y
CONFIG_STATIC_USERMODEHELPER=y
CONFIG_STATIC_USERMODEHELPER_PATH=""
CONFIG_FG_KASLR=y

SMEP, SMAP, and KPTI are of course on. Note that this is an easier variation of the Wall of Perdition challenge.

hint: Using the correct elastic object you can achieve powerful primitives such as arb read and arb write. While arb read for this object has been documented, arb write has not to the extent of our knowledge (it is not a 0 day tho so don't worry).
