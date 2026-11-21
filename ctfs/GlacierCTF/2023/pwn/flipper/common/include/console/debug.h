#pragma once

#include "kprintf.h"

enum AnsiColor
{
  Ansi_Red = 31,
  Ansi_Green = 32,
  Ansi_Yellow = 33,
  Ansi_Blue = 34,
  Ansi_Magenta = 35,
  Ansi_Cyan = 36,
  Ansi_White = 37,
};

#define OUTPUT_ENABLED 0x80000000
#define OUTPUT_ADVANCED 0x70000000
#define OUTPUT_FLAGS (OUTPUT_ENABLED | OUTPUT_ADVANCED)

#ifndef NOCOLOR
#define DEBUG_FORMAT_STRING "\033[1;%zum[%-11s]\033[0;39m"
#define COLOR_PARAM(flag) (flag & ~OUTPUT_FLAGS), #flag
#else
#define DEBUG_FORMAT_STRING "[%-11s]"
#define COLOR_PARAM(flag) #flag
#endif

#ifndef EXE2MINIXFS
#define debug(flag, ...) do { if (flag & OUTPUT_ENABLED) { kprintfd(DEBUG_FORMAT_STRING, COLOR_PARAM(flag)); kprintfd(__VA_ARGS__); } } while (0)
#endif


//group Block Device
const size_t BD_MANAGER         = Ansi_Yellow;
const size_t BD_VIRT_DEVICE     = Ansi_Yellow;

//group Console
const size_t KPRINTF            = Ansi_Yellow;

//group kernel
const size_t LOCK               = Ansi_Yellow  | OUTPUT_ENABLED;
const size_t LOADER             = Ansi_White   | OUTPUT_ENABLED;
const size_t SCHEDULER          = Ansi_Yellow  | OUTPUT_ENABLED;
const size_t SYSCALL            = Ansi_Blue    | OUTPUT_ENABLED;
const size_t MAIN               = Ansi_Red     | OUTPUT_ENABLED;
const size_t THREAD             = Ansi_Magenta | OUTPUT_ENABLED;
const size_t USERPROCESS        = Ansi_Cyan    | OUTPUT_ENABLED;
const size_t PROCESS_REG        = Ansi_Yellow  | OUTPUT_ENABLED;
const size_t BACKTRACE          = Ansi_Cyan    | OUTPUT_ENABLED;
const size_t USERTRACE          = Ansi_Red     | OUTPUT_ENABLED;

//group memory management
const size_t PM                 = Ansi_Green | OUTPUT_ENABLED;
const size_t PAGEFAULT          = Ansi_Green | OUTPUT_ENABLED;
const size_t CPU_ERROR          = Ansi_Red   | OUTPUT_ENABLED;
const size_t KMM                = Ansi_Yellow;

//group driver
const size_t DRIVER             = Ansi_Yellow;
const size_t ATA_DRIVER         = Ansi_Yellow;
const size_t IDE_DRIVER         = Ansi_Yellow;
const size_t MMC_DRIVER         = Ansi_Yellow;

//group arch
const size_t A_BOOT             = Ansi_Yellow | OUTPUT_ENABLED;
const size_t A_COMMON           = Ansi_Yellow;
const size_t A_MEMORY           = Ansi_Yellow;
const size_t A_SERIALPORT       = Ansi_Yellow;
const size_t A_KB_MANAGER       = Ansi_Yellow;
const size_t A_INTERRUPTS       = Ansi_Yellow;

//group file system
const size_t FS                 = Ansi_Yellow;
const size_t RAMFS              = Ansi_White;
const size_t DENTRY             = Ansi_Blue;
const size_t INODE              = Ansi_Blue;
const size_t PATHWALKER         = Ansi_Yellow;
const size_t PSEUDOFS           = Ansi_Yellow;
const size_t VFSSYSCALL         = Ansi_Yellow;
const size_t VFS                = Ansi_Yellow | OUTPUT_ENABLED;
const size_t VFS_FILE           = Ansi_Yellow;
const size_t SUPERBLOCK         = Ansi_Yellow;

//group minix
const size_t M_STORAGE_MANAGER  = Ansi_Yellow;
const size_t M_INODE            = Ansi_Yellow;
const size_t M_SB               = Ansi_Yellow;
const size_t M_ZONE             = Ansi_Yellow;
