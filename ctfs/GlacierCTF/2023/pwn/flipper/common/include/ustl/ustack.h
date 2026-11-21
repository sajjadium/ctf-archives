// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once

namespace ustl {

/// \class stack ustack.h ustl.h
/// \ingroup Sequences
///
/// Stack adapter to uSTL containers.
///
template <typename T, typename Container = vector<T> >
class stack {
public:
    typedef T			value_type;
    typedef Container		container_type;
    typedef typename container_type::size_type size_type;
    typedef typename container_type::difference_type difference_type;
    typedef value_type&		reference;
    typedef const value_type&	const_reference;
public:
    inline			stack (void)			: _storage () { }
    explicit inline		stack (const container_type& s)	: _storage (s) { }
    explicit inline		stack (const stack& s)		: _storage (s._storage) { }
    inline bool			empty (void) const		{ return _storage.empty(); }
    inline size_type		size (void) const		{ return _storage.size(); }
    inline reference		top (void)			{ return _storage.back(); }
    inline const_reference	top (void) const		{ return _storage.back(); }
    inline void			push (const_reference v)	{ _storage.push_back (v); }
    inline void			pop (void)			{ _storage.pop_back(); }
    inline void			swap (stack& v)			{ _storage.swap (v); }
    inline bool			operator== (const stack& s) const	{ return _storage == s._storage; }
    inline bool			operator< (const stack& s) const	{ return _storage.size() < s._storage.size(); }
#if HAVE_CPP11
    inline			stack (stack&& v)		: _storage(move(v._storage)) {}
    inline			stack (container_type&& s)	: _storage(move(s)) {}
    inline stack&		operator= (stack&& v)		{ swap (v); return *this; }
    template <typename... Args>
    inline void			emplace (Args&&... args)	{ _storage.emplace_back (forward<Args>(args)...); }
#endif
private:
    container_type		_storage;	///< Where the data actually is.
};

} // namespace ustl
