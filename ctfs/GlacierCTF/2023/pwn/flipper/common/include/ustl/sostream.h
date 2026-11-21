// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "ustring.h"
#include "mostream.h"

namespace ustl {

class string;

/// \class ostringstream sostream.h ustl.h
/// \ingroup TextStreams
///
/// \brief This stream writes textual data into a memory block.
///
class ostringstream : public ostream {
public:
				ostringstream (const string& v = "");
				ostringstream (void* p, size_t n) noexcept;
    inline fmtflags		flags (void) const		{ return _flags; }
    inline fmtflags		flags (fmtflags f)		{ fmtflags of (_flags); _flags.f = f.f; return of; }
    inline fmtflags		setf (fmtflags f)		{ fmtflags of (_flags); _flags.f |= f.f; return of; }
    inline fmtflags		unsetf (fmtflags f)		{ fmtflags of (_flags); _flags.f &= ~f.f; return of; }
    inline fmtflags		setf (fmtflags f, fmtflags m)	{ unsetf(m); return setf(f); }
    void			iwrite (unsigned char v);
    void			iwrite (wchar_t v);
    inline void			iwrite (char v)			{ iwrite (static_cast<unsigned char>(v)); }
    inline void			iwrite (short v)		{ iformat (v); }
    inline void			iwrite (unsigned short v)	{ iformat (v); }
    inline void			iwrite (int v)			{ iformat (v); }
    inline void			iwrite (unsigned int v)		{ iformat (v); }
    inline void			iwrite (long int v)		{ iformat (v); }
    inline void			iwrite (unsigned long int v)	{ iformat (v); }
    /*inline void			iwrite (float v)		{ iformat (v); }
    inline void			iwrite (double v)		{ iformat (v); }
    inline void			iwrite (long double v)		{ iformat (v); }*/
    void			iwrite (bool v);
    inline void			iwrite (const char* s)		{ write (s, strlen(s)); }
    inline void			iwrite (const unsigned char* s)	{ iwrite (reinterpret_cast<const char*>(s)); }
    inline void			iwrite (const string& v)	{ write (v.begin(), v.size()); }
    inline void			iwrite (fmtflags_bits f);
#if HAVE_THREE_CHAR_TYPES
    inline void			iwrite (signed char v)		{ iwrite (static_cast<char>(v)); }
#endif
#if HAVE_LONG_LONG
    inline void			iwrite (long long v)		{ iformat (v); }
    inline void			iwrite (unsigned long long v)	{ iformat (v); }
#endif
    inline size_type		max_size (void) const		{ return _buffer.max_size(); }
    inline ostringstream&	put (char c)			{ iwrite (uint8_t(c)); return *this; }
    int				vformat (const char* fmt, va_list args);
    int				format (const char* fmt, ...) __attribute__((__format__(__printf__, 2, 3)));
    inline uint16_t		width (void) const		{ return _width; }
    inline void			width (uint16_t w)		{ _width = w; }
    inline void			set_width (uint16_t w)		{ _width = w; }
    inline char			fill (void) const		{ return _fill; }
    inline void			fill (char c)			{ _fill = c; }
    inline uint8_t		precision (void) const		{ return _precision; }
    inline void			precision (uint8_t v)		{ _precision = v; }
    inline void			set_precision (uint8_t v)	{ _precision = v; }
    void			link (void* p, size_type n) noexcept;
    inline void			link (memlink& l)		{ link (l.data(), l.writable_size()); }
    inline const string&	str (void)			{ flush(); return _buffer; }
    void			str (const string& s);
    ostringstream&		write (const void* buffer, size_type size);
    inline ostringstream&	write (const cmemlink& buf)	{ return write (buf.begin(), buf.size()); }
    inline ostringstream&	seekp (off_t p, seekdir d =beg)	{ ostream::seekp(p,d); return *this; }
    virtual ostream&		flush (void) override		{ ostream::flush(); _buffer.resize (pos()); return *this; }
    virtual size_type		overflow (size_type n = 1) override;
protected:
    inline void			reserve (size_type n)		{ _buffer.reserve (n, false); }
    inline size_type		capacity (void) const		{ return _buffer.capacity(); }
private:
    inline void			write_strz (const char*)	{ assert (!"Writing nul characters into a text stream is not allowed"); }
    inline char*		encode_dec (char* fmt, uint32_t n) const noexcept;
    void			fmtstring (char* fmt, const char* typestr, bool bInteger) const;
    template <typename T>
    void			iformat (T v);
private:
    string			_buffer;	///< The output buffer.
    fmtflags			_flags;		///< See ios_base::fmtflags.
    uint16_t			_width;		///< Field width.
    uint8_t			_precision;	///< Number of digits after the decimal separator.
    char			_fill;		///< Character for padding variable width fields (space or 0 only)
};

//----------------------------------------------------------------------

template <typename T>
inline const char* printf_typestring (const T&)	{ return ""; }
#define PRINTF_TYPESTRING_SPEC(type,str)	\
template <> inline const char* printf_typestring (const type&)	{ return str; }
PRINTF_TYPESTRING_SPEC (short,		"hd")
PRINTF_TYPESTRING_SPEC (unsigned short,	"hu")
PRINTF_TYPESTRING_SPEC (int,		"d")
PRINTF_TYPESTRING_SPEC (unsigned int,	"u")
PRINTF_TYPESTRING_SPEC (long,		"ld")
PRINTF_TYPESTRING_SPEC (unsigned long,	"lu")
/*PRINTF_TYPESTRING_SPEC (float,		"f")
PRINTF_TYPESTRING_SPEC (double,		"lf")
PRINTF_TYPESTRING_SPEC (long double,	"Lf")*/
#if HAVE_LONG_LONG
PRINTF_TYPESTRING_SPEC (long long,	"lld")
PRINTF_TYPESTRING_SPEC (unsigned long long, "llu")
#endif
#undef PRINTF_TYPESTRING_SPEC

template <typename T>
void ostringstream::iformat (T v)
{
    char fmt [16];
    fmtstring (fmt, printf_typestring(v), numeric_limits<T>::is_integer);
    format (fmt, v);
}

void ostringstream::iwrite (fmtflags_bits f)
{
    if (f & basefield) setf (f, basefield);
    else if (f & floatfield) setf (f, floatfield);
    else if (f & adjustfield) setf (f, adjustfield);
    setf (f);
}

//----------------------------------------------------------------------

template <typename T> struct object_text_writer {
    inline void operator()(ostringstream& os, const T& v) const { v.text_write (os); }
};
template <typename T> struct integral_text_object_writer {
    inline void operator()(ostringstream& os, const T& v) const { os.iwrite (v); }
};
template <typename T>
inline ostringstream& operator<< (ostringstream& os, const T& v) {
    typedef typename tm::Select <tm::TypeTraits<T>::isFundamental
					|| tm::TypeTraits<T>::isPointer
					|| tm::Conversion<T,long>::exists,
	integral_text_object_writer<T>, object_text_writer<T> >::Result object_writer_t;
    object_writer_t()(os, v);
    return os;
}
// Needed because if called with a char[], numeric_limits will not work. Should be removed if I find out how to partial specialize for arrays...
inline ostringstream& operator<< (ostringstream& os, const char* v)
    { os.iwrite (v); return os; }
inline ostringstream& operator<< (ostringstream& os, char* v)
    { os.iwrite (v); return os; }

//----------------------------------------------------------------------
// Object writer operators

template <> struct object_text_writer<string> {
    inline void operator()(ostringstream& os, const string& v) const { os.iwrite (v); }
};
template <typename T> struct integral_text_object_writer<T*> {
    inline void operator() (ostringstream& os, const T* const& v) const
	{ os.iwrite (uintptr_t(v)); }
};

//----------------------------------------------------------------------
// Manipulators

namespace {
static constexpr const struct Sendl {
    inline constexpr Sendl (void) {}
    inline void text_write (ostringstream& os) const	{ os << '\n'; os.flush(); }
    inline void write (ostream& os) const		{ os.iwrite ('\n'); }
} endl;
static constexpr const struct Sflush {
    inline constexpr Sflush (void) {}
    inline void text_write (ostringstream& os) const	{ os.flush(); }
    inline void write (ostringstream& os) const		{ os.flush(); }
    inline void write (ostream&) const			{ }
} flush;
constexpr const char ends = '\0';		///< End of string character.
} // namespace

struct setiosflags {
    inline constexpr setiosflags (ios_base::fmtflags f) : _f(f) {}
    inline void text_write (ostringstream& os) const	{ os.setf(_f); }
private:
    const ios_base::fmtflags _f;
};
struct resetiosflags {
    inline constexpr resetiosflags (ios_base::fmtflags f) : _f(f) {}
    inline void text_write (ostringstream& os) const	{ os.unsetf(_f); }
private:
    const ios_base::fmtflags _f;
};
class setw {
    uint16_t _w;
public:
    inline constexpr setw (uint16_t w)			: _w(w) {}
    inline void text_write (ostringstream& os) const	{ os.width(_w); }
    inline void write (ostringstream& os) const		{ os.width(_w); }
};
class setfill {
    char _c;
public:
    inline constexpr setfill (char c)			: _c(c) {}
    inline void text_write (ostringstream& os) const	{ os.fill(_c); }
    inline void write (ostringstream& os) const		{ os.fill(_c); }
};
class setprecision {
    uint8_t _p;
public:
    inline constexpr setprecision (uint8_t p)		: _p(p) {}
    inline void text_write (ostringstream& os) const	{ os.precision(_p); }
    inline void write (ostringstream& os) const		{ os.precision(_p); }
};

} // namespace ustl
