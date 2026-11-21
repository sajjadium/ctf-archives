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
#include "stdio.h"
#include "stdlib.h"
#include "stdarg.h"
#include "ctype.h"


#define unlikely(arg) arg

// The following functions defined before scanf are taken from the linux
// kernel (v.2.6.13) file lib/vsprintf.c

/**
 * Maximum integer value
 *
 */
#define INT_MAX         ((int)(~0U>>1))


/**
 * simple_strtoul - convert a string to an unsigned long
 * @cp: The start of the string
 * @endp: A pointer to the end of the parsed string will be placed here
 * @base: The number base to use
 */
unsigned long simple_strtoul(const char *cp,char **endp,unsigned int base)
{
  unsigned long result = 0,value;

  if (!base) {
    base = 10;
    if (*cp == '0') {
      base = 8;
      cp++;
      if ((toupper(*cp) == 'X') && isxdigit(cp[1])) {
        cp++;
        base = 16;
      }
    }
  } else if (base == 16) {
    if (cp[0] == '0' && toupper(cp[1]) == 'X')
      cp += 2;
  }
  while (isxdigit(*cp) &&
         (value = isdigit(*cp) ? *cp-'0' : toupper(*cp)-'A'+10) < base) {
    result = result*base + value;
    cp++;
  }
  if (endp)
    *endp = (char *)cp;
  return result;
}


/**
 * simple_strtol - convert a string to a signed long
 * @cp: The start of the string
 * @endp: A pointer to the end of the parsed string will be placed here
 * @base: The number base to use
 */
long simple_strtol(const char *cp,char **endp,unsigned int base)
{
  if(*cp=='-')
    return -simple_strtoul(cp+1,endp,base);
  return simple_strtoul(cp,endp,base);
}


/**
 * simple_strtoull - convert a string to an unsigned long long
 * @cp: The start of the string
 * @endp: A pointer to the end of the parsed string will be placed here
 * @base: The number base to use
 */
unsigned long long simple_strtoull(const char *cp,char **endp,unsigned int base)
{
  unsigned long long result = 0,value;

  if (!base) {
    base = 10;
    if (*cp == '0') {
      base = 8;
      cp++;
      if ((toupper(*cp) == 'X') && isxdigit(cp[1])) {
        cp++;
        base = 16;
      }
    }
  } else if (base == 16) {
    if (cp[0] == '0' && toupper(cp[1]) == 'X')
      cp += 2;
  }
  while (isxdigit(*cp) && (value = isdigit(*cp) ? *cp-'0' : (islower(*cp)
      ? toupper(*cp) : *cp)-'A'+10) < base) {
    result = result*base + value;
    cp++;
  }
  if (endp)
    *endp = (char *)cp;
  return result;
}


/**
 * simple_strtoll - convert a string to a signed long long
 * @cp: The start of the string
 * @endp: A pointer to the end of the parsed string will be placed here
 * @base: The number base to use
 */
long long simple_strtoll(const char *cp,char **endp,unsigned int base)
{
  if(*cp=='-')
    return -simple_strtoull(cp+1,endp,base);
  return simple_strtoull(cp,endp,base);
}

static int skip_atoi(const char **s)
{
  int i=0;

  while (isdigit(**s))
    i = i*10 + *((*s)++) - '0';
  return i;
}


/**
 * vsscanf - Unformat a buffer into a list of arguments
 * @buf:  input buffer
 * @fmt:  format of buffer
 * @args: arguments
 */
