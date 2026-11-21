// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "unew.h"
#include "uatomic.h"
#include "uiterator.h"
#include "ulimits.h"
#include "upair.h"

namespace ustl {

//{{{ auto_ptr -------------------------------------------------------

/// \class auto_ptr umemory.h ustl.h
/// \ingroup MemoryManagement
///
/// \brief A smart pointer.
///
/// Calls delete in the destructor; assignment transfers ownership.
/// This class does not work with void pointers due to the absence
/// of the required dereference operator. auto_ptr is deprecated in
/// c++11; use unique_ptr instead.
///
template <typename T>
class auto_ptr {
public:
    typedef T		value_type;
    typedef T*		pointer;
    typedef T&		reference;
public:
    /// Takes ownership of \p p.
    inline explicit	auto_ptr (pointer p = nullptr)	: _p (p) {}
    /// Takes ownership of pointer in \p p. \p p relinquishes ownership.
    inline		auto_ptr (auto_ptr<T>& p)	: _p (p.release()) {}
    /// Deletes the owned pointer.
    inline		~auto_ptr (void)		{ delete _p; }
    /// Returns the pointer without relinquishing ownership.
    inline pointer	get (void) const		{ return _p; }
    /// Returns the pointer and gives up ownership.
    inline pointer	release (void)			{ pointer rv (_p); _p = nullptr; return rv; }
    /// Deletes the pointer and sets it equal to \p p.
    inline void		reset (pointer p)		{ if (p != _p) { delete _p; _p = p; } }
    /// Takes ownership of \p p.
    inline auto_ptr<T>&	operator= (pointer p)		{ reset (p); return *this; }
    /// Takes ownership of pointer in \p p. \p p relinquishes ownership.
    inline auto_ptr<T>&	operator= (auto_ptr<T>& p)	{ reset (p.release()); return *this; }
    inline reference	operator* (void) const		{ return *_p; }
    inline pointer	operator-> (void) const		{ return _p; }
    inline bool		operator== (const pointer p) const	{ return _p == p; }
    inline bool		operator== (const auto_ptr<T>& p) const	{ return _p == p._p; }
    inline bool		operator< (const auto_ptr<T>& p) const	{ return p._p < _p; }
private:
    pointer		_p;
};

//}}}-------------------------------------------------------------------
//{{{ unique_ptr
#if HAVE_CPP11

/// \class unique_ptr memory.h stl.h
/// \ingroup MemoryManagement
/// \brief A smart pointer.
/// Calls delete in the destructor; assignment transfers ownership.
/// This class does not work with void pointers due to the absence
/// of the required dereference operator.
template <typename T>
class unique_ptr {
public:
    using element_type		= T;
    using pointer		= element_type*;
    using reference		= element_type&;
public:
    inline constexpr		unique_ptr (void)		: _p (nullptr) {}
    inline constexpr explicit	unique_ptr (pointer p)		: _p (p) {}
    inline			unique_ptr (unique_ptr&& p)	: _p (p.release()) {}
				unique_ptr (const unique_ptr&) = delete;
    inline			~unique_ptr (void)		{ delete _p; }
    inline constexpr pointer	get (void) const		{ return _p; }
    inline pointer		release (void)			{ auto rv (_p); _p = nullptr; return rv; }
    inline void			reset (pointer p = nullptr)	{ assert (p != _p || !p); auto ov (_p); _p = p; delete ov; }
    inline void			swap (unique_ptr& v)		{ ::ustl::swap (_p, v._p); }
    inline constexpr explicit	operator bool (void) const	{ return _p != nullptr; }
    inline unique_ptr&		operator= (pointer p)		{ reset (p); return *this; }
    inline unique_ptr&		operator= (unique_ptr&& p)	{ reset (p.release()); return *this; }
    unique_ptr&			operator=(const unique_ptr&) = delete;
    inline constexpr reference	operator* (void) const		{ return *get(); }
    inline constexpr pointer	operator-> (void) const		{ return get(); }
    inline constexpr reference	operator[] (size_t i) const	{ return get()[i]; }
    inline constexpr bool	operator== (const pointer p) const	{ return _p == p; }
    inline constexpr bool	operator== (const unique_ptr& p) const	{ return _p == p._p; }
    inline constexpr bool	operator< (const unique_ptr& p) const	{ return _p < p._p; }
private:
    pointer			_p;
};

// array version
template<typename T>
class unique_ptr<T[]> {
public:
    using element_type		= T;
    using pointer		= element_type*;
    using reference		= element_type&;
public:
    inline constexpr		unique_ptr (void)		: _p (nullptr) {}
    inline constexpr explicit	unique_ptr (pointer p)		: _p (p) {}
    inline			unique_ptr (unique_ptr&& p)	: _p (p.release()) {}
				unique_ptr(const unique_ptr&) = delete;
    inline			~unique_ptr (void)		{ delete [] _p; }
    inline constexpr pointer	get (void) const		{ return _p; }
    inline pointer			release (void)			{ auto rv (_p); _p = nullptr; return rv; }
    inline void			reset (pointer p)		{ assert (p != _p); auto ov (_p); _p = p; delete [] ov; }
    inline void			swap (unique_ptr& v)		{ ::ustl::swap (_p, v._p); }
    inline constexpr explicit	operator bool (void) const	{ return _p != nullptr; }
    inline unique_ptr&		operator= (pointer p)		{ reset (p); return *this; }
    inline unique_ptr&		operator= (unique_ptr&& p)	{ reset (p.release()); return *this; }
    unique_ptr&			operator=(const unique_ptr&) = delete;
    inline constexpr reference	operator* (void) const		{ return *_p; }
    inline constexpr pointer	operator-> (void) const		{ return _p; }
    inline constexpr reference	operator[] (size_t i) const	{ return _p[i]; }
    inline constexpr bool	operator== (const pointer p) const	{ return _p == p; }
    inline constexpr bool	operator== (const unique_ptr& p) const	{ return _p == p._p; }
    inline constexpr bool	operator< (const unique_ptr& p) const	{ return _p < p._p; }
private:
    pointer			_p;
};

#if HAVE_CPP14

template <typename T> struct __make_unique { using __single_object = unique_ptr<T>; };
template <typename T> struct __make_unique<T[]> { using __array = unique_ptr<T[]>; };
template <typename T, size_t N> struct __make_unique<T[N]> { struct __invalid_type {}; };

template <typename T, typename... Args>
inline typename __make_unique<T>::__single_object
    make_unique (Args&&... args) { return unique_ptr<T> (new T (forward<Args>(args)...)); }

template <typename T>
inline typename __make_unique<T>::__array
    make_unique (size_t n) { return unique_ptr<T> (new remove_extent_t<T>[n]()); }

template <typename T, typename... Args>
inline typename __make_unique<T>::__invalid_type
    make_unique (Args&&...) = delete;

#endif // HAVE_CPP14
#endif // HAVE_CPP11

//}}}-------------------------------------------------------------------
//{{{ shared_ptr

#if HAVE_CPP11

/// \class shared_ptr memory.h stl.h
/// \ingroup MemoryManagement
/// \brief A smart pointer.
/// Calls delete in the destructor; assignment shares ownership.
template <typename T>
class shared_ptr {
public:
    using element_type		= T;
    using pointer		= element_type*;
    using reference		= element_type&;
private:
    struct container {
	pointer		p;
	atomic<size_t>	refs;
	inline constexpr explicit container (pointer np) : p(np),refs(1) {}
	inline	~container (void) noexcept { assert (!refs); delete p; }
    };
public:
    inline constexpr		shared_ptr (void)		: _p (nullptr) {}
    inline explicit		shared_ptr (pointer p)		: _p (new container (p)) {}
    inline			shared_ptr (shared_ptr&& p)	: _p (p._p) { p._p = nullptr; }
    inline			shared_ptr (const shared_ptr& p): _p (p._p) { if (_p) ++_p->refs; }
    inline			~shared_ptr (void)		{ reset(); }
    inline constexpr size_t	use_count (void) const		{ return _p ? _p->refs.load() : 0; }
    inline constexpr bool	unique (void) const		{ return use_count() == 1; }
    inline constexpr pointer	get (void) const		{ return _p ? _p->p : nullptr; }
    void			reset (pointer p = nullptr) {
				    assert (p != get() || !p);
				    auto ov = _p;
				    _p = p ? new container(p) : nullptr;
				    if (ov && !--ov->refs)
					delete ov;
				}
    inline void			swap (shared_ptr& v)		{ ::ustl::swap (_p, v._p); }
    inline constexpr explicit	operator bool (void) const	{ return get(); }
    inline shared_ptr&		operator= (pointer p)		{ reset (p); return *this; }
    inline shared_ptr&		operator= (shared_ptr&& p)	{ swap (p); return *this; }
    inline shared_ptr&		operator= (const shared_ptr& p)	{ reset(); _p = p._p; if (_p) ++_p->refs; return *this; }
    inline constexpr reference	operator* (void) const		{ return *get(); }
    inline constexpr pointer	operator-> (void) const		{ return get(); }
    inline constexpr reference	operator[] (size_t i) const	{ return get()[i]; }
    inline constexpr bool	operator== (const pointer p) const	{ return get() == p; }
    inline constexpr bool	operator== (const shared_ptr& p) const	{ return get() == p.get(); }
    inline constexpr bool	operator< (const shared_ptr& p) const	{ return get() < p.get(); }
private:
    container*			_p;
};

#if HAVE_CPP14

template <typename T, typename... Args>
inline auto make_shared (Args&&... args)
    { return shared_ptr<T> (new T (forward<Args>(args)...)); }

#endif // HAVE_CPP14

//}}}-------------------------------------------------------------------
//{{{ scope_exit

template <typename F>
class scope_exit {
public:
    inline explicit	scope_exit (F&& f) noexcept		: _f(move(f)),_enabled(true) {}
    inline		scope_exit (scope_exit&& f) noexcept	: _f(move(f._f)),_enabled(f._enabled) { f.release(); }
    inline void		release (void) noexcept			{ _enabled = false; }
    inline		~scope_exit (void) noexcept (noexcept (declval<F>()))	{ if (_enabled) _f(); }
			scope_exit (const scope_exit&) = delete;
    scope_exit&		operator= (const scope_exit&) = delete;
    scope_exit&		operator= (scope_exit&&) = delete;
private:
    F		_f;
    bool	_enabled;
};

#if HAVE_CPP14
template <typename F>
auto make_scope_exit (F&& f) noexcept
    { return scope_exit<remove_reference_t<F>>(forward<F>(f)); }
#endif // HAVE_CPP14

//}}}-------------------------------------------------------------------
//{{{ unique_resource

template <typename R, typename D>
class unique_resource {
public:
    inline explicit	unique_resource (R&& resource, D&& deleter, bool enabled = true) noexcept
			    : _resource(move(resource)), _deleter(move(deleter)),_enabled(enabled) {}
    inline		unique_resource (unique_resource&& r) noexcept
			    : _resource(move(r._resource)),_deleter(move(r._deleter)),_enabled(r._enabled) { r.release(); }
			unique_resource (const unique_resource&) = delete;
    inline		~unique_resource() noexcept(noexcept(declval<unique_resource<R,D>>().reset()))
			    { reset(); }
    inline const D&	get_deleter (void) const noexcept	{ return _deleter; }
    inline R const&	get (void) const noexcept		{ return _resource; }
    inline R const&	release (void) noexcept			{ _enabled = false; return get(); }
    inline void		reset (void) noexcept (noexcept(declval<D>())) {
			    if (_enabled) {
				_enabled = false;
				get_deleter()(_resource);
			    }
			}
    inline void		reset (R&& r) noexcept (noexcept(reset())) {
			    reset();
			    _resource = move(r);
			    _enabled = true;
			}
    unique_resource&	operator= (const unique_resource&) = delete;
    unique_resource&	operator= (unique_resource &&r) noexcept(noexcept(reset())) {
			    reset();
			    _deleter = move(r._deleter);
			    _resource = move(r._resource);
			    _enabled = r._enabled;
			    r.release();
			    return *this;
			}
    inline		operator R const& (void) const noexcept	{ return get(); }
    inline R		operator-> (void) const noexcept	{ return _resource; }
    inline add_lvalue_reference_t<remove_pointer_t<R>>
			operator* (void) const	{ return *_resource; }
private:
    R			_resource;
    D			_deleter;
    bool		_enabled;
};

#if HAVE_CPP14

template <typename R,typename D>
auto make_unique_resource (R&& r, D&& d) noexcept
    { return unique_resource<R,remove_reference_t<D>>(move(r), forward<remove_reference_t<D>>(d), true); }

template <typename R,typename D>
auto make_unique_resource_checked (R r, R invalid, D d) noexcept
{
    bool shouldrun = !(r == invalid);
    return unique_resource<R,D>(move(r), move(d), shouldrun);
}

#endif // HAVE_CPP14
#endif // HAVE_CPP11

//}}}-------------------------------------------------------------------
//{{{ construct and destroy

/// Calls the placement new on \p p.
/// \ingroup RawStorageAlgorithms
///
template <typename T>
inline void construct_at (T* p)
    { new (p) T; }

/// Calls the placement new on \p p.
/// \ingroup RawStorageAlgorithms
///
template <typename T>
inline void construct_at (T* p, const T& value)
    { new (p) T (value); }

#if HAVE_CPP11
/// Calls the move placement new on \p p.
/// \ingroup RawStorageAlgorithms
///
template <typename T>
inline void construct_at (T* p, T&& value)
    { new (p) T (move<T>(value)); }
#endif

template <typename T>
inline void construct (T* p)
    { construct_at(p); }

/// Calls the placement new on \p p.
/// \ingroup RawStorageAlgorithms
///
template <typename ForwardIterator>
inline void uninitialized_default_construct (ForwardIterator first, ForwardIterator last)
{
    typedef typename iterator_traits<ForwardIterator>::value_type value_type;
#if HAVE_CPP11
    if (is_pod<value_type>::value)
#else
    if (numeric_limits<value_type>::is_integral)
#endif
	memset (reinterpret_cast<void*>(first), 0, max(distance(first,last),0)*sizeof(value_type));
    else
	for (--last; intptr_t(first) <= intptr_t(last); ++first)
	    construct_at (&*first);
}
template <typename ForwardIterator>
inline void uninitialized_default_construct_n (ForwardIterator first, size_t n)
    { uninitialized_default_construct (first, first+n); }
template <typename ForwardIterator>
inline void construct (ForwardIterator first, ForwardIterator last)
    { uninitialized_default_construct (first, last); }

/// Calls the placement new on \p [first,last) with iterator_traits::value_type()
template <typename ForwardIterator>
inline void uninitialized_value_construct (ForwardIterator first, ForwardIterator last)
{
    typedef typename iterator_traits<ForwardIterator>::value_type value_type;
    for (--last; intptr_t(first) <= intptr_t(last); ++first)
	construct_at (&*first, value_type());
}
template <typename ForwardIterator>
inline void uninitialized_value_construct_n (ForwardIterator first, size_t n)
    { uninitialized_value_construct (first, first+n); }

/// Calls the destructor of \p p without calling delete.
/// \ingroup RawStorageAlgorithms
///
template <typename T>
inline void destroy_at (T* p) noexcept
    { p->~T(); }

template <typename T>
inline void destroy (T* p) noexcept
    { destroy_at(p); }

// Helper templates to not instantiate anything for integral types.
namespace {

template <typename T>
void dtors (T first, T last) noexcept
    { for (--last; intptr_t(first) <= intptr_t(last); ++first) destroy_at (&*first); }
template <typename T, bool bIntegral>
struct Sdtorsr {
    inline void operator()(T first, T last) noexcept { dtors (first, last); }
};
template <typename T>
struct Sdtorsr<T,true> {
    inline void operator()(T, T) noexcept {}
};
} // namespace

/// Calls the destructor on elements in range [first, last) without calling delete.
/// \ingroup RawStorageAlgorithms
///
template <typename ForwardIterator>
inline void destroy (ForwardIterator first, ForwardIterator last) noexcept
{
    typedef typename iterator_traits<ForwardIterator>::value_type value_type;
#if HAVE_CPP11
    Sdtorsr<ForwardIterator,is_pod<value_type>::value>()(first, last);
#else
    Sdtorsr<ForwardIterator,numeric_limits<value_type>::is_integral>()(first, last);
#endif
}
template <typename ForwardIterator>
inline void destroy_n (ForwardIterator first, size_t n) noexcept
    { destroy (first, first+n); }

//}}}-------------------------------------------------------------------
//{{{ Raw storage algorithms

//}}}-------------------------------------------------------------------
//{{{ Raw storage algorithms

template <typename T> inline T* cast_to_type (void* p, const T*) { return reinterpret_cast<T*>(p); }

/// \brief Creates a temporary buffer pair from \p p and \p n
/// This is intended to be used with alloca to create temporary buffers.
/// The size in the returned pair is set to 0 if the allocation is unsuccessful.
/// \ingroup RawStorageAlgorithms
///
template <typename T>
inline pair<T*, ptrdiff_t> make_temporary_buffer (void* p, size_t n, const T* ptype)
{
    return make_pair (cast_to_type(p,ptype), ptrdiff_t(p ? n : 0));
}

#if HAVE_ALLOCA_H
    /// \brief Allocates a temporary buffer, if possible.
    /// \ingroup RawStorageAlgorithms
    #define get_temporary_buffer(size, ptype)	make_temporary_buffer (alloca(size_of_elements(size, ptype)), size, ptype)
    #define return_temporary_buffer(p)
#else
    #define get_temporary_buffer(size, ptype)	make_temporary_buffer (malloc(size_of_elements(size, ptype)), size, ptype)
    #define return_temporary_buffer(p)		if (p) free (p), p = nullptr
#endif

/// Copies [first, last) into result by calling copy constructors in result.
/// \ingroup RawStorageAlgorithms
///
template <typename InputIterator, typename ForwardIterator>
ForwardIterator uninitialized_copy (InputIterator first, InputIterator last, ForwardIterator result)
{
    for (; first < last; ++result, ++first)
	construct_at (&*result, *first);
    return result;
}

/// Copies [first, first + n) into result by calling copy constructors in result.
/// \ingroup RawStorageAlgorithms
///
template <typename InputIterator, typename ForwardIterator>
ForwardIterator uninitialized_copy_n (InputIterator first, size_t n, ForwardIterator result)
{
    for (++n; --n; ++result, ++first)
	construct_at (&*result, *first);
    return result;
}

/// Calls construct on all elements in [first, last) with value \p v.
/// \ingroup RawStorageAlgorithms
///
template <typename ForwardIterator, typename T>
void uninitialized_fill (ForwardIterator first, ForwardIterator last, const T& v)
{
    for (; first < last; ++first)
	construct_at (&*first, v);
}

/// Calls construct on all elements in [first, first + n) with value \p v.
/// \ingroup RawStorageAlgorithms
///
template <typename ForwardIterator, typename T>
ForwardIterator uninitialized_fill_n (ForwardIterator first, size_t n, const T& v)
{
    for (++n; --n; ++first)
	construct_at (&*first, v);
    return first;
}

#if HAVE_CPP11

/// Moves [first, last) into result by calling move constructors in result.
/// \ingroup RawStorageAlgorithms
///
template <typename InputIterator, typename ForwardIterator>
ForwardIterator uninitialized_move (InputIterator first, InputIterator last, ForwardIterator result)
{
    for (; first < last; ++result, ++first)
	construct_at (&*result, move(*first));
    return result;
}

/// Moves [first, first + n) into result by calling move constructors in result.
/// \ingroup RawStorageAlgorithms
///
template <typename InputIterator, typename ForwardIterator>
ForwardIterator uninitialized_move_n (InputIterator first, size_t n, ForwardIterator result)
{
    for (++n; --n; ++result, ++first)
	construct_at (&*result, move(*first));
    return result;
}

#endif // HAVE_CPP11

} // namespace ustl

