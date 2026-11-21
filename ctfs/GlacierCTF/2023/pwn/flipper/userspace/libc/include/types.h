#pragma once

#ifdef __cplusplus
extern "C" {
#endif

typedef long unsigned int off_t;
typedef long unsigned int mode_t;
typedef long unsigned int uid_t;
typedef long unsigned int gid_t;
typedef long unsigned int size_t;
typedef long int ssize_t;

#ifndef PID_T_DEFINED
#define PID_T_DEFINED
typedef long int pid_t;
#endif

#ifdef __cplusplus
}
#endif

