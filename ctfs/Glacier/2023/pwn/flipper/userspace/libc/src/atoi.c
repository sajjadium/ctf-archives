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

#include "stdlib.h"

/**
 * parses the given string and returns its value as integer
 * @param string the string for parsing
 * @return the parsed value
 *
 */
int atoi(const char *string)
{
  // taken from kprintf.cpp
  int number = 0;
  int base = 10;
  int negative = 0;

  if(*string == '-')
  {
    negative = 1;
    ++string;
  }
  else
    if(*string == '+')
      ++string;

  while(*string >= '0' && *string <= '9')
  {
    number *= base;
    number += *string - '0';
    ++string;
  }

  if(negative)
    number *= -1;

  return number;
}

/**
 * parses the given string and returns its value as long
 * @param string the string for parsing
 * @return the parsed value
 *
 */
long atol(const char *string)
{
  // taken from kprintf.cpp
  long number = 0;
  long base = 10;
  int negative = 0;

  if(*string == '-')
  {
    negative = 1;
    ++string;
  }
  else
    if(*string == '+')
      ++string;

  while(*string >= '0' && *string <= '9')
  {
    number *= base;
    number += *string - '0';
    ++string;
  }

  if(negative)
    number *= -1;

  return number;
}
