// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#include "mistream.h"	// for istream_iterator, referenced in utf8.h
#include "sostream.h"
#include "ustring.h"
#include "ulimits.h"
#include "ustringformat.h"
//#include <stdio.h>

namespace ustl {

/// Creates an output string stream linked to the given memory area.
ostringstream::ostringstream (void* p, size_t n) noexcept
: ostream()
,_buffer()
,_flags (0)
,_width (0)
,_precision (2)
,_fill (0)
{
    exceptions (goodbit);
    link (p, n);
}

/// Creates an output string stream, initializing the buffer with v.
ostringstream::ostringstream (const string& v)
: ostream()
,_buffer (v)
,_flags (0)
,_width (0)
,_precision (2)
,_fill (0)
{
    exceptions (goodbit);
    ostream::link (_buffer);
}

/// Copies \p s to the internal buffer.
void ostringstream::str (const string& s)
{
    _buffer = s;
    ostream::link (_buffer);
    SetPos (_buffer.size());
}

/// Writes a single character into the stream.
void ostringstream::iwrite (unsigned char v)
{
    if (remaining() >= 1 || overflow() >= 1)
	ostream::iwrite (v);
}

/// Writes the contents of \p buffer of \p size into the stream.
ostringstream& ostringstream::write (const void* buffer, size_type sz)
{
    const char* buf = static_cast<const char*>(buffer);
    for (size_type bw = 0; (bw = min(sz, remaining() ? remaining() : overflow(sz))); buf += bw, sz -= bw)
	ostream::write (buf, bw);
    return *this;
}

/// Simple decimal encoding of \p n into \p fmt.
inline char* ostringstream::encode_dec (char* fmt, uint32_t n) const noexcept
{
    do {
	*fmt++ = '0' + n % 10;
    } while (n /= 10);
    return fmt;
}

/// Generates a sprintf format string for the given type.
void ostringstream::fmtstring (char* fmt, const char* typestr, bool bInteger) const
{
    *fmt++ = '%';
    if (_width) {
	if (_fill == '0')
	    *fmt++ = '0';
	fmt = encode_dec (fmt, _width);
    }
    if (_flags.f & left)
	*fmt++ = '-';
    if (bInteger) {
	if (_flags.f & showpos)
	    *fmt++ = '+';
	if (_flags.f & showbase)
	    *fmt++ = '#';
    } else {
	*fmt++ = '.';
	fmt = encode_dec (fmt, _precision);
    }
    while (*typestr)
	*fmt++ = *typestr++;
    if (bInteger) {
	if (_flags.f & hex)
	    fmt[-1] = (_flags.f & uppercase) ? 'X' : 'x';
	else if (_flags.f & oct)
	    fmt[-1] = 'o';
    } else if (_flags.f & scientific)
	fmt[-1] = 'E';
    *fmt = 0;
}

/// Writes \p v into the stream as utf8
void ostringstream::iwrite (wchar_t v)
{
    char buffer [8];
    *utf8out(buffer) = v;
    write (buffer, Utf8Bytes(v));
}

/// Writes value \p v into the stream as text.
void ostringstream::iwrite (bool v)
{
    static const char tf[2][8] = { "false", "true" };
    write (tf[v], 5 - v);
}

/// Equivalent to a vsprintf on the string.
int ostringstream::vformat (const char* fmt, va_list args)
{
#if HAVE_VA_COPY
    va_list args2;
#else
    #define args2 args
    #undef __va_copy
    #define __va_copy(x,y)
#endif
    int rv, space;
    do {
	space = remaining();
	__va_copy (args2, args);
	if (0 > (rv = vsnprintf (ipos(), space, fmt, args2)))
	    return rv;
    } while (rv >= space && rv < int(overflow(rv+1)));
    SetPos (pos() + min (rv, space));
    return rv;
}

/// Equivalent to a sprintf on the string.
int ostringstream::format (const char* fmt, ...)
{
    va_list args;
    va_start (args, fmt);
    const int rv = vformat (fmt, args);
    va_end (args);
    return rv;
}

/// Links to string \p l as resizable.
void ostringstream::link (void* p, size_type n) noexcept
{
    assert ((p || !n) && "The output string buffer must not be read-only");
    ostream::link (p, n);
    _buffer.link (p, n);
}

/// Attempts to create more output space. Returns remaining().
ostringstream::size_type ostringstream::overflow (size_type n)
{
    if (n > remaining() && (good() || n <= capacity() - pos())) {
	const uoff_t oldPos (pos());
	_buffer.reserve (oldPos + n, false);
	_buffer.resize (oldPos + n);
	ostream::link (_buffer);
	SetPos (oldPos);
    }
    verify_remaining ("write", "text", n);
    return remaining();
}

} // namespace ustl
