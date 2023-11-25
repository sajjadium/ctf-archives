// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#include "cmemlink.h"
//#include "ofstream.h"
#include "strmsize.h"
#include "ualgo.h"
#include "panic.h"

namespace ustl {

/// \brief Attaches the object to pointer \p p of size \p n.
///
/// If \p p is nullptr and \p n is non-zero, bad_alloc is thrown and current
/// state remains unchanged.
///
void cmemlink::link (const void* p, size_type n)
{
    if (!p && n)
      kpanict("bad_alloc");
      //throw bad_alloc (n);
    unlink();
    relink (p, n);
}

/// Writes the object to stream \p os
/*void cmemlink::write (ostream& os) const
{
    const written_size_type sz (size());
    assert (sz == size() && "No support for writing memblocks larger than 4G");
    os << sz;
    os.write (cdata(), sz);
    os.align (stream_align_of (sz));
}

/// Writes the object to stream \p os
void cmemlink::text_write (ostringstream& os) const
{
    os.write (begin(), readable_size());
}*/

/// Returns the number of bytes required to write this object to a stream.
cmemlink::size_type cmemlink::stream_size (void) const noexcept
{
    const written_size_type sz (size());
    return Align (stream_size_of (sz) + sz, stream_align_of(sz));
}

/// Writes the data to file \p "filename".
/*void cmemlink::write_file (const char* filename, int mode) const
{
    fstream f;
    f.exceptions (fstream::allbadbits);
    f.open (filename, fstream::out | fstream::trunc, mode);
    f.write (cdata(), readable_size());
    f.close();
}*/

/// Compares to memory block pointed by l. Size is compared first.
bool cmemlink::operator== (const cmemlink& l) const noexcept
{
    return l._size == _size &&
	    (l._data == _data || 0 == memcmp (l._data, _data, _size));
}

} // namespace ustl
