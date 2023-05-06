Who doesn't like hashbrowns? I like them so much that I wrote a driver named after them! But apparently programming is hard and I might have made a mistake...

Please note that the following measures are active (whether they are important to the exploit process is up to you):

CONFIG_SLAB_FREELIST_RANDOM=y
CONFIG_SLAB=y
CONFIG_FG_KASLR=y

SMAP, SMEP, and KPTI are enabled as well.

nc hashbrown.dicec.tf 31337

Note: only one connection per IP is allowed, and there is a 10 minute wall-clock time limit from the moment you connect. Test locally!
