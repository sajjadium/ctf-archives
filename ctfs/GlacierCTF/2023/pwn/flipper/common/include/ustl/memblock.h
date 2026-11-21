// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "memlink.h"

namespace ustl {

/// \class memblock memblock.h ustl.h
/// \ingroup MemoryManagement
///
/// \brief Allocated memory block.
///
/// Adds memory management capabilities to memlink. Uses malloc and realloc to
/// maintain the internal pointer, but only if allocated using members of this class,
/// or if linked to using the Manage() member function. Managed memory is automatically
/// freed in the destructor.
///
class memblock : public memlink {
public:
				memblock (void) noexcept;
				memblock (const void* p, size_type n);
    explicit			memblock (size_type n);
    explicit			memblock (const cmemlink& b);
    explicit			memblock (const memlink& b);
				memblock (const memblock& b);
    virtual			~memblock (void) noexcept;
    virtual void		unlink (void) noexcept override;
    inline void			assign (const cmemlink& l)	{ assign (l.cdata(), l.readable_size()); }
    inline const memblock&	operator= (const cmemlink& l)	{ assign (l); return *this; }
    inline const memblock&	operator= (const memlink& l)	{ assign (l); return *this; }
    inline const memblock&	operator= (const memblock& l)	{ assign (l); return *this; }
    inline void			swap (memblock& l) noexcept	{ memlink::swap (l); ::ustl::swap (_capacity, l._capacity); }
    void			assign (const void* p, size_type n);
    void			reserve (size_type newSize, bool bExact = false);
    void			resize (size_type newSize, bool bExact = true);
    iterator			insert (const_iterator start, size_type size);
    iterator			erase (const_iterator start, size_type size);
    inline void			clear (void) noexcept		{ resize (0); }
    inline size_type		capacity (void) const		{ return _capacity; }
    inline bool			is_linked (void) const		{ return !capacity(); }
    inline size_type		max_size (void) const		{ return is_linked() ? memlink::max_size() : SIZE_MAX; }
    inline void			manage (memlink& l)		{ manage (l.begin(), l.size()); }
    void			deallocate (void) noexcept;
    void			shrink_to_fit (void);
    void			manage (void* p, size_type n) noexcept;
    void			copy_link (void);
    void			read (istream& is);
    void			read_file (const char* filename);
#if HAVE_CPP11
    inline			memblock (memblock&& b)		: memlink(), _capacity(0) { swap (b); }
    inline memblock&		operator= (memblock&& b)	{ swap (b); return *this; }
#endif
protected:
    virtual size_type		minimumFreeCapacity (void) const noexcept __attribute__((const));
private:
    size_type			_capacity;	///< Number of bytes allocated by Resize.
};

} // namespace ustl
