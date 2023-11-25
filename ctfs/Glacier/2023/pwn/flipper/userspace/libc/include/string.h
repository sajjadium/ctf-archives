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
 * NULL pointer constant
 *
 */
#define NULL 0

/**
 * Compares the given number of bytes of the memory areas started by the
 * given pointers.
 * The return value will be an integer less than zero, if the bytes at the
 * first area are less than those of the second. It will be zero for equality,
 * and a value greater zero if the bytes at the first area are greater than
 * those of the second
 *
 * @param first_position Position of the first memory area
 * @param second_position Position of the second memory area
 * @param number_of_bytes Number of bytes to compare
 * @return An integer indicating the found differences
 *
 */
extern int memcmp(const void *first_position, const void *second_position,
                  size_t number_of_bytes);

/**
 * Copies the given number of bytes from memory area source to memory area
 * destination. The memory areas should not overlap.
 *
 * @param destination Destination memory position
 * @param source Source memory position
 * @param number_of_bytes Number of bytes to copy
 * @return A pointer to the destination
 *
 */
extern void* memcpy(void *destination, const void *source,
                  size_t number_of_bytes);

/**
 * Fills the given number of bytes of the memory area pointed to by the given
 * position with the given value.
 *
 * @param position Position of the memory area
 * @param value Value to write
 * @param number_of_bytes Number of bytes to write
 * @return A pointer to the memory area
 *
 */
extern void *memset(void *position, int value, size_t number_of_bytes);

/**
 * Gets the length of the null terminated string
 *
 * @param str String
 * @return length of String
 */
extern size_t strlen(const char* str);

/**
 * Compares the 2 Strings, default implementation
 */
extern int strcmp (const char * l, const char * r);

/**
 * searches for needle in haystack
 */
extern char *strstr(const char *haystack, const char *needle);

#ifdef __cplusplus
}
#endif



