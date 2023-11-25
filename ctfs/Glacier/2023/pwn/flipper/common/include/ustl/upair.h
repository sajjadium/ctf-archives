// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "ualgobase.h"

namespace ustl {

class istream;
class ostream;
class ostringstream;

/// \class pair upair.h ustl.h
/// \ingroup AssociativeContainers
///
/// \brief Container for two values.
///
template <typename T1, typename T2>
class pair {
public:
    typedef T1		first_type;
    typedef T2		second_type;
public:
    /// Default constructor.
    inline constexpr	pair (void)			: first (T1()), second (T2()) {}
    /// Initializes members with \p a, and \p b.
    inline		pair (const T1& a, const T2& b)	: first (a), second (b) {}
    template <typename T3, typename T4>
    inline		pair (const pair<T3,T4>& p2)	: first (p2.first), second (p2.second) {}
    inline pair&	operator= (const pair& p2)	{ first = p2.first; second = p2.second; return *this; }
    template <typename T3, typename T4>
    inline pair&	operator= (const pair<T3,T4>& p2) { first = p2.first; second = p2.second; return *this; }
    inline bool		operator== (const pair& v)const	{ return first == v.first && second == v.second; }
    inline bool		operator< (const pair& v) const	{ return first < v.first || (first == v.first && second < v.second); }
    inline void		swap (pair& v)			{ ::ustl::swap(first,v.first); ::ustl::swap(second,v.second); }
    inline void		read (istream& is);
    inline void		write (ostream& os) const;
    void		text_write (ostringstream& os) const;
    inline size_t	stream_size (void) const;
#if HAVE_CPP11
			pair (const pair&) = default;
			pair (pair&&) = default;
    template <typename T3, typename T4>
    inline		pair (T3&& a, T4&& b)		: first (forward<T3>(a)), second (forward<T4>(b)) {}
    template <typename T3, typename T4>
    inline		pair (pair<T3,T4>&& p2)		: first (forward<T3>(p2.first)), second (forward<T4>(p2.second)) {}
    inline pair&	operator= (pair&& p2)		{ first = move(p2.first); second = move(p2.second); return *this; }
    template <typename T3, typename T4>
    inline pair&	operator= (pair<T3,T4>&& p2)	{ first = forward<T3>(p2.first); second = forward<T4>(p2.second); return *this; }
    inline void		swap (pair&& v)			{ ::ustl::swap(first,v.first); ::ustl::swap(second,v.second); }
#endif
public:
    first_type		first;
    second_type		second;
};

#if HAVE_CPP11

/// Returns a pair object with (a,b)
template <typename T1, typename T2>
inline constexpr pair<T1,T2> make_pair (T1&& a, T2&& b)
    { return pair<T1,T2> (forward<T1>(a), forward<T2>(b)); }

#endif

/// Returns a pair object with (a,b)
template <typename T1, typename T2>
inline constexpr pair<T1,T2> make_pair (const T1& a, const T2& b)
    { return pair<T1,T2> (a, b); }

} // namespace ustl