int vsscanf(const char * buf, const char * fmt, va_list args)
{
  const char *str = buf;
  char *next;
  char digit;
  int num = 0;
  int qualifier;
  int base;
  int field_width;
  int is_sign = 0;

  while(*fmt && *str) {
    /* skip any white space in format */
    /* white space in format matchs any amount of
     * white space, including none, in the input.
     */
    if (isspace(*fmt)) {
      while (isspace(*fmt))
        ++fmt;
      while (isspace(*str))
        ++str;
    }

    /* anything that is not a conversion must match exactly */
    if (*fmt != '%' && *fmt) {
      if (*fmt++ != *str++)
        break;
      continue;
    }

    if (!*fmt)
      break;
    ++fmt;

    /* skip this conversion.
     * advance both strings to next white space
     */
    if (*fmt == '*') {
      while (!isspace(*fmt) && *fmt)
        fmt++;
      while (!isspace(*str) && *str)
        str++;
      continue;
    }

    /* get field width */
    field_width = -1;
    if (isdigit(*fmt))
      field_width = skip_atoi(&fmt);

    /* get conversion qualifier */
    qualifier = -1;
    if (*fmt == 'h' || *fmt == 'l' || *fmt == 'L' ||
        *fmt == 'Z' || *fmt == 'z') {
      qualifier = *fmt++;
      if (unlikely(qualifier == *fmt)) {
        if (qualifier == 'h') {
          qualifier = 'H';
          fmt++;
        } else if (qualifier == 'l') {
          qualifier = 'L';
          fmt++;
        }
      }
    }
    base = 10;
    is_sign = 0;

    if (!*fmt || !*str)
      break;

    switch(*fmt++) {
    case 'c':
    {
      char *s = (char *) va_arg(args,char*);
      if (field_width == -1)
        field_width = 1;
      do {
        *s++ = *str++;
      } while (--field_width > 0 && *str);
      num++;
    }
    continue;
    case 's':
    {
      char *s = (char *) va_arg(args, char *);
      if(field_width == -1)
        field_width = INT_MAX;
      /* first, skip leading white space in buffer */
      while (isspace(*str))
        str++;

      /* now copy until next white space */
      while (*str && !isspace(*str) && field_width--) {
        *s++ = *str++;
      }
      *s = '\0';
      num++;
    }
    continue;
    case 'n':
      /* return number of characters read so far */
    {
      int *i = (int *)va_arg(args,int*);
      *i = str - buf;
    }
    continue;
    case 'o':
      base = 8;
      break;
    case 'x':
    case 'X':
      base = 16;
      break;
    case 'i':
      base = 0;
      // fall through
    case 'd':
      is_sign = 1;
    case 'u':
      break;
    case '%':
      /* looking for '%' in str */
      if (*str++ != '%')
        return num;
      continue;
    default:
      /* invalid format; stop here */
      return num;
    }

    /* have some sort of integer conversion.
     * first, skip white space in buffer.
     */
    while (isspace(*str))
      str++;

    digit = *str;
    if (is_sign && digit == '-')
      digit = *(str + 1);

    if (!digit
                    || (base == 16 && !isxdigit(digit))
                    || (base == 10 && !isdigit(digit))
                    || (base == 8 && (!isdigit(digit) || digit > '7'))
                    || (base == 0 && !isdigit(digit)))
        break;

    switch(qualifier) {
    case 'H': /* that's 'hh' in format */
      if (is_sign) {
        signed char *s = (signed char *) va_arg(args,signed char *);
        *s = (signed char) simple_strtol(str,&next,base);
      } else {
        unsigned char *s = (unsigned char *) va_arg(args, unsigned char *);
        *s = (unsigned char) simple_strtoul(str, &next, base);
      }
      break;
    case 'h':
      if (is_sign) {
        short *s = (short *) va_arg(args,short *);
        *s = (short) simple_strtol(str,&next,base);
      } else {
        unsigned short *s = (unsigned short *) va_arg(args, unsigned short *);
        *s = (unsigned short) simple_strtoul(str, &next, base);
      }
      break;
    case 'l':
      if (is_sign) {
        long *l = (long *) va_arg(args,long *);
        *l = simple_strtol(str,&next,base);
      } else {
        unsigned long *l = (unsigned long*) va_arg(args,unsigned long*);
        *l = simple_strtoul(str,&next,base);
      }
      break;
    case 'L':
      if (is_sign) {
        long long *l = (long long*) va_arg(args,long long *);
        *l = simple_strtoll(str,&next,base);
      } else {
        unsigned long long *l = (unsigned long long*) va_arg(args,unsigned long long*);
        *l = simple_strtoull(str,&next,base);
      }
      break;
    case 'Z':
    case 'z':
    {
      size_t *s = (size_t*) va_arg(args,size_t*);
      *s = (size_t) simple_strtoul(str,&next,base);
    }
    break;
    default:
      if (is_sign) {
        int *i = (int *) va_arg(args, int*);
        *i = (int) simple_strtol(str,&next,base);
      } else {
        unsigned int *i = (unsigned int*) va_arg(args, unsigned int*);
        *i = (unsigned int) simple_strtoul(str,&next,base);
      }
      break;
    }
    num++;

    if (!next)
      break;
    str = next;
  }
  return num;
}


