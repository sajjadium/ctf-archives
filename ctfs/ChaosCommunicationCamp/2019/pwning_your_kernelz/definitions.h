//
//  definitions.h
//  pwning your kernelz
//
//  Created by Linus Henze.
//  Copyright © 2019 Linus Henze. All rights reserved.
//

//
// THIS IS 32 BIT ONLY, USE XCODE 9.4.1
//

#ifndef definitions_h
#define definitions_h

#include <string.h>    // memset
#include <mach/mach.h> // thread_set_state

#pragma pack(4)

#define x86_SAVED_STATE32        THREAD_STATE_NONE + 1
#define x86_SAVED_STATE64        THREAD_STATE_NONE + 2

struct x86_saved_state32 {
    uint32_t    gs;
    uint32_t    fs;
    uint32_t    es;
    uint32_t    ds;
    uint32_t    edi;
    uint32_t    esi;
    uint32_t    ebp;
    uint32_t    cr2;
    uint32_t    ebx;
    uint32_t    edx;
    uint32_t    ecx;
    uint32_t    eax;
    uint16_t    trapno;
    uint16_t    cpu;
    uint32_t    err;
    uint32_t    eip;
    uint32_t    cs;
    uint32_t    efl;
    uint32_t    uesp;
    uint32_t    ss;
};
typedef struct x86_saved_state32 x86_saved_state32_t;

#define x86_SAVED_STATE32_COUNT    ((mach_msg_type_number_t) \
(sizeof (x86_saved_state32_t)/sizeof(unsigned int)))

#pragma pack(0)

#endif /* definitions_h */
