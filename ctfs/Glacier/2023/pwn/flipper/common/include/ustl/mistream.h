// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "memlink.h"
#include "strmsize.h"
#include "utf8.h"
#include "uios.h"
#if WANT_STREAM_BOUNDS_CHECKING
    #include "typeinfo.h"
#endif

namespace ustl {

class ostream;
class memlink;
class string;

/// \class istream mistream.h ustl.h
/// \ingroup BinaryStreams
///
/// \brief Helper class to read packed binary streams.
/// 
/// This class contains a set of functions to read integral types from an
/// unstructured memory block. Unpacking binary file data can be done this
/// way, for instance. aligning the data is your responsibility, and can
/// be accomplished by proper ordering of reads and by calling the align()
/// function. Unaligned access is usually slower by orders of magnitude and,
/// on some architectures, such as PowerPC, can cause your program to crash.
/// Therefore, all read functions have asserts to check alignment.
/// Overreading the end of the stream will also cause a crash (an assert in
/// debug builds). Oh, and don't be intimidated by the size of the inlines
/// here. In the assembly code the compiler will usually chop everything down
/// to five instructions each.
/// 
/// Alignment rules for your objects:
///	- Assume your writes start off 4-byte aligned.
///	- After completion, \ref istream::align the stream to at least 4.
///	- If data portability between 32bit and 64bit platforms is important
///	(it often is not, in config files and the like), ensure you are always
///	using fixed-size types and are aligning to a fixed grain. Avoid writing
///	8-byte types, and if you do, manually align before doing so.
///	- Non-default alignment is allowed if you plan to frequently write this
///	object in array form and alignment would be costly. For example, an
///	array of uint16_t-sized objects may leave the stream uint16_t aligned
///	as long as you know about it and will default-align the stream after
///	writing the array (note: \ref vector will already do this for you)
/// 
/// Example code:
/// \code
///     memblock b;
///     b.read_file ("test.file");
///     ostream is (b);
///     is >> boolVar >> ios::talign<int>();
///     is >> intVar >> floatVar;
///     is.read (binaryData, binaryDataSize);
///     is.align();
/// \endcode
///
class istream : public cmemlink, public ios_base {
public:
    inline		istream (void)				: cmemlink(), _pos (0) {}
    inline		istream (const void* p, streamsize n)	: cmemlink(p, n), _pos (0) {}
    inline explicit	istream (const cmemlink& source)	: cmemlink (source), _pos (0) {}
    explicit		istream (const ostream& source) noexcept;
    inline iterator	end (void) const			{ return cmemlink::end(); }
    inline void		link (const void* p, streamsize n)	{ cmemlink::link (p, n); }
    inline void		link (const cmemlink& l)		{ cmemlink::link (l.cdata(), l.readable_size()); }
    inline void		link (const void* f, const void* l)	{ cmemlink::link (f, l); }
    inline void		relink (const void* p, streamsize n)	{ cmemlink::relink (p, n); _pos = 0; }
    inline void		relink (const cmemlink& l)		{ relink (l.cdata(), l.readable_size()); }
    virtual void	unlink (void) noexcept override;
    virtual streamsize	underflow (streamsize = 1);
    inline uoff_t	pos (void) const	{ return _pos; }
    inline const_iterator ipos (void) const	{ return begin() + pos(); }
    inline streamsize	remaining (void) const	{ return size() - pos(); }
    inline void		seek (uoff_t newPos);
    inline void		iseek (const_iterator newPos);
    inline void		skip (streamsize nBytes);
    inline bool		aligned (streamsize grain = c_DefaultAlignment) const;
    inline bool		verify_remaining (const char* op, const char* type, streamsize n);
    inline streamsize	align_size (streamsize grain = c_DefaultAlignment) const;
    inline void		align (streamsize grain = c_DefaultAlignment);
    inline void		swap (istream& is);
    inline void		read (void* buffer, streamsize size);
    inline void		read (memlink& buf)	{ read (buf.begin(), buf.writable_size()); }
    void		read_strz (string& str);
    streamsize		readsome (void* s, streamsize n);
    inline void		read (istream&)			{ }
    void		write (ostream& os) const;
    void		text_write (ostringstream& os) const;
    inline streamsize	stream_size (void) const	{ return remaining(); }
    template <typename T>
    inline void		iread (T& v);
    inline void		ungetc (void)		{ seek (pos() - 1); }
    inline off_t	tellg (void) const	{ return pos(); }
    inline void		seekg (off_t p, seekdir d = beg);
private:
    streamoff		_pos;		///< The current read position.
};

//----------------------------------------------------------------------

template <typename T, typename Stream>
inline streamsize required_stream_size (T, const Stream&) { return 1; }
template <typename T>
inline streamsize required_stream_size (T v, const istream&) { return stream_size_of(v); }

template <typename Stream>
inline bool stream_at_eof (const Stream& stm)	{ return stm.eof(); }
template <>
inline bool stream_at_eof (const istream&)	{ return false; }

/// \class istream_iterator
/// \ingroup BinaryStreamIterators
///
/// \brief An iterator over an istream to use with uSTL algorithms.
///
template <typename T, typename Stream = istream>
class istream_iterator {
public:
    typedef T			value_type;
    typedef ptrdiff_t		difference_type;
    typedef const value_type*	pointer;
    typedef const value_type&	reference;
    typedef typename Stream::size_type	size_type;
    typedef input_iterator_tag	iterator_category;
public:
				istream_iterator (void)		: _pis (nullptr), _v() {}
    explicit			istream_iterator (Stream& is)	: _pis (&is), _v() { Read(); }
				istream_iterator (const istream_iterator& i)	: _pis (i._pis), _v (i._v) {}
    /// Reads and returns the next value.
    inline const T&		operator* (void)	{ return _v; }
    inline istream_iterator&	operator++ (void)	{ Read(); return *this; }
    inline istream_iterator&	operator-- (void)	{ _pis->seek (_pis->pos() - 2 * stream_size_of(_v)); return operator++(); }
    inline istream_iterator	operator++ (int)	{ istream_iterator old (*this); operator++(); return old; }
    inline istream_iterator	operator-- (int)	{ istream_iterator old (*this); operator--(); return old; }
    inline istream_iterator&	operator+= (streamsize n)	{ while (n--) operator++(); return *this; }
    inline istream_iterator&	operator-= (streamsize n)	{ _pis->seek (_pis->pos() - (n + 1) * stream_size_of(_v)); return operator++(); }
    inline istream_iterator	operator- (streamoff n) const			{ istream_iterator result (*this); return result -= n; }
    inline difference_type	operator- (const istream_iterator& i) const	{ return distance (i._pis->pos(), _pis->pos()) / stream_size_of(_v); }
    inline bool			operator== (const istream_iterator& i) const	{ return (!_pis && !i._pis) || (_pis && i._pis && _pis->pos() == i._pis->pos()); }
    inline bool			operator< (const istream_iterator& i) const	{ return !i._pis || (_pis && _pis->pos() < i._pis->pos()); }
private:
    void Read (void)
    {
	if (!_pis)
	    return;
	const streamsize rs (required_stream_size (_v, *_pis));
	if (_pis->remaining() < rs && _pis->underflow (rs) < rs) {
	    _pis = nullptr;
	    return;
	}
	*_pis >> _v;
	if (stream_at_eof (*_pis))
	    _pis = nullptr;
    }
private:
    Stream*	_pis;		///< The host stream.
    T		_v;		///< Last read value; cached to be returnable as a const reference.
};

//----------------------------------------------------------------------

/// Checks that \p n bytes are available in the stream, or else throws.
inline bool istream::verify_remaining (const char* op, const char* type, streamsize n)
{
    const streamsize rem = remaining();
    bool enough = n <= rem;
    if (!enough) overrun (op, type, n, pos(), rem);
    return enough;
}

/// Sets the current read position to \p newPos
inline void istream::seek (uoff_t newPos)
{
#if WANT_STREAM_BOUNDS_CHECKING
    if (newPos > size())
	return overrun ("seekg", "byte", newPos, pos(), size());
#else
    assert (newPos <= size());
#endif
    _pos = newPos;
}

/// Sets the current read position to \p newPos
inline void istream::iseek (const_iterator newPos)
{
    seek (distance (begin(), newPos));
}

/// Sets the current write position to \p p based on \p d.
inline void istream::seekg (off_t p, seekdir d)
{
    switch (d) {
	case beg:	seek (p); break;
	case cur:	seek (pos() + p); break;
	case ios_base::end:	seek (size() - p); break;
    }
}

/// Skips \p nBytes without reading them.
inline void istream::skip (streamsize nBytes)
{
    seek (pos() + nBytes);
}

/// Returns the number of bytes to skip to be aligned on \p grain.
inline streamsize istream::align_size (streamsize grain) const
{
    return Align (pos(), grain) - pos();
}

/// Returns \c true if the read position is aligned on \p grain
inline bool istream::aligned (streamsize grain) const
{
    return pos() % grain == 0;
}

/// aligns the read position on \p grain
inline void istream::align (streamsize grain)
{
    seek (Align (pos(), grain));
}

/// Reads type T from the stream via a direct pointer cast.
template <typename T>
inline void istream::iread (T& v)
{
    assert (aligned (stream_align_of (v)));
#if WANT_STREAM_BOUNDS_CHECKING
    if (!verify_remaining ("read", typeid(v).name(), sizeof(T)))
	return;
#else
    assert (remaining() >= sizeof(T));
#endif
    v = *reinterpret_cast<const T*>(ipos());
    _pos += sizeof(T);
}

/// Swaps contents with \p is
inline void istream::swap (istream& is)
{
    cmemlink::swap (is);
    ::ustl::swap (_pos, is._pos);
}

/// Reads \p n bytes into \p buffer.
inline void istream::read (void* buffer, size_type n)
{
#if WANT_STREAM_BOUNDS_CHECKING
    if (!verify_remaining ("read", "binary data", n))
	return;
#else
    assert (remaining() >= n && "Reading past end of buffer. Make sure you are reading the right format.");
#endif
    memcpy (reinterpret_cast<value_type*>(buffer), ipos(), n);
    _pos += n;
}

//----------------------------------------------------------------------

template <typename T> struct object_reader {
    inline void operator()(istream& is, T& v) const { v.read (is); }
};
template <typename T> struct integral_object_reader {
    inline void operator()(istream& is, T& v) const { is.iread (v); }
};
template <typename T>
inline istream& operator>> (istream& is, T& v) {
    typedef typename tm::Select <numeric_limits<T>::is_integral,
	integral_object_reader<T>, object_reader<T> >::Result object_reader_t;
    object_reader_t()(is, v);
    return is;
}
template <typename T>
inline istream& operator>> (istream& is, const T& v) { v.read (is); return is; }

//----------------------------------------------------------------------

typedef istream_iterator<utf8subchar_t> istream_iterator_for_utf8;
typedef utf8in_iterator<istream_iterator_for_utf8> utf8istream_iterator;

/// Returns a UTF-8 adaptor reading from \p is.
inline utf8istream_iterator utf8in (istream& is)
{
    istream_iterator_for_utf8 si (is);
    return utf8istream_iterator (si);
}

//----------------------------------------------------------------------

} // namespace ustl
