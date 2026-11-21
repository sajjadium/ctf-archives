// Projectname: SWEB
// Simple operating system for educational purposes
//
// Copyright (C) 2005  Andreas Niederl
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#include "unistd.h"
#include "../../../common/include/kernel/syscall-definitions.h"
#include "sys/syscall.h"
#include "stdarg.h"
#include "stdlib.h"

/**
 * Creates a child process.
 * The new process will be nearly identical to the callee except for its
 * PID and PPID.
 * Resource utilizations are set to zero, file locks are not inherited.
 *
 */
pid_t fork()
{
  return __syscall(sc_fork, 0x00, 0x00, 0x00, 0x00, 0x00);
}

/**
 * Replaces the current process image with a new one.
 * The values provided with the argv array are the arguments for the new
 * image starting with the filename of the file to be executed (by convention).
 * This pointer array must be terminated by a NULL pointer (which has to be
 * of type char *.
 * If this function returns, an error has occured.
 *
 * @param path path to the file to execute
 * @param argv an array containing the arguments
 * @return 0 on success, -1 otherwise and errno is set appropriately
 *
 */
int execv(const char *path __attribute__((unused)), char *const argv[] __attribute__((unused)))
{

  return 0;
}

/**
 * Terminates the calling process. Any open file descriptors belonging to the
 * process are closed, any children of the process are inherited by process
 * 1, init, and the process's parent is sent a SIGCHLD signal.
 * The value status is returned to the parent process as the process's exit
 * status and can be collected using a wait call.
 * This function does NOT call any functions registered with atexit(), nor any
 * registered signal handlers.
 *
 * @param status exit status of the process
 *
 */
void _exit(int status)
{
  __syscall(sc_exit, status, 0x00, 0x00, 0x00, 0x00);
}
void exit(int status)
{
  __syscall(sc_exit, status, 0x00, 0x00, 0x00, 0x00);
}
