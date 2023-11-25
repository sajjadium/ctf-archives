// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "uvector.h"
#include "uctralgo.h"

namespace ustl {

/// \class list ulist.h ustl.h
/// \ingroup Sequences
///
/// \brief Linked list, defined as an alias to vector.
///
template <typename T>
class list : public vector<T> {
public:
    typedef typename vector<T>::size_type	size_type;
    typedef typename vector<T>::iterator	iterator;
    typedef typename vector<T>::const_iterator	const_iterator;
    typedef typename vector<T>::reference	reference;
    typedef typename vector<T>::const_reference	const_reference;
public:
    inline			list (void)			: vector<T> () {}
    inline explicit		list (size_type n)		: vector<T> (n) {}
    inline			list (size_type n, const T& v)	: vector<T> (n, v) {}
    inline			list (const list<T>& v)		: vector<T> (v) {}
    inline			list (const_iterator i1, const_iterator i2)	: vector<T> (i1, i2) {}
    inline size_type		size (void) const		{ return vector<T>::size(); }
    inline iterator		begin (void)			{ return vector<T>::begin(); }
    inline const_iterator	begin (void) const		{ return vector<T>::begin(); }
    inline iterator		end (void)			{ return vector<T>::end(); }
    inline const_iterator	end (void) const		{ return vector<T>::end(); }
    inline void			push_front (const T& v)		{ this->insert (begin(), v); }
    inline void			pop_front (void)		{ this->erase (begin()); }
    inline const_reference	front (void) const		{ return *begin(); }
    inline reference		front (void)			{ return *begin(); }
    inline void			remove (const T& v)		{ ::ustl::remove (*this, v); }
    template <typename Predicate>
    inline void			remove_if (Predicate p)		{ ::ustl::remove_if (*this, p); }
    inline void			reverse (void)			{ ::ustl::reverse (*this); }
    inline void			unique (void)			{ ::ustl::unique (*this); }
    inline void			sort (void)			{ ::ustl::sort (*this); }
    void			merge (list<T>& l);
    void			splice (iterator ip, list<T>& l, iterator first = nullptr, iterator last = nullptr);
#if HAVE_CPP11
    inline			list (list&& v)			: vector<T> (move(v)) {}
    inline			list (std::initializer_list<T> v) : vector<T>(v) {}
    inline list&		operator= (list&& v)		{ vector<T>::operator= (move(v)); return *this; }
    template <typename... Args>
    inline void			emplace_front (Args&&... args)	{ vector<T>::emplace (begin(), forward<Args>(args)...); }
    inline void			push_front (T&& v)		{ emplace_front (move(v)); }
#endif
};

/// Merges the contents with \p l. Assumes both lists are sorted.
template <typename T>
void list<T>::merge (list& l)
{
    this->insert_space (begin(), l.size());
    ::ustl::merge (this->iat(l.size()), end(), l.begin(), l.end(), begin());
}

/// Moves the range [first, last) from \p l to this list at \p ip.
template <typename T>
void list<T>::splice (iterator ip, list<T>& l, iterator first, iterator last)
{
    if (!first)
	first = l.begin();
    if (!last)
	last = l.end();
    this->insert (ip, first, last);
    l.erase (first, last);
}

#if HAVE_CPP11
    template <typename T> using deque = list<T>;
#else
    #define deque list ///< list has all the functionality provided by deque
#endif


} // namespace ustl
