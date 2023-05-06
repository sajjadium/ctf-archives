There is strategy in kernel exploitation. First off, having a good primitive is very important.

The arbitrary read is at the front and keeps an eye on how the pwner is performing. And the rest of the bugs focuses on the back of the information leak and follows their lead.

Compiled Linux v5.15 with the following options...

CONFIG_PAGE_TABLE_ISOLATION=y
CONFIG_SECURITY_DMESG_RESTRICT=y
CONFIG_STATIC_USERMODEHELPER=y
CONFIG_STATIC_USERMODEHELPER_PATH=""
CONFIG_SLAB_FREELIST_HARDENED=y
CONFIG_SLUB=y
