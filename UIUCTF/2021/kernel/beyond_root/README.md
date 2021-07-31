The flag is hidden away in initrd, but you are in a mounted hard drive. There's another busybox in initrd in case you need it.

$ stty raw -echo; nc beyond-root.chal.uiuc.tf 1337; stty -raw echo
