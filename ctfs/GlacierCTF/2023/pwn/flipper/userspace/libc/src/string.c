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

#include "string.h"

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
int memcmp(const void *first_position, const void *second_position,
           size_t number_of_bytes)
{
  const char *b1 = first_position;
  const char *b2 = second_position;

  if(number_of_bytes == 0)
    return 0;

  while(number_of_bytes--)
  {
    if(*b1++ != *b2++)
      return (*--b1 - *--b2);
  }

  return 0;
}

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
void* memcpy(void *destination, const void *source, size_t number_of_bytes)
{
  char *byte_destination = (char*) destination;
  const char *byte_source = (const char*) source;

  // The areas must not overlap!
  if(((byte_source < (byte_destination + number_of_bytes)) &&
      (byte_source > byte_destination)) ||
     ((byte_destination < (byte_source + number_of_bytes)) &&
      (byte_destination > byte_source)))
    return destination;

  if(number_of_bytes == 0 || source == destination)
    return destination;

  while(number_of_bytes--)
    *byte_destination++ = *byte_source++;

  return destination;
}

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
void *memset(void *position, int value, size_t number_of_bytes)
{
  char *byte_block = (char *) position;

  if(number_of_bytes)
  {
    while(number_of_bytes--)
      *byte_block++ = (char) value;
  }

  return position;
}

/**
 * Gets the length of the null terminated string
 *
 * @param str String
 * @return length of String
 */
size_t strlen(const char* str) 
{
  size_t count=0;
  while(str[count] != '\0')
    count++;
  return count;
}

/**
 * Compares the 2 Strings, default implementation
 */
int strcmp (const char * l, const char * r)
{
 
    for(; *l == *r; ++l, ++r)
        if(*l == 0)
            return 0;
    return *(unsigned char *)l < *(unsigned char *)r ? -1 : 1;
}


char *strstr(const char *haystack, const char *needle)
{
  if(*needle == '\0')
    return (char*)haystack;

  for(int i = 0; haystack[i] != '\0'; i++)
  {
    int j;
    for(j = 0; needle[j] != '\0' && haystack[i + j] == needle[j]; j++)
      ;
    if(needle[j] == '\0')
      return (char*)(haystack + i);
  }

  return NULL;
}