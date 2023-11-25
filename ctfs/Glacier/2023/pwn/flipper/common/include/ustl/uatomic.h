// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2016 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "utypes.h"
#if HAVE_CPP11

//{{{ memory_order -----------------------------------------------------

namespace ustl {

enum memory_order {
    memory_order_relaxed = __ATOMIC_RELAXED,
    memory_order_consume = __ATOMIC_CONSUME,
    memory_order_acquire = __ATOMIC_ACQUIRE,
    memory_order_release = __ATOMIC_RELEASE,
    memory_order_acq_rel = __ATOMIC_ACQ_REL,
    memory_order_seq_cst = __ATOMIC_SEQ_CST
};

//}}}-------------------------------------------------------------------
//{{{ atomic

template <typename T>
class atomic {
    T			_v;
public:
			atomic (void) = default;
    inline constexpr	atomic (T v) : _v(v) {}
			atomic (const atomic&) = delete;
    atomic&		operator= (const atomic&) = delete;
    inline bool		is_lock_free (void) const
			    { return __atomic_is_lock_free (sizeof(T), &_v); }
    inline void		store (T v, memory_order order = memory_order_seq_cst)
			    { __atomic_store_n (&_v, v, order); }
    inline T		load (memory_order order = memory_order_seq_cst) const
			    { return __atomic_load_n (&_v, order); }
    inline T		exchange (T v, memory_order order = memory_order_seq_cst)
			    { return __atomic_exchange_n (&_v, v, order); }
    inline bool		compare_exchange_weak (T& expected, T desired, memory_order order = memory_order_seq_cst)
			    { return __atomic_compare_exchange_n (&_v, &expected, desired, true, order, order); }
    inline bool		compare_exchange_weak (T& expected, T desired, memory_order success, memory_order failure)
			    { return __atomic_compare_exchange_n (&_v, &expected, desired, true, success, failure); }
    inline bool		compare_exchange_strong (T& expected, T desired, memory_order success, memory_order failure)
			    { return __atomic_compare_exchange_n (&_v, &expected, desired, false, success, failure); }
    inline T		fetch_add (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_fetch_add (&_v, v, order); }
    inline T		fetch_sub (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_fetch_sub (&_v, v, order); }
    inline T		fetch_and (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_fetch_and (&_v, v, order); }
    inline T		fetch_or (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_fetch_or (&_v, v, order); }
    inline T		fetch_xor (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_fetch_xor (&_v, v, order); }
    inline T		add_fetch (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_add_fetch (&_v, v, order); }
    inline T		sub_fetch (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_sub_fetch (&_v, v, order); }
    inline T		and_fetch (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_and_fetch (&_v, v, order); }
    inline T		or_fetch (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_or_fetch (&_v, v, order); }
    inline T		xor_fetch (T v, memory_order order = memory_order_seq_cst )
			    { return __atomic_xor_fetch (&_v, v, order); }
    inline		operator T (void) const	{ return load(); }
    inline T		operator= (T v)		{ store(v); return v; }
    inline T		operator++ (int)	{ return fetch_add (1); }
    inline T		operator-- (int)	{ return fetch_sub (1); }
    inline T		operator++ (void)	{ return add_fetch (1); }
    inline T		operator-- (void)	{ return sub_fetch (1); }
    inline T		operator+= (T v)	{ return add_fetch (v); }
    inline T		operator-= (T v)	{ return sub_fetch (v); }
    inline T		operator&= (T v)	{ return and_fetch (v); }
    inline T		operator|= (T v)	{ return  or_fetch (v); }
    inline T		operator^= (T v)	{ return xor_fetch (v); }
};
#define ATOMIC_VAR_INIT	{0}

//}}}-------------------------------------------------------------------
//{{{ atomic_flag

class atomic_flag {
    bool		_v;
public:
			atomic_flag (void) = default;
    inline constexpr	atomic_flag (bool v)	: _v(v) {}
			atomic_flag (const atomic_flag&) = delete;
    atomic_flag&	operator= (const atomic_flag&) = delete;
    void		clear (memory_order order = memory_order_seq_cst)
			    { __atomic_clear (&_v, order); }
    bool		test_and_set (memory_order order = memory_order_seq_cst)
			    { return __atomic_test_and_set (&_v, order); }
};
#define ATOMIC_FLAG_INIT	{false}

//}}}-------------------------------------------------------------------
//{{{ fence functions

namespace {

template <typename T>
static inline T kill_dependency (T v) noexcept
    { T r (v); return r; }
static inline void atomic_thread_fence (memory_order order) noexcept
    { __atomic_thread_fence (order); }
static inline void atomic_signal_fence (memory_order order) noexcept
    { __atomic_signal_fence (order); }

} // namespace
} // namespace ustl
#endif // HAVE_CPP11
//}}}-------------------------------------------------------------------
