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
#include "string.h"

/**
 * structure containing useful variables describing a string stored in a
 * character array
 *
 */
typedef struct c_string
{
  // start pointer
  char *start;

  // working pointer
  char *ptr;

  // length of the string
  size_t length;

  // actual allocated size for the string
  size_t size;

} c_string;

unsigned char const ZEROPAD = 1;    /* pad with zero */
unsigned char const SIGN  = 2;    /* unsigned/signed long */
unsigned char const PLUS  = 4;    /* show plus */
unsigned char const SPACE = 8;    /* space if plus */
unsigned char const LEFT  = 16;   /* left justified */
unsigned char const SPECIAL = 32;   /* 0x */
unsigned char const LARGE = 64;   /* use 'ABCDEF' instead of 'abcdef' */
unsigned char const LONG = 128;   /* sizeof(number) == sizeof(size_t) */

/**
 * Resizes the string in the given c_string structure..
 *
 * @param str structure containing information for the string to resize
 * @param new_size the value for resizing the string
 *
 */
#ifdef STATIC_MEMORY__
void resizeString(c_string *str, unsigned int new_size)
{
  c_string old_string;
  unsigned int copy_count = 0;

  old_string.start = str->start;
  old_string.ptr = str->start;
  old_string.size = str->size;

  str->size = new_size;
  str->start = str->ptr = (char *) malloc(str->size * sizeof(char));

  if(new_size > old_string.size)
    new_size = old_string.size;

  for(; copy_count < new_size; ++copy_count)
    *str->ptr++ = *old_string.ptr++;

  free(old_string.start);
}
#endif // STATIC_MEMORY__


/**
 * Writes a number of fill chars into a string
 */
void writeFillChars(c_string *output_string, int size, char fill )
{
  while( size-- > 0 )
  {
    *output_string->ptr++ = fill;
    ++output_string->length;
  }
}

/**
 * Writes a number into a string using the given parameters.
 *
 * @param output_string Structure containing information for the output string
 * @param number The number for writing
 * @param base The base of the number
 * @param size The size (in digits) for output
 * @param precision Precision for output
 * @param type Output type
 *
 */
