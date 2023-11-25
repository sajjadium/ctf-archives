// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.
//
/// \file uutility.h
/// \brief Utility templates.

#pragma once
#include "utypes.h"
#include "ulimits.h"
#include "assert.h"

namespace ustl {

#if HAVE_CPP11
    using nullptr_t	= decltype(nullptr);
    using max_align_t	= uintptr_t;
#endif

#if __GNUC__
    /// Returns the number of elements in a static vector
    #define VectorSize(v)	(sizeof(v) / sizeof(*v))
#else
    // Old compilers will not be able to evaluate *v on an empty vector.
    // The tradeoff here is that VectorSize will not be able to measure arrays of local structs.
    #define VectorSize(v)	(sizeof(v) / ustl::size_of_elements(1, v))
#endif

/// Returns the end() for a static vector
template <typename T, size_t N> inline constexpr T* VectorEnd (T(&a)[N]) { return &a[N]; }

/// Expands into a ptr,size expression for the given static vector; useful as link arguments.
#define VectorBlock(v)	&(v)[0], VectorSize(v)
/// Expands into a begin,end expression for the given static vector; useful for algorithm arguments.
#define VectorRange(v)	&(v)[0], VectorEnd(v)

/// Returns the number of bits in the given type
#define BitsInType(t)	(sizeof(t) * CHAR_BIT)

/// Returns the mask of type \p t with the lowest \p n bits set.
#define BitMask(t,n)	(t(~t(0)) >> (BitsInType(t) - (n)))

/// Argument that is used only in debug builds (as in an assert)
#ifndef NDEBUG
    #define DebugArg(x)	x
#else
    #define DebugArg(x)
#endif

/// Shorthand for container iteration.
#define foreach(type,i,ctr)	for (type i = (ctr).begin(); i != (ctr).end(); ++ i)
/// Shorthand for container reverse iteration.
#define eachfor(type,i,ctr)	for (type i = (ctr).rbegin(); i != (ctr).rend(); ++ i)

#ifndef DOXYGEN_SHOULD_SKIP_THIS
// Macro for passing template types as macro arguments.
// These are deprecated. Use metamac macros instead. Will remove by next release.
#define TEMPLATE_FULL_DECL1(d1,t1)		template <d1 t1>
#define TEMPLATE_FULL_DECL2(d1,t1,d2,t2)	template <d1 t1, d2 t2>
#define TEMPLATE_FULL_DECL3(d1,t1,d2,t2,d3,t3)	template <d1 t1, d2 t2, d3 t3>
#define TEMPLATE_DECL1(t1)		TEMPLATE_FULL_DECL1(typename,t1)
#define TEMPLATE_DECL2(t1,t2)		TEMPLATE_FULL_DECL2(typename,t1,typename,t2)
#define TEMPLATE_DECL3(t1,t2,t3)	TEMPLATE_FULL_DECL3(typename,t1,typename,t2,typename,t3)
#define TEMPLATE_TYPE1(type,a1)		type<a1>
#define TEMPLATE_TYPE2(type,a1,a2)	type<a1,a2>
#define TEMPLATE_TYPE3(type,a1,a2,a3)	type<a1,a2,a3>
#endif

/// Returns the minimum of \p a and \p b
template <typename T1, typename T2>
inline constexpr T1 min (const T1& a, const T2& b)
{
    return a < b ? a : b;
}

/// Returns the maximum of \p a and \p b
template <typename T1, typename T2>
inline constexpr T1 max (const T1& a, const T2& b)
{
    return b < a ? a : b;
}

/// Indexes into a static array with bounds limit
template <typename T, size_t N>
inline constexpr T& VectorElement (T(&v)[N], size_t i) { return v[min(i,N-1)]; }

/// The alignment performed by default.
const size_t c_DefaultAlignment = __alignof__(void*);

/// \brief Rounds \p n up to be divisible by \p grain
template <typename T>
inline constexpr T AlignDown (T n, size_t grain = c_DefaultAlignment)
    { return n - n % grain; }

/// \brief Rounds \p n up to be divisible by \p grain
template <typename T>
inline constexpr T Align (T n, size_t grain = c_DefaultAlignment)
    { return AlignDown (n + grain - 1, grain); }

/// Returns a nullptr pointer cast to T.
template <typename T>
inline constexpr T* NullPointer (void)
    { return nullptr; }

/// \brief Returns a non-dereferentiable value reference.
/// This is useful for passing to stream_align_of or the like which need a value but
/// don't need to actually use it.
template <typename T>
inline constexpr T& NullValue (void)
    { return *NullPointer<T>(); }

#ifndef DOXYGEN_SHOULD_SKIP_THIS
// Offsets a pointer
template <typename T>
inline T advance_ptr (T i, ptrdiff_t offset)
    { return i + offset; }

// Offsets a void pointer
template <>
inline const void* advance_ptr (const void* p, ptrdiff_t offset)
{
    assert (p || !offset);
    return reinterpret_cast<const uint8_t*>(p) + offset;
}

// Offsets a void pointer
template <>
inline void* advance_ptr (void* p, ptrdiff_t offset)
{
    assert (p || !offset);
    return reinterpret_cast<uint8_t*>(p) + offset;
}
#endif

/// Offsets an iterator
template <typename T, typename Distance>
inline T advance (T i, Distance offset)
    { return advance_ptr (i, offset); }

/// Returns the difference \p p1 - \p p2
template <typename T1, typename T2>
inline constexpr ptrdiff_t distance (T1 i1, T2 i2)
{
    return i2 - i1;
}

#ifndef DOXYGEN_SHOULD_SKIP_THIS
#define UNVOID_DISTANCE(T1const,T2const)   \
template <> inline constexpr ptrdiff_t distance (T1const void* p1, T2const void* p2) \
{ return static_cast<T2const uint8_t*>(p2) - static_cast<T1const uint8_t*>(p1); }
UNVOID_DISTANCE(,)
UNVOID_DISTANCE(const,const)
UNVOID_DISTANCE(,const)
UNVOID_DISTANCE(const,)
#undef UNVOID_DISTANCE
#endif

template <typename T>
T* addressof (T& v)
    { return reinterpret_cast<T*>(&const_cast<char&>(reinterpret_cast<const volatile char&>(v))); }

#ifndef DOXYGEN_SHOULD_SKIP_THIS
// The compiler issues a warning if an unsigned type is compared to 0.
template <typename T, bool IsSigned> struct __is_negative { inline constexpr bool operator()(const T& v) const { return v < 0; } };
template <typename T> struct __is_negative<T,false> { inline constexpr bool operator()(const T&) const { return false; } };
/// Warning-free way to check if \p v is negative, even if for unsigned types.
template <typename T> inline constexpr bool is_negative (const T& v) { return __is_negative<T,numeric_limits<T>::is_signed>()(v); }
#endif

/// \brief Returns the absolute value of \p v
/// Unlike the stdlib functions, this is inline and works with all types.
template <typename T>
inline constexpr T absv (T v)
{
    return is_negative(v) ? -v : v;
}

/// \brief Returns -1 for negative values, 1 for positive, and 0 for 0
template <typename T>
inline constexpr T sign (T v)
{
    return (0 < v) - is_negative(v);
}

/// Returns the absolute value of the distance i1 and i2
template <typename T1, typename T2>
inline constexpr size_t abs_distance (T1 i1, T2 i2)
{
    return absv (distance(i1, i2));
}

/// Returns the size of \p n elements of size \p T
template <typename T>
inline constexpr size_t size_of_elements (size_t n, const T*)
{
    return n * sizeof(T);
}

/// Returns the greatest common divisor
template <typename T>
constexpr T gcd (T a, T b)
{
    return b ? gcd(b,a%b) : absv(a);
}

/// Returns the least common multiple
template <typename T>
constexpr T lcm (T a, T b)
{
    return a/gcd(a,b)*b;
}

// Defined in byteswap.h, which is usually unusable.
#undef bswap_16
#undef bswap_32
#undef bswap_64

inline uint16_t bswap_16 (uint16_t v)
{
#if __x86__
    if (!__builtin_constant_p(v)) asm ("rorw $8, %0":"+r"(v)); else
#endif
	v = v << 8 | v >> 8;
    return v;
}
inline uint32_t bswap_32 (uint32_t v)
{
#if __x86__
    if (!__builtin_constant_p(v)) asm ("bswap %0":"+r"(v)); else
#endif
	v = v << 24 | (v & 0xFF00) << 8 | ((v >> 8) & 0xFF00) | v >> 24;
    return v;
}
#if HAVE_INT64_T
inline uint64_t bswap_64 (uint64_t v)
{
#if __x86_64__
    if (!__builtin_constant_p(v)) asm ("bswap %0":"+r"(v)); else
#endif
	v = (uint64_t(bswap_32(v)) << 32) | bswap_32(v >> 32);
    return v;
}
#endif

/// \brief Swaps the byteorder of \p v.
template <typename T>
inline T bswap (const T& v)
{
    switch (BitsInType(T)) {
	default:	return v;
	case 16:	return T (bswap_16 (uint16_t (v)));
	case 32:	return T (bswap_32 (uint32_t (v)));
#if HAVE_INT64_T
	case 64:	return T (bswap_64 (uint64_t (v)));
#endif
    }
}

#if BYTE_ORDER == BIG_ENDIAN
template <typename T> inline T le_to_native (const T& v) { return bswap (v); }
template <typename T> inline T be_to_native (const T& v) { return v; }
template <typename T> inline T native_to_le (const T& v) { return bswap (v); }
template <typename T> inline T native_to_be (const T& v) { return v; }
#elif BYTE_ORDER == LITTLE_ENDIAN
template <typename T> inline T le_to_native (const T& v) { return v; }
template <typename T> inline T be_to_native (const T& v) { return bswap (v); }
template <typename T> inline T native_to_le (const T& v) { return v; }
template <typename T> inline T native_to_be (const T& v) { return bswap (v); }
#endif // BYTE_ORDER

/// Deletes \p p and sets it to nullptr
template <typename T>
inline void Delete (T*& p)
{
    delete p;
    p = nullptr;
}

/// Deletes \p p as an array and sets it to nullptr
template <typename T>
inline void DeleteVector (T*& p)
{
    delete [] p;
    p = nullptr;
}

/// Template of making != from ! and ==
template <typename T>
inline constexpr bool operator!= (const T& x, const T& y)
    { return !(x == y); }

/// Template of making > from <
template <typename T>
inline constexpr bool operator> (const T& x, const T& y)
    { return y < x; }

/// Template of making <= from < and ==
template <typename T>
inline constexpr bool operator<= (const T& x, const T& y)
    { return !(y < x); }

/// Template of making >= from < and ==
template <typename T>
inline constexpr bool operator>= (const T& x, const T& y)
    { return !(x < y); }

/// Packs \p s multiple times into \p b. Useful for loop unrolling.
template <typename TSmall, typename TBig>
inline void pack_type (TSmall s, TBig& b)
{
    b = s;
    for (unsigned h = BitsInType(TSmall); h < BitsInType(TBig); h *= 2)
	b = (b << h)|b;
}

/// \brief Divides \p n1 by \p n2 and rounds the result up.
/// This is in contrast to regular division, which rounds down.
template <typename T1, typename T2>
inline T1 DivRU (T1 n1, T2 n2)
{
    T2 adj = n2 - 1;
    if (is_negative (n1))
	adj = -adj;
    return (n1 + adj) / n2;
}

/// Sets the contents of \p pm to 1 and returns true if the previous value was 0.
inline bool TestAndSet (int* pm)
{
#if __x86__
    int oldVal (1);
    asm volatile ("xchgl %0, %1" : "=r"(oldVal), "=m"(*pm) : "0"(oldVal), "m"(*pm) : "memory");
    return !oldVal;
#elif __sparc32__	// This has not been tested
    int rv;
    asm volatile ("ldstub %1, %0" : "=r"(rv), "=m"(*pm) : "m"(pm));
    return !rv;
#else
    const int oldVal (*pm);
    *pm = 1;
    return !oldVal;
#endif
}

/// Returns the index of the first set bit in \p v or \p nbv if none.
inline uoff_t FirstBit (uint32_t v, uoff_t nbv)
{
    uoff_t n = nbv;
#if __x86__
    if (!__builtin_constant_p(v)) asm ("bsr\t%1, %k0":"+r,r"(n):"r,m"(v)); else
#endif
#if __GNUC__
    if (v) n = 31 - __builtin_clz(v);
#else
    if (v) for (uint32_t m = uint32_t(1)<<(n=31); !(v & m); m >>= 1) --n;
#endif
    return n;
}
/// Returns the index of the first set bit in \p v or \p nbv if none.
inline uoff_t FirstBit (uint64_t v, uoff_t nbv)
{
    uoff_t n = nbv;
#if __x86_64__
    if (!__builtin_constant_p(v)) asm ("bsr\t%1, %0":"+r,r"(n):"r,m"(v)); else
#endif
#if __GNUC__ && SIZE_OF_LONG >= 8
    if (v) n = 63 - __builtin_clzl(v);
#elif __GNUC__ && HAVE_LONG_LONG && SIZE_OF_LONG_LONG >= 8
    if (v) n = 63 - __builtin_clzll(v);
#else
    if (v) for (uint64_t m = uint64_t(1)<<(n=63); !(v & m); m >>= 1) --n;
#endif
    return n;
}

/// Returns the next power of 2 >= \p v.
/// Values larger than UINT32_MAX/2 will return 2^0
inline uint32_t NextPow2 (uint32_t v)
{
    uint32_t r = v-1;
#if __x86__
    if (!__builtin_constant_p(r)) asm("bsr\t%0, %0":"+r"(r)); else
#endif
    { r = FirstBit(r,r); if (r >= BitsInType(r)-1) r = uint32_t(-1); }
    return 1<<(1+r);
}

/// Bitwise rotate value left
template <typename T>
inline T Rol (T v, size_t n)
{
#if __x86__
    if (!(__builtin_constant_p(v) && __builtin_constant_p(n))) asm("rol\t%b1, %0":"+r,r"(v):"i,c"(n)); else
#endif
    v = (v << n) | (v >> (BitsInType(T)-n));
    return v;
}

/// Bitwise rotate value right
template <typename T>
inline T Ror (T v, size_t n)
{
#if __x86__
    if (!(__builtin_constant_p(v) && __builtin_constant_p(n))) asm("ror\t%b1, %0":"+r,r"(v):"i,c"(n)); else
#endif
    v = (v >> n) | (v << (BitsInType(T)-n));
    return v;
}

/// \brief This template is to be used for dereferencing a type-punned pointer without a warning.
///
/// When casting a local variable to an unrelated type through a pointer (for
/// example, casting a float to a uint32_t without conversion), the resulting
/// memory location can be accessed through either pointer, which violates the
/// strict aliasing rule. While -fno-strict-aliasing option can be given to
/// the compiler, eliminating this warning, inefficient code may result in
/// some instances, because aliasing inhibits some optimizations. By using
/// this template, and by ensuring the memory is accessed in one way only,
/// efficient code can be produced without the warning. For gcc 4.1.0+.
///
template <typename DEST, typename SRC>
inline DEST noalias (const DEST&, SRC* s)
{
    asm("":"+g"(s)::"memory");
    union UPun { SRC s; DEST d; };
    return reinterpret_cast<UPun*>(s)->d;
}

template <typename DEST, typename SRC>
inline DEST noalias_cast (SRC s)
{
    asm("":"+g"(s)::"memory");
    union { SRC s; DEST d; } u = {s};
    return u.d;
}

namespace simd {
    /// Call after you are done using SIMD algorithms for 64 bit tuples.
    #define ALL_MMX_REGS_CHANGELIST "mm0","mm1","mm2","mm3","mm4","mm5","mm6","mm7","st","st(1)","st(2)","st(3)","st(4)","st(5)","st(6)","st(7)"
#if __3DNOW__
    inline void reset_mmx (void) { asm ("femms":::ALL_MMX_REGS_CHANGELIST); }
#elif __MMX__
    inline void reset_mmx (void) { asm ("emms":::ALL_MMX_REGS_CHANGELIST); }
#else
    inline void reset_mmx (void) {}
#endif
} // namespace simd
} // namespace ustl
