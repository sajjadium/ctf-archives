// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.
//
/// \file uiterator.h
/// \brief Contains various iterator adapters.

#pragma once
#include "utypes.h"

namespace ustl {

//----------------------------------------------------------------------

template <typename Category, typename T, typename Distance = ptrdiff_t, typename Pointer = T*, typename Reference = T&>
struct iterator {
    typedef T		value_type;
    typedef Distance	difference_type;
    typedef Pointer	pointer;
    typedef Reference	reference;
    typedef Category	iterator_category;
};

//----------------------------------------------------------------------

struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag {};
struct bidirectional_iterator_tag {};
struct random_access_iterator_tag {};

/// \struct iterator_traits uiterator.h ustl.h
/// \brief Contains the type traits of \p Iterator
///
template <typename Iterator>
struct iterator_traits {
    typedef typename Iterator::value_type	value_type;
    typedef typename Iterator::difference_type	difference_type;
    typedef typename Iterator::pointer		pointer;
    typedef typename Iterator::reference	reference;
    typedef typename Iterator::iterator_category iterator_category;
};

#ifndef DOXYGEN_SHOULD_SKIP_THIS

template <typename T>
struct iterator_traits<T*> {
    typedef T		value_type;
    typedef ptrdiff_t	difference_type;
    typedef const T*	const_pointer;
    typedef T*		pointer;
    typedef const T&	const_reference;
    typedef T&		reference;
    typedef random_access_iterator_tag	iterator_category;
};

template <typename T>
struct iterator_traits<const T*> {
    typedef T		value_type;
    typedef ptrdiff_t	difference_type;
    typedef const T*	const_pointer;
    typedef const T*	pointer;
    typedef const T&	const_reference;
    typedef const T&	reference;
    typedef random_access_iterator_tag	iterator_category;
};

template <>
struct iterator_traits<void*> {
    typedef uint8_t		value_type;
    typedef ptrdiff_t		difference_type;
    typedef const void*		const_pointer;
    typedef void*		pointer;
    typedef const value_type&	const_reference;
    typedef value_type&		reference;
    typedef random_access_iterator_tag	iterator_category;
};

template <>
struct iterator_traits<const void*> {
    typedef uint8_t		value_type;
    typedef ptrdiff_t		difference_type;
    typedef const void*		const_pointer;
    typedef const void*		pointer;
    typedef const value_type&	const_reference;
    typedef const value_type&	reference;
    typedef random_access_iterator_tag	iterator_category;
};

#endif

//----------------------------------------------------------------------

/// \class reverse_iterator uiterator.h ustl.h
/// \ingroup IteratorAdaptors
/// \brief Wraps \p Iterator to behave in an exactly opposite manner.
///
template <typename Iterator>
class reverse_iterator {
public:
    typedef typename iterator_traits<Iterator>::value_type	value_type;
    typedef typename iterator_traits<Iterator>::difference_type	difference_type;
    typedef typename iterator_traits<Iterator>::pointer		pointer;
    typedef typename iterator_traits<Iterator>::reference	reference;
    typedef typename iterator_traits<Iterator>::iterator_category iterator_category;
public:
				reverse_iterator (void) : _i() {}
    explicit			reverse_iterator (Iterator iter) : _i (iter) {}
    inline bool			operator== (const reverse_iterator& iter) const { return _i == iter._i; }
    inline bool			operator< (const reverse_iterator& iter) const { return iter._i < _i; }
    inline Iterator		base (void) const { return _i; }
    inline reference		operator* (void) const { Iterator prev (_i); --prev; return *prev; }
    inline pointer		operator-> (void) const { return &(operator*()); }
    inline reverse_iterator&	operator++ (void) { -- _i; return *this; }
    inline reverse_iterator&	operator-- (void) { ++ _i; return *this; }
    inline reverse_iterator	operator++ (int) { reverse_iterator prev (*this); -- _i; return prev; }
    inline reverse_iterator	operator-- (int) { reverse_iterator prev (*this); ++ _i; return prev; }
    inline reverse_iterator&	operator+= (size_t n) { _i -= n; return *this; }
    inline reverse_iterator&	operator-= (size_t n) { _i += n; return *this; }
    inline reverse_iterator	operator+ (size_t n) const { return reverse_iterator (_i - n); }
    inline reverse_iterator	operator- (size_t n) const { return reverse_iterator (_i + n); }
    inline reference		operator[] (uoff_t n) const { return *(*this + n); }
    inline difference_type	operator- (const reverse_iterator& i) const { return distance (i._i, _i); }
protected:
    Iterator			_i;
};

template <typename Iterator>
inline reverse_iterator<Iterator> make_reverse_iterator (Iterator i)
    { return reverse_iterator<Iterator>(i); }

//----------------------------------------------------------------------
#if HAVE_CPP11

/// \class move_iterator uiterator.h ustl.h
/// \ingroup IteratorAdaptors
/// \brief Wraps \p Iterator to behave in an exactly opposite manner.
///
template <typename Iterator>
class move_iterator {
public:
    using value_type		= typename iterator_traits<Iterator>::value_type;
    using difference_type	= typename iterator_traits<Iterator>::difference_type;
    using pointer		= typename iterator_traits<Iterator>::pointer;
    using reference		= value_type&&;
    using iterator_category	= typename iterator_traits<Iterator>::iterator_category;
public:
				move_iterator (void)		: _i() {}
    explicit			move_iterator (Iterator iter)	: _i (iter) {}
    inline bool			operator== (const move_iterator& iter) const	{ return _i == iter._i; }
    inline bool			operator< (const move_iterator& iter) const	{ return _i < iter._i; }
    inline Iterator		base (void) const		{ return _i; }
    inline reference		operator* (void) const		{ return move(*_i); }
    inline pointer		operator-> (void) const		{ return &*_i; }
    inline move_iterator&	operator++ (void)		{ ++_i; return *this; }
    inline move_iterator&	operator-- (void)		{ --_i; return *this; }
    inline move_iterator	operator++ (int)		{ move_iterator r (*this); ++ _i; return r; }
    inline move_iterator	operator-- (int)		{ move_iterator r (*this); -- _i; return r; }
    inline move_iterator&	operator+= (size_t n)		{ _i += n; return *this; }
    inline move_iterator&	operator-= (size_t n)		{ _i -= n; return *this; }
    inline move_iterator	operator+ (size_t n) const	{ return move_iterator (_i - n); }
    inline move_iterator	operator- (size_t n) const	{ return move_iterator (_i + n); }
    inline reference		operator[] (uoff_t n) const	{ return move(*(*this + n)); }
    inline difference_type	operator- (const move_iterator& i) const	{ return distance (_i, i._i); }
protected:
    Iterator			_i;
};

template <typename Iterator>
inline move_iterator<Iterator> make_move_iterator (Iterator i)
    { return move_iterator<Iterator>(i); }

#endif
//----------------------------------------------------------------------

/// \class insert_iterator uiterator.h ustl.h
/// \ingroup IteratorAdaptors
/// \brief Calls insert on bound container for each assignment.
///
template <typename Container>
class insert_iterator {
public:
    typedef typename Container::value_type	value_type;
    typedef typename Container::difference_type	difference_type;
    typedef typename Container::pointer		pointer;
    typedef typename Container::reference	reference;
    typedef typename Container::iterator	iterator;
    typedef output_iterator_tag			iterator_category;
public:
    explicit			insert_iterator (Container& ctr, iterator ip) : _rctr (ctr), _ip (ip) {}
    inline insert_iterator&	operator= (typename Container::const_reference v)
				    { _ip = _rctr.insert (_ip, v); return *this; }
    inline insert_iterator&	operator* (void)  { return *this; }
    inline insert_iterator&	operator++ (void) { ++ _ip; return *this; }
    inline insert_iterator	operator++ (int)  { insert_iterator prev (*this); ++_ip; return prev; }
protected:
    Container&			_rctr;
    iterator			_ip;
};

/// Returns the insert_iterator for \p ctr.
template <typename Container>
inline insert_iterator<Container> inserter (Container& ctr, typename Container::iterator ip)
    { return insert_iterator<Container> (ctr, ip); }

//----------------------------------------------------------------------

/// \class back_insert_iterator uiterator.h ustl.h
/// \ingroup IteratorAdaptors
/// \brief Calls push_back on bound container for each assignment.
///
template <class Container>
class back_insert_iterator {
public:
    typedef typename Container::value_type	value_type;
    typedef typename Container::difference_type	difference_type;
    typedef typename Container::pointer		pointer;
    typedef typename Container::reference	reference;
    typedef output_iterator_tag			iterator_category;
public:
    explicit				back_insert_iterator (Container& ctr) : _rctr (ctr) {}
    inline back_insert_iterator&	operator= (typename Container::const_reference v)
					    { _rctr.push_back (v); return *this; }
    inline back_insert_iterator&	operator* (void)  { return *this; }
    inline back_insert_iterator&	operator++ (void) { return *this; }
    inline back_insert_iterator		operator++ (int)  { return *this; }
protected:
    Container&		_rctr;
};

/// Returns the back_insert_iterator for \p ctr.
template <class Container>
inline back_insert_iterator<Container> back_inserter (Container& ctr)
    { return back_insert_iterator<Container> (ctr); }

//----------------------------------------------------------------------

/// \class front_insert_iterator uiterator.h ustl.h
/// \ingroup IteratorAdaptors
/// \brief Calls push_front on bound container for each assignment.
///
template <class Container>
class front_insert_iterator {
public:
    typedef typename Container::value_type	value_type;
    typedef typename Container::difference_type	difference_type;
    typedef typename Container::pointer		pointer;
    typedef typename Container::reference	reference;
    typedef output_iterator_tag			iterator_category;
public:
    explicit				front_insert_iterator (Container& ctr) : _rctr (ctr) {}
    inline front_insert_iterator&	operator= (typename Container::const_reference v)
					    { _rctr.push_front (v); return *this; }
    inline front_insert_iterator&	operator* (void)  { return *this; }
    inline front_insert_iterator&	operator++ (void) { return *this; }
    inline front_insert_iterator	operator++ (int)  { return *this; }
protected:
    Container&		_rctr;
};

/// Returns the front_insert_iterator for \p ctr.
template <class Container>
inline front_insert_iterator<Container> front_inserter (Container& ctr)
    { return front_insert_iterator<Container> (ctr); }

//----------------------------------------------------------------------

/// \class index_iterate uiterator.h ustl.h
/// \ingroup IteratorAdaptors
///
/// \brief Allows iteration through an index container.
///
/// Converts an iterator into a container of uoff_t indexes to an
/// iterator of iterators into another container.
///
template <typename RandomAccessIterator, typename IndexIterator>
class index_iterate {
public:
    typedef RandomAccessIterator	value_type;
    typedef ptrdiff_t			difference_type;
    typedef RandomAccessIterator*	pointer;
    typedef RandomAccessIterator	reference;
    typedef random_access_iterator_tag	iterator_category;
public:
				index_iterate (void) : _base(), _i() {}
				index_iterate (RandomAccessIterator ibase, IndexIterator iindex) : _base (ibase), _i (iindex) {}
    inline bool			operator== (const index_iterate& i) const { return _i == i._i; }
    inline bool			operator< (const index_iterate& i) const { return _i < i._i; }
    inline bool			operator== (const RandomAccessIterator& i) const { return _base == i; }
    inline bool			operator< (const RandomAccessIterator& i) const { return _base < i; }
    inline IndexIterator	base (void) const { return _i; }
    inline reference		operator* (void) const { return advance(_base, *_i); }
    inline pointer		operator-> (void) const { return &(operator*()); }
    inline index_iterate&	operator++ (void) { ++_i; return *this; }
    inline index_iterate&	operator-- (void) { --_i; return *this; }
    inline index_iterate	operator++ (int) { index_iterate prev (*this); ++_i; return prev; }
    inline index_iterate	operator-- (int) { index_iterate prev (*this); --_i; return prev; }
    inline index_iterate&	operator+= (size_t n) { _i += n; return *this; }
    inline index_iterate&	operator-= (size_t n) { _i -= n; return *this; }
    inline index_iterate	operator+ (size_t n) const { return index_iterate (_base, _i + n); }
    inline index_iterate	operator- (size_t n) const { return index_iterate (_base, _i - n); }
    inline reference		operator[] (uoff_t n) const { return *(*this + n); }
    inline difference_type	operator- (const index_iterate& i) const { return distance (_i, i._i); }
private:
    RandomAccessIterator	_base;
    IndexIterator		_i;
};

/// Returns an index_iterate for \p ibase over \p iindex.
template <typename RandomAccessIterator, typename IndexIterator>
inline index_iterate<RandomAccessIterator, IndexIterator> index_iterator (RandomAccessIterator ibase, IndexIterator iindex)
{
    return index_iterate<RandomAccessIterator, IndexIterator> (ibase, iindex);
}

/// Converts the indexes in \p xc to iterators in \p ic of base \p ibase.
template <typename IndexContainer, typename IteratorContainer>
inline void indexv_to_iteratorv (typename IteratorContainer::value_type ibase, const IndexContainer& xc, IteratorContainer& ic)
{
    ic.resize (xc.size());
    copy_n (index_iterator (ibase, xc.begin()), xc.size(), ic.begin());
}

//----------------------------------------------------------------------

/// Converts the given const_iterator into an iterator.
///
template <typename Container>
inline typename Container::iterator unconst (typename Container::const_iterator i, Container&)
    { return const_cast<typename Container::iterator>(i); }

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#define IBYI(Iter1, Iter2, Ctr1, Ctr2)	\
template <typename Container1, typename Container2>	\
inline typename Container2::Iter2 ibyi (typename Container1::Iter1 idx, Ctr1& ctr1, Ctr2& ctr2)	\
{						\
    assert (ctr1.size() == ctr2.size());	\
    return ctr2.begin() + (idx - ctr1.begin());	\
}

IBYI(const_iterator, const_iterator, const Container1, const Container2)
IBYI(iterator, iterator, Container1, Container2)
IBYI(const_iterator, iterator, const Container1, Container2)
IBYI(iterator, const_iterator, Container1, const Container2)

#else // DOXYGEN

#error "This declaration is for doxygen only; it is not compiled."

/// Converts a const_iterator in one container into a const_iterator in another container.
template <typename Container1, typename Container2>
inline typename Container2::iterator ibyi (typename Container1::iterator idx, Container1& ctr1, Container2& ctr2) {}

#endif // DOXYGEN

//----------------------------------------------------------------------

} // namespace ustl
