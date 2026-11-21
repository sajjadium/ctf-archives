// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#include "mistream.h"
#include "sostream.h"
//#include "ustdxept.h"
#include "ustring.h"
#include "ualgo.h"
#include "kprintf.h"
#include "panic.h"

namespace ustl {

//--------------------------------------------------------------------

/// Checks that \p n bytes are available in the stream, or else throws.
void ios_base::overrun (__attribute__((unused)) const char* op, __attribute__((unused)) const char* type, __attribute__((unused)) uint32_t n, __attribute__((unused)) uint32_t pos, uint32_t rem)
{
    if (set_and_throw (rem ? failbit : (failbit | eofbit)))
            /*  throw stream_bounds_exception (op, type, pos, n, rem)*/{ kprintfd("ERROR stream_bounds_exception: %s:%d", __FILE__, __LINE__); kpanict("ERROR stream_bounds_exception " LOCATION); }
}

//--------------------------------------------------------------------

/// Attaches to the block pointed to by source of size source.pos()
istream::istream (const ostream& source) noexcept
: cmemlink (source.begin(), source.pos())
,_pos (0)
{
}

void istream::unlink (void) noexcept		{ cmemlink::unlink(); _pos = 0; }
void ostream::unlink (void) noexcept		{ memlink::unlink(); _pos = 0; }

/// Writes all unread bytes into \p os.
void istream::write (ostream& os) const
{
    os.write (ipos(), remaining());
}

/// Writes the object to stream \p os.
/*void istream::text_write (ostringstream& os) const
{
    os.write (ipos(), remaining());
}*/

/// Reads a null-terminated string into \p str.
void istream::read_strz (string& str)
{
    const_iterator zp = find (ipos(), end(), '\0');
    if (zp == end())
	zp = ipos();
    const size_type strl = distance (ipos(), zp);
    str.assign (ipos(), strl);
    _pos += strl + 1;
}

/// Reads at most \p n bytes into \p s.
istream::size_type istream::readsome (void* s, size_type n)
{
    if (remaining() < n)
	underflow (n);
    const size_type ntr (min (n, remaining()));
    read (s, ntr);
    return ntr;
}

streamsize istream::underflow (streamsize n)
{
    verify_remaining ("read", "byte", n);
    return remaining();
}

//--------------------------------------------------------------------

/// Aligns the write pointer on \p grain. The skipped bytes are zeroed.
void ostream::align (size_type grain)
{
    assert (!((grain-1)&grain) && "grain must be a power of 2");
    iterator ip = ipos();
    iterator ipa = iterator((uintptr_t(ip) + (grain-1)) & ~(grain-1));
    size_t nb = distance (ip, ipa);
#if WANT_STREAM_BOUNDS_CHECKING
    if (!verify_remaining ("align", "padding", nb))
	return;
#else
    assert (remaining() >= nb && "Buffer overrun. Check your stream size calculations.");
#endif
    memset (ip, '\x0', nb);
    _pos += nb;
}

/// Writes \p str as a null-terminated string.
void ostream::write_strz (const char* str)
{
    write (str, strlen(str)+1);
}

/// Writes all available data from \p is.
void ostream::read (istream& is)
{
    write (is.ipos(), is.remaining());
    is.seek (is.size());
}

/// Writes all written data to \p os.
/*void ostream::text_write (ostringstream& os) const
{
    os.write (begin(), pos());
}*/

/// Inserts an empty area of \p size, at \p start.
void ostream::insert (iterator start, size_type s)
{
    _pos += s;
    memlink::insert (start, s);
}

/// Erases an area of \p size, at \p start.
void ostream::erase (iterator start, size_type s)
{
    _pos -= s;
    memlink::erase (start, s);
}

//--------------------------------------------------------------------

} // namespace ustl
