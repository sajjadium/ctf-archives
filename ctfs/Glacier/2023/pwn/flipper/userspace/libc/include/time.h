#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#define CLOCKS_PER_SEC 1000000

#ifndef CLOCK_T_DEFINED
#define CLOCK_T_DEFINED
typedef unsigned int clock_t;
#endif // CLOCK_T_DEFINED

extern clock_t clock(void);

#ifdef __cplusplus
}
#endif

