// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "uvector.h"
#include "ualgo.h"

namespace ustl {

/// \class multiset umultiset.h ustl.h
/// \ingroup AssociativeContainers
///
/// \brief Multiple sorted container.
/// Unlike set, it may contain multiple copies of each element.
///
template <typename T, typename Comp = less<T> >
class multiset : public vector<T> {
public:
    typedef const multiset<T,Comp>&			rcself_t;
    typedef vector<T>					base_class;
    typedef typename base_class::value_type		value_type;
    typedef typename base_class::size_type		size_type;
    typedef typename base_class::pointer		pointer;
    typedef typename base_class::const_pointer		const_pointer;
    typedef typename base_class::reference		reference;
    typedef typename base_class::const_reference	const_reference;
    typedef typename base_class::const_iterator		const_iterator;
    typedef typename base_class::iterator		iterator;
    typedef typename base_class::reverse_iterator	reverse_iterator;
    typedef typename base_class::const_reverse_iterator	const_reverse_iterator;
    typedef pair<iterator,iterator>			range_t;
    typedef pair<const_iterator,const_iterator>		const_range_t;
public:
    inline			multiset (void)				: base_class() {}
    inline explicit		multiset (size_type n)			: base_class (n) {}
    inline explicit		multiset (rcself_t v)			: base_class (v) {}
    inline			multiset (const_iterator i1, const_iterator i2) : base_class() { insert (i1, i2); }
    inline rcself_t		operator= (rcself_t v)			{ base_class::operator= (v); return *this; }
    inline size_type		size (void) const			{ return base_class::size(); }
    inline iterator		begin (void)				{ return base_class::begin(); }
    inline const_iterator	begin (void) const			{ return base_class::begin(); }
    inline const_iterator	cbegin (void) const			{ return base_class::cbegin(); }
    inline iterator		end (void)				{ return base_class::end(); }
    inline const_iterator	end (void) const			{ return base_class::end(); }
    inline const_iterator	cend (void) const			{ return base_class::cend(); }
    inline Comp			value_comp (void) const			{ return Comp(); }
    inline Comp			key_comp (void) const			{ return value_comp(); }
    inline void			assign (const_iterator i1, const_iterator i2)	{ clear(); insert (i1, i2); }
    inline const_iterator	find (const_reference v) const		{ const_iterator i = ::ustl::lower_bound (begin(), end(), v, Comp()); return (i != end() && *i == v) ? i : end(); }
    inline iterator		find (const_reference v)		{ return const_cast<iterator>(const_cast<rcself_t>(*this).find (v)); }
    inline const_iterator	lower_bound (const_reference v) const	{ return ::ustl::lower_bound (begin(), end(), v, Comp()); }
    inline iterator		lower_bound (const_reference v)		{ return const_cast<iterator>(const_cast<rcself_t>(*this).lower_bound (v)); }
    inline const_iterator	upper_bound (const_reference v) const	{ return ::ustl::upper_bound (begin(), end(), v, Comp()); }
    inline iterator		upper_bound (const_reference v)		{ return const_cast<iterator>(const_cast<rcself_t>(*this).upper_bound (v)); }
    inline const_range_t	equal_range (const_reference v) const	{ return ::ustl::equal_range (begin(), end(), v, Comp()); }
    inline range_t		equal_range (const_reference v)		{ return ::ustl::equal_range (begin(), end(), v, Comp()); }
    inline size_type		count (const_reference v) const		{ const_range_t r = equal_range(v); return distance(r.first,r.second); }
    inline void			push_back (const_reference v)		{ insert (v); }
    inline iterator		insert (const_reference v)		{ return base_class::insert (upper_bound(v), v); }
    inline iterator		insert (const_iterator, const_reference v)	{ return insert(v); }
    void			insert (const_iterator i1, const_iterator i2)	{ for (; i1 < i2; ++i1) insert (*i1); }
    inline iterator		erase (const_iterator ep)			{ return base_class::erase (ep); }
    inline iterator		erase (const_iterator ep1, const_iterator ep2)	{ return base_class::erase (ep1, ep2); }
    inline size_type		erase (const_reference v)		{ range_t epr = equal_range (v); erase (epr.first, epr.second); return distance(epr.first, epr.second); }
    inline void			clear (void)				{ base_class::clear(); }
    inline void			swap (multiset& v)			{ base_class::swap (v); }
#if HAVE_CPP11
    using initlist_t = std::initializer_list<value_type>;
    inline explicit		multiset (multiset&& v)			: base_class (move(v)) {}
    inline			multiset (initlist_t v)			: base_class() { insert (v.begin(), v.end()); }
    inline multiset&		operator= (multiset&& v)		{ base_class::operator= (move(v)); return *this; }
    inline iterator		insert (T&& v)				{ return base_class::insert (upper_bound(v), move(v)); }
    inline iterator		insert (const_iterator, T&& v)		{ return insert (move(v)); }
    inline void			insert (initlist_t v)			{ insert (v.begin(), v.end()); }
    template <typename... Args>
    inline iterator		emplace (Args&&... args)		{ return insert (T(forward<Args>(args)...)); }
    template <typename... Args>
    inline iterator		emplace_hint (const_iterator h, Args&&... args)	{ return insert (h, T(forward<Args>(args)...)); }
    template <typename... Args>
    inline iterator		emplace_back (Args&&... args)		{ return insert (T(forward<Args>(args)...)); }
#endif
};

} // namespace ustl