/**
 * Size of the static input buffer for scanf
 *
 */
#define INPUT_BUFFER_SIZE 256

/**
 * Reads input from stdin according to the given format and
 * assigns read values to the given variables.
 * A detailed description of the format is given in the
 * 'Linux Programmer's Manual'.
 *
 * @param format A string containing the input format, followed by an\
 argument list of variables for assignment
 * @return The number of input items assigned, zero indicates that no input\
 items were assigned while input was available, EOF if failure (e.g.\
 end-of-file) occurs before any items have been read
 *
 */
int scanf(const char *fmt, ...)
{
  va_list args;
  int return_val = 0;

  char input_buffer_array[INPUT_BUFFER_SIZE];
  char *buffer = (char*) &input_buffer_array;

  if(gets(buffer, INPUT_BUFFER_SIZE) == NULL)
    return return_val;

  va_start(args, fmt);

  return_val = vsscanf(buffer, fmt, args);

  va_end(args);

  return return_val;
}


int sscanf(const char *buffer, const char *fmt, ...)
{
  va_list args;
  int return_val = 0;

  va_start(args, fmt);

  return_val = vsscanf(buffer, fmt, args);

  va_end(args);

  return return_val;
}


/**
 * Reads the next character from stdin.
 * The read value will be returned as unsigned char cast to an int
 *
 * @return The read character on success, EOF otherwise and errno is set\
 appropriately
 *
 */
int getchar()
{
  char character = 0;
  int characters_read = read(STDIN_FILENO, (void*) &character, 1);

  if(!characters_read || (characters_read == -1))
    return EOF;

  return (int) character;
}

/**
 * Reads a line from stdin and stores it in the string pointed to by the
 * argument.
 * Reading is terminated by a newline, EOF which are both replaced by '\0' or
 * when the buffer is full.
 *
 * @param input_buffer The buffer where the input is stored
 * @param buffer_size The size of the buffer
 * @return A pointer to the input_string on success, NULL otherwise
 *
 */
char *gets(char *input_buffer, size_t buffer_size)
{
  unsigned int counter = 0;
  if (!buffer_size)
    return input_buffer;

  int cchar = 0;

  while((cchar = getchar()) != EOF)
  {

    if(cchar == '\r' || cchar == '\n' || (counter + 1) >= buffer_size) // there must be one space left for the \0 at end
    {
      *(input_buffer + counter) = '\0';
      break;
    }
    else
    {
      *(input_buffer + counter) = (char)cchar;
    }

    if (cchar == '\b')
    {
      if (counter > 0)
        counter--;
    }
    else
    {
      counter++;
    }

  }

  return input_buffer;
}


char *fgets(char *str, int num, int fd)
{
  unsigned int counter = 0;
  ssize_t readCount = 0;
  char buffer[128];
  off_t oldOffset = lseek(fd, 0, SEEK_CUR);

  if (!num)
    return str;

  do
  {
    readCount = read(fd, buffer, 128);
    for (ssize_t i = 0; i < readCount; i++)
    {
      if (buffer[i] == '\r' || buffer[i] == '\n' || (counter+1) >= num)
      {
        *(str + counter) = '\0';
        lseek(fd, oldOffset+counter+1, SEEK_SET);
        return str;
      }
      else
      {
        *(str + counter) = buffer[i];
      }

      if (buffer[i] == '\b')
      {
        if (counter > 0)
          counter--;
      }
      else
      {
        counter++;
      }
    }
  } while (readCount > 0);

  if (num - counter)
    str[counter] = '\0';

  if (counter == 0)
    return 0;

  return str;
}
