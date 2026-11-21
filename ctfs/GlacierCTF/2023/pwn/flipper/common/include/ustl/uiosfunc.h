// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "sostream.h"

namespace ustl {

class ios : public ios_base {
public:
    /// \class align uiosfunc.h ustl.h
    /// \ingroup StreamFunctors
    /// \brief Stream functor to allow inline align() calls.
    ///
    /// Example: os << ios::align(sizeof(uint16_t));
    ///
    class align {
    public:
	inline explicit		align (size_t grain = c_DefaultAlignment) : _grain(grain) {}
	inline istream&		apply (istream& is) const { is.align (_grain); return is; }
	inline ostream&		apply (ostream& os) const { os.align (_grain); return os; }
	inline void		read (istream& is) const  { apply (is); }
	inline void		write (ostream& os) const { apply (os); }
	inline size_t		stream_size (void) const  { return _grain - 1; }
    private:
	const size_t		_grain;
    };

    /// \class talign uiosfunc.h ustl.h
    /// \ingroup StreamFunctors
    /// \brief Stream functor to allow type-based alignment.
    template <typename T>
    class talign : public align {
    public:
	inline explicit		talign (void) : align (stream_align_of (NullValue<T>())) {}
    };

    /// \class skip uiosfunc.h ustl.h
    /// \ingroup StreamFunctors
    /// \brief Stream functor to allow inline skip() calls.
    ///
    /// Example: os << ios::skip(sizeof(uint16_t));
    ///
    class skip {
    public:
	inline explicit 	skip (size_t nBytes) : _nBytes(nBytes) {}
	inline istream&		apply (istream& is) const { is.skip (_nBytes); return is; }
	inline ostream&		apply (ostream& os) const { os.skip (_nBytes); return os; }
	inline void		read (istream& is) const  { apply (is); }
	inline void		write (ostream& os) const { apply (os); }
	inline size_t		stream_size (void) const  { return _nBytes; }
    private:
	const size_t		_nBytes;
    };

    /// \class width uiosfunc.h ustl.h
    /// \ingroup StreamFunctors
    /// \brief Stream functor to allow inline set_width() calls.
    ///
    /// Example: os << ios::width(15);
    ///
    class width {
    public:
	inline explicit		width (size_t nBytes) : _nBytes(nBytes) {}
	inline ostringstream&	apply (ostringstream& os) const { os.width (_nBytes); return os; }
	inline void		text_write (ostringstream& os) const { apply (os); }
    private:
	const size_t		_nBytes;
    };

    // Deprecated way to set output format base. Use setiosflags manipulator instead.
    struct base {
	inline explicit		base (size_t n) : _f (n == 16 ? hex : (n == 8 ? oct : dec)) {}
	inline void		text_write (ostringstream& os) const { os.setf (_f, basefield); }
    private:
	fmtflags		_f;
    };
};

} // namespace ustl
