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

#pragma once

#include "unistd.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * The basic flags for files
 */
#ifndef O_RDONLY
#define O_RDONLY    0x0001
#endif
#ifndef O_WRONLY
#define O_WRONLY    0x0002
#endif
#ifndef O_RDWR
#define O_RDWR      0x0004
#endif
#ifndef O_CREAT
#define O_CREAT     0x0008
#endif
#ifndef O_APPEND
#define O_APPEND    0x0010
#endif
#ifndef O_EXCL
#define O_EXCL      0x0020
#endif
#ifndef O_NONBLOCK
#define O_NONBLOCK  0x0040
#endif
#ifndef O_TRUNC
#define O_TRUNC     0x0080
#endif
#ifndef O_SYNC
#define O_SYNC      0x0100
#endif
#ifndef O_DSYNC
#define O_DSYNC     0x0200
#endif
#ifndef O_RSYNC
#define O_RSYNC     O_SYNC
#endif

/**
 * The basic access modes for files
 */
#define A_READABLE  0x0001
#define A_WRITABLE  0x0002
#define A_EXECABLE  0x0004


/**
 * Structure for describing a file lock
 *
 */
struct flock
{

  /**
   * Type of lock
   * F_RDLCK, F_WRLCK or F_UNLCK
   *
   */
  short l_type;

  /**
   * Flag for starting offset
   *
   */
  short l_whence;

  /**
   * Relative offset in bytes
   *
   */
  off_t l_start;

  /**
   * Size, if 0 then until EOF
   *
   */
  off_t l_len;

  /**
   * Process ID of the process holding the lock.
   *
   */
  pid_t l_pid;

};

/**
 * Equivalent to open() with flags equal to O_CREAT | O_WRONLY | O_TRUNC.
 *
 * @param path A pathname pointing to the file to open
 * @param mode
 * @return A valid file descriptor or -1 if an error occured
 *
 */
extern int creat(const char *path, mode_t mode);

/**
 * Converts a pathname into a file descriptor which can be used in subsequent
 * read and write operations.
 * If successfull, the lowest file descriptor not currently open for the
 * process will be returned.
 *
 * Possible values for the flags parameter are:
 *  - O_RDONLY  Open for reading only
 *  - O_WRONLY  Open for writing only
 *  - O_RDWR    Open for reading and writing
 *
 * which can be bitwise combined (or'd) with:
 *  - O_APPEND  Open in append mode
 *  - O_CREAT   Create file if it does not exist
 *  - O_TRUNC   Truncate file to 0 length if it already exists and is a
 *              regular file
 *
 * @param path A pathname pointing to the file to open
 * @param flags Flags to specify how the file is opened
 * @return A valid file descriptor or -1 if an error occured
 *
 */
extern int open(const char *path, int flags, ...);

#ifdef __cplusplus
}
#endif