//}}}-------------------------------------------------------------------
//{{{ initializer_list
#if HAVE_CPP11 && WITHOUT_LIBSTDCPP

namespace std {	// Internal stuff must be in std::

/// Internal class for compiler support of C++11 initializer lists
template <typename T>
class initializer_list {
public:
    typedef T 			value_type;
    typedef size_t 		size_type;
    typedef const T& 		const_reference;
    typedef const_reference	reference;
    typedef const T* 		const_iterator;
    typedef const_iterator	iterator;
private:
    /// This object is only constructed by the compiler when the {1,2,3}
    /// syntax is used, so the constructor must be private
    inline constexpr		initializer_list (const_iterator p, size_type sz) noexcept : _data(p), _size(sz) {}
public:
    inline constexpr		initializer_list (void)noexcept	: _data(nullptr), _size(0) {}
    inline constexpr size_type	size (void) const noexcept	{ return _size; }
    inline constexpr const_iterator begin() const noexcept	{ return _data; }
    inline constexpr const_iterator end() const noexcept	{ return begin()+size(); }
private:
    iterator			_data;
    size_type			_size;
};

template <typename T>
inline constexpr const T* begin (initializer_list<T> il) noexcept { return il.begin(); }
template <typename T>
inline constexpr const T* end (initializer_list<T> il) noexcept { return il.end(); }

} // namespace std

#endif	// HAVE_CPP11
//}}}-------------------------------------------------------------------
