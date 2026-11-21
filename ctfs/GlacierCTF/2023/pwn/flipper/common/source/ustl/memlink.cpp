// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#include "memlink.h"
//#include "mistream.h"
//#include "ustdxept.h"

namespace ustl {

/// Reads the object from stream \p s
/*void memlink::read (istream& is)
{
    written_size_type n = 0;
    is >> n;
    if (!is.verify_remaining ("read", "ustl::memlink", n))
	return;
    if (n > size())
	throw length_error ("memlink can not increase the size of the linked storage for reading");
    resize (n);
    is.read (data(), n);
    is.align (stream_align_of (n));
}*/

/// Fills the linked block with the given pattern.
/// \arg start   Offset at which to start filling the linked block
/// \arg p       Pointer to the pattern.
/// \arg elSize  Size of the pattern.
/// \arg elCount Number of times to write the pattern.
/// Total number of bytes written is \p elSize * \p elCount.
///
void memlink::fill (const_iterator cstart, const void* p, size_type elSize, size_type elCount) noexcept
{
    assert (data() || !elCount || !elSize);
    assert (cstart >= begin() && cstart + elSize * elCount <= end());
    iterator start = const_cast<iterator>(cstart);
    if (elSize == 1)
	fill_n (start, elCount, *reinterpret_cast<const uint8_t*>(p));
    else while (elCount--)
	start = copy_n (const_iterator(p), elSize, start);
}

} // namespace ustl
