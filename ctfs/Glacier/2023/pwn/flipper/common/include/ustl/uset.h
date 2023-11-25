// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "uvector.h"

namespace ustl {

/// \class set uset.h ustl.h
/// \ingroup Sequences
///
/// \brief Unique sorted container. Sorted vector with all values unique.
///
template <typename T, typename Comp = less<T> >
class set : public vector<T> {
public:
    typedef const set<T,Comp>&				rcself_t;
    typedef vector<T>					base_class;
    typedef typename base_class::value_type		key_type;
    typedef typename base_class::value_type		data_type;
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
    typedef pair<iterator,bool>				insertrv_t;
    typedef pair<iterator,iterator>			range_t;
    typedef pair<const_iterator,const_iterator>		const_range_t;
public:
    inline			set (void)		: base_class() { }
    explicit inline		set (size_type n)	: base_class (n) { }
    inline			set (rcself_t v)	: base_class (v) { }
    inline			set (const_iterator i1, const_iterator i2) : base_class() { insert (i1, i2); }
    inline rcself_t		operator= (rcself_t v)	{ base_class::operator= (v); return *this; }
    inline size_type		size (void) const	{ return base_class::size(); }
    inline iterator		begin (void)		{ return base_class::begin(); }
    inline const_iterator	begin (void) const	{ return base_class::begin(); }
    inline const_iterator	cbegin (void) const	{ return base_class::cbegin(); }
    inline iterator		end (void)		{ return base_class::end(); }
    inline const_iterator	end (void) const	{ return base_class::end(); }
    inline const_iterator	cend (void) const	{ return base_class::cend(); }
    inline const_iterator	find (const_reference v) const	{ const_iterator i = ::ustl::lower_bound (begin(), end(), v, Comp()); return (i != end() && *i == v) ? i : end(); }
    inline iterator		find (const_reference v)	{ return const_cast<iterator>(const_cast<rcself_t>(*this).find (v)); }
    inline const_iterator	lower_bound (const_reference v) const	{ return ::ustl::lower_bound (begin(), end(), v, Comp()); }
    inline iterator		lower_bound (const_reference v)		{ return const_cast<iterator>(const_cast<rcself_t>(*this).lower_bound (v)); }
    inline const_iterator	upper_bound (const_reference v) const	{ return ::ustl::upper_bound (begin(), end(), v, Comp()); }
    inline iterator		upper_bound (const_reference v)		{ return const_cast<iterator>(const_cast<rcself_t>(*this).upper_bound (v)); }
    inline const_range_t	equal_range (const_reference v) const	{ return ::ustl::equal_range (begin(), end(), v, Comp()); }
    inline range_t		equal_range (const_reference v)		{ return ::ustl::equal_range (begin(), end(), v, Comp()); }
    inline size_type		count (const_reference v) const		{ const_range_t r = equal_range(v); return distance(r.first,r.second); }
    inline Comp			value_comp (void) const			{ return Comp(); }
    inline Comp			key_comp (void) const			{ return value_comp(); }
    inline void			assign (const_iterator i1, const_iterator i2)	{ clear(); insert (i1, i2); }
    inline void			push_back (const_reference v)		{ insert (v); }
    insertrv_t			insert (const_reference v);
    inline iterator		insert (const_iterator, const_reference v)	{ return insert(v).first; }
    inline void			insert (const_iterator i1, const_iterator i2)	{ for (; i1 < i2; ++i1) insert (*i1); }
    inline void			erase (const_reference v)		{ iterator ip = find (v); if (ip != end()) erase (ip); }
    inline iterator		erase (iterator ep)			{ return base_class::erase (ep); }
    inline iterator		erase (iterator ep1, iterator ep2)	{ return base_class::erase (ep1, ep2); }
    inline void			clear (void)				{ base_class::clear(); }
    inline void			swap (set& v)				{ base_class::swap (v); }
#if HAVE_CPP11
    using initlist_t = std::initializer_list<value_type>;
    inline			set (set&& v)				: base_class (move(v)) {}
    inline			set (initlist_t v)			: base_class() { insert (v.begin(), v.end()); }
    inline set&			operator= (set&& v)			{ base_class::operator= (move(v)); return *this; }
    insertrv_t			insert (T&& v);
    inline iterator		insert (const_iterator, T&& v)		{ return insert (move(v)); }
    inline void			insert (initlist_t v)			{ insert (v.begin(), v.end()); }
    template <typename... Args>
    inline insertrv_t		emplace (Args&&... args)		{ return insert (T(forward<Args>(args)...)); }
    template <typename... Args>
    inline iterator		emplace_hint (const_iterator h, Args&&... args)	{ return insert (h, T(forward<Args>(args)...)); }
    template <typename... Args>
    inline insertrv_t		emplace_back (Args&&... args)		{ return insert (T(forward<Args>(args)...)); }
#endif
};

#if HAVE_CPP11

template <typename T, typename Comp>
typename set<T,Comp>::insertrv_t set<T,Comp>::insert (T&& v)
{
    iterator ip = lower_bound (v);
    bool bInserted = (ip == end() || Comp()(v,*ip));
    if (bInserted)
	ip = base_class::insert (ip, move(v));
    return make_pair (ip, bInserted);
}

#endif

/// Inserts \p v into the container, maintaining the sort order.
template <typename T, typename Comp>
typename set<T,Comp>::insertrv_t set<T,Comp>::insert (const_reference v)
{
    iterator ip = lower_bound (v);
    bool bInserted = (ip == end() || Comp()(v,*ip));
    if (bInserted)
	ip = base_class::insert (ip, v);
    return make_pair (ip, bInserted);
}

} // namespace ustl