void writeNumber(c_string *output_string, size_t number,
                 unsigned int base, unsigned int size,
                 unsigned int precision, unsigned char type)
{
  // code taken from kprintf's output_number()
  char c;
  char sign,tmp[70];
  const char *digits;
  static const char small_digits[] = "0123456789abcdefghijklmnopqrstuvwxyz";
  static const char large_digits[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  unsigned int i;

  digits = (type & LARGE) ? large_digits : small_digits;
  if (type & LEFT)
  {
    type &= ~ZEROPAD;
    size = 0;  //no padding then
  }
  if (base < 2 || base > 36)
    return;
  c = (type & ZEROPAD) ? '0' : ' ';
  sign = 0;
  if (type & SIGN) {
    if ((type & LONG) && ((ssize_t)number) < 0) {
      sign = '-';
      number = - (ssize_t) number;
    } else if (!(type & LONG) && ((int)number) < 0) {
      sign = '-';
      number = - (int) number;
    } else if (type & PLUS) {
      sign = '+';
    } else if (type & SPACE) {
      sign = ' ';
    }
  }
  i = 0;
  if (number == 0)
    tmp[i++]='0';
  else while (number != 0)
  {
    tmp[i++] = digits[number%base];
    number /= base;
  }
  //size -= precision;
  //~ if (!(type&(ZEROPAD+LEFT))) {
    //~ while(size-- >0) {
      //~ console->write(' ');
    //~ }
  //~ }
  if (sign) {
    tmp[i++] = sign;
  }
  if (type & SPECIAL) {
    precision = 0; //no precision with special for now
    if (base==8) {
        tmp[i++] = '0';
    } else if (base==16) {
        tmp[i++] = digits[33];
        tmp[i++] = '0';
      }
  }

  if (precision > size)
    precision = size;

  while (size-- - precision > i)
  {
    *output_string->ptr++ = c;
    ++output_string->length;
  }

  while (precision-- > i)
  {
    *output_string->ptr++ = '0';
    ++output_string->length;
  }

  while (i-- > 0)
  {
    *output_string->ptr++ = tmp[i];
    ++output_string->length;
  }


  //~ while (size-- > 0) {
    //~ if (buf <= end)
      //~ *buf = ' ';
    //~ ++buf;
  //~ }
}

/**
 * Calculates the integer logarithm of base 10.
 *
 * @param n Value of which the logarithm should be calculated
 *
 */
int _log10(double n) 
{
  int log = 0;
  while(n >= 10) 
  {
    n /= 10.0;
    log++;
  }
  return log;
}

/**
 * Calculates 10.0^x for integer x.
 *
 * @param p Exponent, can be positive and negative
 *
 */
double _pow10(int p) 
{
    double res = 1;
    while(p > 0) 
    {
        res *= 10.0;
        p--;
    }
    while(p < 0) 
    {
        res /= 10.0;
        p++;
    }
    return res;
}

/**
 * Writes a floating point number into a string using the given precision.
 * Based on http://stackoverflow.com/a/7097567/5259559
 *
 * @param s Structure containing information for the output string
 * @param n The floating point number for writing
 * @param precision Precision for output
 *
 */
void writeFloat(c_string *output_string, double n, unsigned int width, unsigned int prec, unsigned char flags)
{
    c_string s;
    int character_count = 70;
    s.size = character_count;
    char buffer[character_count];
    s.start = (char *) &buffer;
    s.ptr = s.start;
    s.length = 0;
    double precision = _pow10(-prec);
  
    // special cases
    if (__builtin_isnan(n)) 
    {
        if(flags & LARGE) 
        {
          *s.ptr++ = 'N'; *s.ptr++ = 'A'; *s.ptr++ = 'N';
        } else {
          *s.ptr++ = 'n'; *s.ptr++ = 'a'; *s.ptr++ = 'n';
        }
        s.length += 3;
    } 
    else if (__builtin_isinf(n)) 
    {
        if(flags & LARGE) 
        {
          *s.ptr++ = 'I'; *s.ptr++ = 'N'; *s.ptr++ = 'F';
        } else {
          *s.ptr++ = 'i'; *s.ptr++ = 'n'; *s.ptr++ = 'f';
        }
        s.length += 3;
    } 
    else if (n == 0.0) 
    {
        *(s.ptr++) = '0';
        s.length++;
    } 
    else 
    {
        int digit, m, m1;
        int neg = (n < 0);
        if (neg)
            n = -n;
        // calculate magnitude
        m = _log10(n);
        int useExp = (m >= 14 || (neg && m >= 9) || m <= -9);
        if (neg) 
        {
            *(s.ptr++) = '-';
            s.length++;
        }
        // set up for scientific notation
        if (useExp) 
        {
            if (m < 0)
               m -= 1.0;
            n = n / _pow10(m);
            m1 = m;
            m = 0;
        }
        if (m < 1.0) 
        {
            m = 0;
        }
        // convert the number
        while (n > precision || m >= 0) 
        {
            double weight = _pow10(m);
            if (weight > 0 && !__builtin_isinf(weight)) 
            {
                digit = (int)(n / weight);
                n -= (digit * weight);
                *(s.ptr++) = '0' + digit;
                s.length++;
            }
            if (m == 0 && n > 0) 
            {
                *(s.ptr++) = '.';
                s.length++;
            }
            m--;
        }
        if (useExp) 
        {
            // convert the exponent
            int i, j;
            *(s.ptr++) = 'e';
            s.length++;
            if (m1 > 0) 
            {
                *(s.ptr++) = '+';
                s.length++;
            } 
            else 
            {
                *(s.ptr++) = '-';
                s.length++;
                m1 = -m1;
            }
            m = 0;
            while (m1 > 0) 
            {
                *(s.ptr++) = '0' + m1 % 10;
                s.length++;
                m1 /= 10;
                m++;
            }
            s.ptr -= m;
            char tmp;
            for (i = 0, j = m-1; i<j; i++, j--) 
            {
                tmp = s.ptr[i];
                s.ptr[i] = s.ptr[j];
                s.ptr[j] = tmp;
            }
            s.ptr += m;
        }
    }
    
    size_t i;
    char* start = s.start;
    if(width > s.length) {
        for(i = 0; i < width - s.length; i++) {
            if(flags & ZEROPAD) *output_string->ptr++ = '0';
            else *output_string->ptr++ = ' ';
            output_string->length++;
        }
    }
    for(i = 0; i < s.length; i++) {
        *output_string->ptr++ = *start++;
    }
    output_string->length += s.length;

}

/**
 * Writes output to stdout.
 * A detailed description of the format is given in the
 * 'Linux Programmer's Manual'.
 *
 * @param format A string containing the output format, followed by an\
 argument list containing different variables for output
 * @return The number of characters printed or the number of characters that\
 would have been printed if the output was truncated, a negative\
 value is returned on failure
 *
 */
extern int printf(const char *format, ...)
{
// no dynamic memory allocation available yet
#define STATIC_MEMORY__

  c_string output_string;
  int character_count = 256;
  output_string.size = character_count;

#ifdef STATIC_MEMORY__
  char buffer[character_count];

  output_string.start = (char *) &buffer;
#else
  output_string.start = (char *) malloc(output_string.size * sizeof(char));
#endif // STATIC_MEMORY__

  output_string.ptr = output_string.start;
  output_string.length = 0;


  va_list args;

  va_start(args, format);

  // format handling taken from vkprintf
  while (format && *format)
  {
    if(!character_count)
    {
#ifdef STATIC_MEMORY__
      break;
#else
      // resize output string if necessary
      character_count = output_string.size;
      resizeString(&output_string, output_string.size * 2);
#endif // STATIC_MEMORY__
    }

    if (*format == '%')
    {
      int width = 0;
      int precision = 14;
      unsigned char flag = 0;
      ++format;
      while (1)
      {
        switch (*format) // prefix specifiers (there might be multiple)
        {
          case '-':
            flag |= LEFT;
            ++format;
            continue;
          case '+':
            flag |= PLUS;
            ++format;
            continue;
          case '0':
            flag |= ZEROPAD;
            ++format;
            continue;
          case 'z':
          case 'l':
            flag |= LONG;
            ++format;
            continue;
          default:
            break;
        }
        if (width)
          break; // only look for width specifier if we didn't have one yet
        
        size_t c = 0;
        char num[4];
        for(; *format >= (c ? '0' : '1') && *format <= '9'; ++format, ++c)
          if( c < 4 )
            num[c] = *format;
        num[c < 4 ? c : 3] = 0;
        if( c )
        {
          width = atoi(num);

#ifdef STATIC_MEMORY__
          if(character_count < width)
            width = character_count;
#else
          while(character_count < width)
          {
            character_count = output_string.size;
            resizeString(&output_string, output_string.size * 2);
          }
#endif // STATIC_MEMORY__

          continue; // there might be another prefix character after this...
        }
        
        break; // prefix is done
      }
      
      if(*format == '.') {
        ++format; 
        char num[4];
        size_t c = 0;
        for(; *format >= (c ? '0' : '1') && *format <= '9'; ++format, ++c)
            if( c < 4 )
                num[c] = *format;
        num[c < 4 ? c : 3] = 0;
        if( c )
        {
            precision = atoi(num);
        }
      }
      
      //handle diouxXfeEgGcs
      switch (*format)
      {
        case '%':
          *output_string.ptr++ = *format;

          --character_count;
          ++output_string.length;
          break;

        case 's':
        {
          char const *string_arg = va_arg(args, char const*);
          int len = strlen(string_arg);

          // we should align right -> fill with spaces
          if( !(flag & LEFT) && (len < width) )
          {
            character_count -= width - len;
            if( character_count < 0 )
            {
#ifdef STATIC_MEMORY__
              break;
#else
              // resize output string if necessary
              character_count = output_string.size;
              resizeString(&output_string, output_string.size * 2);
#endif // STATIC_MEMORY__
            }

            writeFillChars(&output_string, width - len, ' ');
          }

          // now print the string
          while(string_arg && *string_arg)
          {
            if(!character_count)
            {
#ifdef STATIC_MEMORY__
              break;
#else
              // resize output string if necessary
              character_count = output_string.size;
              resizeString(&output_string, output_string.size * 2);
#endif // STATIC_MEMORY__
            }


            *output_string.ptr++ = *string_arg++;
            --character_count;
            ++output_string.length;
          }

          // and some fillchars if aligned on the left
          if( flag & LEFT && len < width )
          {
            character_count -= width - len;
            if( character_count < 0 )
            {
#ifdef STATIC_MEMORY__
              break;
#else
              // resize output string if necessary
              character_count = output_string.size;
              resizeString(&output_string, output_string.size * 2);
#endif // STATIC_MEMORY__
            }

            writeFillChars(&output_string, width - len, ' ');
          }

          break;
        }

        //signed decimal
        case 'd':
          writeNumber(&output_string,(size_t) va_arg(args,size_t),10,width, 0, flag | SIGN);
          break;

        //we don't do i until I see what it actually should do
        //case 'i':
        //  break;

        //octal
        case 'o':
          writeNumber(&output_string,(size_t) va_arg(args,size_t),8,width, 0, flag | SPECIAL);
          break;

        //unsigned
        case 'u':
          writeNumber(&output_string,(size_t) va_arg(args,size_t),10,width, 0, flag );
          break;

        case 'p':
        case 'x':
          writeNumber(&output_string,(size_t) va_arg(args,size_t),16,width, 0, flag | SPECIAL);
          break;

        case 'X':
          writeNumber(&output_string,(size_t) va_arg(args,size_t), 16, width, 0, flag | SPECIAL | LARGE);
          break;

        //float
        case 'f':
          writeFloat(&output_string,(double) va_arg(args,double), width, precision, flag);
          break;
          
        case 'F':
          writeFloat(&output_string,(double) va_arg(args,double), width, precision, flag | LARGE);
          break;            

        //no scientific notation (yet)
        //case 'e':
        //  break;

        //case 'E':
        //  break;

        //no floating point yet
        //case 'g':
        //  break;

        //case 'G':
        //  break;

        //we don't do unicode (yet)
        case 'c':
          *output_string.ptr++ = (char) va_arg(args,unsigned int);
          ++output_string.length;
          break;

        default:
          //jump over unknown arg
          //++args;
          *output_string.ptr++ = '%';
          ++output_string.length;
          break;
      }

    }
    else
    {
      *output_string.ptr++ = *format;
      --character_count;
      ++output_string.length;
    }

    ++format;
  }

  va_end(args);

  character_count = write(STDOUT_FILENO,
                          (void*) output_string.start, output_string.length);

#ifndef STATIC_MEMORY__
  free(output_string.start);
#endif // STATIC_MEMORY__

  return (int) character_count;
}


/**
 * Writes the given character to stdout.
 * The character is casted to unsigned char.
 *
 * @param character The character for writing
 * @return The character written as unsigned char cast to int or EOF on error
 *
 */
int putchar(int character)
{
  unsigned char output_char = (unsigned char) character;
  int characters_written = write(STDOUT_FILENO, (void*) &output_char, 1);

  if(!characters_written || (characters_written == -1))
    return EOF;

  return (int) output_char;
}

/**
 * Writes the given string followed by a newline to stdout.
 *
 * @param output_string The string for writing
 * @return A non-negative number on success or EOF on error
 *
 */
int puts(const char *output_string)
{
  unsigned char newline = '\n';
  const char *string_ptr = output_string;
  size_t string_length = 0;
  int characters_written = 0;

  while(string_ptr && *string_ptr++)
    ++string_length;

  if(string_length)
  {
    characters_written = write(STDOUT_FILENO, (void*) output_string, string_length);
    if(!characters_written || (characters_written == -1))
      return EOF;
  }

  characters_written = write(STDOUT_FILENO, (void*) &newline, 1);

  if(!characters_written || (characters_written == -1))
    return EOF;

  return 0;
}

