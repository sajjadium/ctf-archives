#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/string.h>
#include <linux/delay.h>

MODULE_AUTHOR("amritabi0s1@gmail.com");
MODULE_DESCRIPTION("MultiStorage");
MODULE_LICENSE("GPL");

static DEFINE_MUTEX(lock);

#define ADD 0x1337
#define DELETE 0x1338
#define VIEW 0x1339

#define TYPE1 0xbabe1337
#define TYPE2 0xbeef1337

/*  Globals */
void * t1Ptr = NULL;
void * t2Ptr = NULL;
int t1_len = 0;
int t2_len = 0;

/*  Type 1 stores string */
typedef struct{
    char data[28];
    unsigned int id;
}Type1;

/*  Type 2 stores int arr */
typedef struct{
    unsigned int arr[7];
    unsigned int id;
}Type2;

/*  Just so we know total count */
typedef struct{
    unsigned int length;
}Header;

typedef struct{
    char * buf;
    unsigned int type; /* Used in view  */
}req;

/*  User input  for type1*/
typedef struct{
    unsigned int type;
    char buf[28];
}input1;

/*  User input  for type2*/
typedef struct{
    unsigned int type;
    unsigned int arr[7];
}input2;

static noinline void Info(char* s){
    msleep(10);
    printk(KERN_INFO "%s", s);
    return;
}
