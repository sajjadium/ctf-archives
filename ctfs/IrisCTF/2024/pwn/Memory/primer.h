// Thanks: https://tldp.org/LDP/lkmpg/2.4/html/x856.html

#ifndef PRIMER_H
#define PRIMER_H

#include <linux/ioctl.h>

#define MAJOR_NUM 100

#define IOCTL_QUERY _IOR(MAJOR_NUM, 0, unsigned long)
#define DEVICE_FILE_NAME "primer"

#endif
