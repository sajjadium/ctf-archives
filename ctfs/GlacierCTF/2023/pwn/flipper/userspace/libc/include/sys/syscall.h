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

#include "types.h"

#ifdef __cplusplus
extern "C" {
#endif


/**
 * Low-level syscall function, takes 6 arguments where the first is the syscall
 * number as defined in the kernel syscall definitions.
 * Unused arguments can be filled up with 0x00s.
 * e.g. __syscall(sc_exit, status, 0x00, 0x00, 0x00, 0x00);
 * DO NOT CHANGE SIGNATURE.
 */
extern size_t __syscall(size_t arg1, size_t arg2, size_t arg3, size_t arg4, size_t arg5,
                        size_t arg6);

#ifdef __cplusplus
}
#endif



