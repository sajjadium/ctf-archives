// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2007 by Mike Sharov <msharov@users.sourceforge.net>
//
// This implementation is adapted from the Loki library, distributed under
// the MIT license with Copyright (c) 2001 by Andrei Alexandrescu.

#pragma once

namespace ustl {
/// Template metaprogramming tools
namespace tm {

/// An empty type useful as a placeholder.
class NullType { };

/// Converts an integer to a type.
template <int v> struct Int2Type { enum { value = v }; };

/// Converts an type to a unique empty type.
template <typename T> struct Type2Type { typedef T OriginalType; };

/// Selects type Result = flag ? T : U
template <bool flag, typename T, typename U>
struct Select { typedef T Result; };
template <typename T, typename U>
struct Select<false, T, U> { typedef U Result; };

/// IsSameType<T,U>::value is true when T=U
template <typename T, typename U>
struct IsSameType { enum { value = false }; };
template <typename T>
struct IsSameType<T,T> { enum { value = true }; };

/// \brief Checks for conversion possibilities between T and U
/// Conversion<T,U>::exists is true if T is convertible to U
/// Conversion<T,U>::sameType is true if U is T
template <typename T, typename U>
struct Conversion {
private:
    typedef char UT;
    typedef short TT;
    static UT Test (U);
    static TT Test (...);
    static T MakeT (void);
public:
    enum {
	exists = sizeof(UT) == sizeof(Test(MakeT())),
	sameType = false
    };
};
template <typename T>
struct Conversion<T, T> { enum { exists = true, sameType = true }; };
template <typename T>
struct Conversion<void, T> { enum { exists = false, sameType = false }; };
template <typename T>
struct Conversion<T, void> { enum { exists = false, sameType = false }; };
template <>
struct Conversion<void, void> { enum { exists = true, sameType = true }; };

/// SuperSubclass<T,U>::value is true when U is derived from T, or when U is T
template <typename T, typename U>
struct SuperSubclass {
    enum { value = (::ustl::tm::Conversion<const volatile U*, const volatile T*>::exists &&
		    !::ustl::tm::Conversion<const volatile T*, const volatile void*>::sameType) };
    enum { dontUseWithIncompleteTypes = sizeof(T)==sizeof(U) };	// Dummy enum to make sure that both classes are fully defined.
};
template <>
struct SuperSubclass<void, void> { enum { value = false }; };
template <typename U>
struct SuperSubclass<void, U> {
    enum { value = false };
    enum { dontUseWithIncompleteTypes = 0==sizeof(U) };
};
template <typename T>
struct SuperSubclass<T, void> {
    enum { value = false };
    enum { dontUseWithIncompleteTypes = 0==sizeof(T) };
};

/// SuperSubclassStrict<T,U>::value is true when U is derived from T
template <typename T, typename U>
struct SuperSubclassStrict {
    enum { value = SuperSubclass<T,U>::value &&
		    !::ustl::tm::Conversion<const volatile T*, const volatile U*>::sameType };
};

#if !HAVE_CPP11
// static assert support
template <bool> struct CompileTimeError;
template <> struct CompileTimeError<true> {};
#define static_assert(cond,msg)	{ ::ustl::tm::CompileTimeError<!!(cond)> ERROR_##msg; (void) ERROR_##msg; }
#endif

} // namespace tm
} // namespace ustl
