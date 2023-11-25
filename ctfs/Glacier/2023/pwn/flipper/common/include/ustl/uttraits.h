// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "utypes.h"

#if HAVE_CPP11
namespace ustl {

//{{{ Helper templates and specs ---------------------------------------

/// true or false templatized constant for metaprogramming
template <typename T, T v>
struct integral_constant {
    using value_type = T;
    using type = integral_constant<value_type,v>;
    static constexpr const T value = v;
    constexpr operator value_type() const	{ return value; }
    constexpr T operator()() const		{ return value; }
};
template <typename T, T v> constexpr const T integral_constant<T,v>::value;

using true_type = integral_constant<bool, true>;
using false_type = integral_constant<bool, false>;

/// Selects type = flag ? T : U
template <bool flag, typename T, typename U> struct conditional { using type = T; };
template <typename T, typename U> struct conditional<false, T, U> { using type = U; };
template <bool flag, typename T, typename U> using conditional_t = typename conditional<flag,T,U>::type;

/// Selects bool = flag ? T : U
template <bool flag, bool T, bool U> struct t_if : public integral_constant<bool, T> {};
template <bool T, bool U> struct t_if<false, T, U> : public integral_constant<bool, U> {};

template <bool, typename T = void> struct enable_if { };
template <typename T> struct enable_if<true, T> { using type = T; };
template <bool flag, typename T> using enable_if_t = typename enable_if<flag,T>::type;

#define UNARY_TRAIT_DEFB(name,condition)	\
template <typename T> struct name : public integral_constant<bool, condition> {}
#define UNARY_TRAIT_DEFN(name)	\
template <typename T> struct name : public false_type {}
#define UNARY_TRAIT_TRUE(name,type)	\
template <> struct name<type> : public true_type {}

//}}}-------------------------------------------------------------------
//{{{ Type modifications

template <typename T> struct remove_const		{ using type = T; };
template <typename T> struct remove_const<T const>	{ using type = T; };
template <typename T> using remove_const_t = typename remove_const<T>::type;

template <typename T> struct remove_volatile		{ using type = T; };
template <typename T> struct remove_volatile<T volatile>{ using type = T; };
template <typename T> using remove_volatile_t = typename remove_volatile<T>::type;

template <typename T> struct remove_cv			{ using type = remove_volatile_t<remove_const_t<T>>; };
template <typename T> using remove_cv_t = typename remove_cv<T>::type;

template <typename T> struct add_const			{ using type = T const; };
template <typename T> struct add_const<const T>		{ using type = T const; };
template <typename T> using add_const_t = typename add_const<T>::type;

template <typename T> constexpr add_const_t<T>& as_const (T& v) { return v; }
template <class T> void as_const(const T&&) = delete;

template <typename T> struct add_volatile		{ using type = T volatile; };
template <typename T> struct add_volatile<volatile T>	{ using type = T volatile; };
template <typename T> using add_volatile_t = typename add_volatile<T>::type;

template <typename T> struct add_cv			{ using type = add_volatile_t<add_const_t<T>>; };
template <typename T> using add_cv_t = typename add_cv<T>::type;

template <typename T> struct remove_reference		{ using type = T; };
template <typename T> struct remove_reference<T&>	{ using type = T; };
template <typename T> struct remove_reference<T&&>	{ using type = T; };
template <typename T> using remove_reference_t = typename remove_reference<T>::type;

template <typename T> struct remove_pointer		{ using type = T; };
template <typename T> struct remove_pointer<T*>		{ using type = T; };
template <typename T> using remove_pointer_t = typename remove_pointer<T>::type;

template <typename T> struct add_pointer		{ using type = T*; };
template <typename T> struct add_pointer<T*>		{ using type = T*; };
template <typename T> using add_pointer_t = typename add_pointer<T>::type;

template <typename T> struct remove_extent			{ using type = T; };
template <typename T> struct remove_extent<T[]>			{ using type = T; };
template <typename T, size_t N> struct remove_extent<T[N]>	{ using type = T; };
template <typename T> using remove_extent_t = typename remove_extent<T>::type;

template <typename T> struct remove_all_extents			{ using type = T; };
template <typename T> struct remove_all_extents<T[]>		{ using type = typename remove_all_extents<T>::type; };
template <typename T, size_t N> struct remove_all_extents<T[N]>	{ using type = typename remove_all_extents<T>::type; };
template <typename T> using remove_all_extents_t = typename remove_all_extents<T>::type;

template <typename T> struct underlying_type	{ using type = __underlying_type(T); };
template <typename T> using underlying_type_t = typename underlying_type<T>::type;

#if HAVE_CPP14
template <typename...> using void_t = void;
#endif

template <typename T> struct make_signed	{ using type = T; };
template <> struct make_signed<char>		{ using type = signed char; };
template <> struct make_signed<unsigned char>	{ using type = signed char; };
template <> struct make_signed<unsigned short>	{ using type = signed short; };
template <> struct make_signed<unsigned int>	{ using type = signed int; };
template <> struct make_signed<unsigned long>	{ using type = signed long; };
#if HAVE_LONG_LONG
template <> struct make_signed<unsigned long long> { using type = signed long long; };
#endif
template <typename T> using make_signed_t = typename make_signed<T>::type;

template <typename T> struct make_unsigned	{ using type = T; };
template <> struct make_unsigned<char>		{ using type = unsigned char; };
template <> struct make_unsigned<signed char>	{ using type = unsigned char; };
template <> struct make_unsigned<short>		{ using type = unsigned short; };
template <> struct make_unsigned<int>		{ using type = unsigned int; };
template <> struct make_unsigned<long>		{ using type = unsigned long; };
#if HAVE_LONG_LONG
template <> struct make_unsigned<long long>	{ using type = unsigned long long; };
#endif
template <typename T> using make_unsigned_t = typename make_unsigned<T>::type;

//}}}-------------------------------------------------------------------
//{{{ Primary type categories

#if __clang__	// clang already has these __is_ helpers as builtins

UNARY_TRAIT_DEFB (is_void, __is_void(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_integral, __is_integral(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_signed, __is_signed(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_floating_point, __is_floating_point(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_pointer, __is_pointer(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_member_pointer, __is_member_pointer(remove_cv_t<T>));
UNARY_TRAIT_DEFB (is_member_function_pointer, __is_member_function_pointer(remove_cv_t<T>));

#else

UNARY_TRAIT_DEFN (__is_void);
UNARY_TRAIT_TRUE (__is_void, void);
UNARY_TRAIT_DEFB (is_void, __is_void<remove_cv_t<T>>::value);

UNARY_TRAIT_DEFN (__is_integral);
UNARY_TRAIT_TRUE (__is_integral, char);
#if HAVE_THREE_CHAR_TYPES
UNARY_TRAIT_TRUE (__is_integral, signed char);
#endif
UNARY_TRAIT_TRUE (__is_integral, short);
UNARY_TRAIT_TRUE (__is_integral, int);
UNARY_TRAIT_TRUE (__is_integral, long);
UNARY_TRAIT_TRUE (__is_integral, unsigned char);
UNARY_TRAIT_TRUE (__is_integral, unsigned short);
UNARY_TRAIT_TRUE (__is_integral, unsigned int);
UNARY_TRAIT_TRUE (__is_integral, unsigned long);
#if HAVE_LONG_LONG
UNARY_TRAIT_TRUE (__is_integral, long long);
UNARY_TRAIT_TRUE (__is_integral, unsigned long long);
#endif
UNARY_TRAIT_TRUE (__is_integral, wchar_t);
UNARY_TRAIT_TRUE (__is_integral, bool);
UNARY_TRAIT_DEFB (is_integral, __is_integral<remove_cv_t<T>>::value);

UNARY_TRAIT_DEFN (__is_signed);
UNARY_TRAIT_TRUE (__is_signed, char);
UNARY_TRAIT_TRUE (__is_signed, wchar_t);
UNARY_TRAIT_TRUE (__is_signed, short);
UNARY_TRAIT_TRUE (__is_signed, int);
UNARY_TRAIT_TRUE (__is_signed, long);
UNARY_TRAIT_TRUE (__is_signed, long long);
UNARY_TRAIT_DEFB (is_signed, __is_signed<remove_cv_t<T>>::value);

UNARY_TRAIT_DEFN (__is_floating_point);
//UNARY_TRAIT_TRUE (__is_floating_point, float);
//UNARY_TRAIT_TRUE (__is_floating_point, double);
//UNARY_TRAIT_TRUE (__is_floating_point, long double);
UNARY_TRAIT_DEFB (is_floating_point, __is_floating_point<remove_cv_t<T>>::value);

template <typename T> struct __is_pointer : public false_type {};
template <typename T> struct __is_pointer<T*> : public true_type {};
template <typename T> struct is_pointer : public __is_pointer<remove_cv_t<T>> {};

UNARY_TRAIT_DEFN (__is_member_pointer);
template <typename T, typename U> struct __is_member_pointer<U T::*> : public true_type {};
UNARY_TRAIT_DEFB (is_member_pointer, __is_member_pointer<remove_cv_t<T>>::value);

UNARY_TRAIT_DEFN (__is_member_function_pointer);
template <typename T, typename R> struct __is_member_function_pointer<R (T::*)(void)> : public true_type {};
template <typename T, typename R> struct __is_member_function_pointer<R (T::*)(...)> : public true_type {};
template <typename T, typename R, typename... Args>
struct __is_member_function_pointer<R (T::*)(Args...)> : public true_type {};
template <typename T, typename R, typename... Args>
struct __is_member_function_pointer<R (T::*)(Args..., ...)> : public true_type {};
UNARY_TRAIT_DEFB (is_member_function_pointer, __is_member_function_pointer<remove_cv_t<T>>::value);

#endif	// __clang__

UNARY_TRAIT_DEFB (is_unsigned, !is_signed<T>::value);
UNARY_TRAIT_DEFB (is_member_object_pointer, is_member_pointer<T>::value && !is_member_function_pointer<T>::value);

UNARY_TRAIT_DEFN (is_array);
UNARY_TRAIT_DEFN (is_lvalue_reference);
template <typename T> struct is_lvalue_reference<T&> : public true_type {};
UNARY_TRAIT_DEFN (is_rvalue_reference);
template <typename T> struct is_rvalue_reference<T&&> : public true_type {};

UNARY_TRAIT_DEFB (is_reference,	is_lvalue_reference<T>::value || is_rvalue_reference<T>::value);

template <typename T> struct is_array<T[]> : public true_type {};
template <typename T, size_t N> struct is_array<T[N]> : public true_type {};

UNARY_TRAIT_DEFB (is_union,	__is_union(T));
UNARY_TRAIT_DEFB (is_class,	__is_class(T));
UNARY_TRAIT_DEFB (is_enum,	__is_enum(T));

UNARY_TRAIT_DEFN (is_function);
template <typename R, typename... Args> struct is_function<R(Args...)> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...)> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) volatile> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) volatile &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) volatile &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) volatile> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) volatile &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) volatile &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const volatile> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const volatile &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...) const volatile &&> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const volatile> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const volatile &> : public true_type { };
template <typename R, typename... Args> struct is_function<R(Args...,...) const volatile &&> : public true_type { };

UNARY_TRAIT_DEFB (is_object, !is_reference<T>::value && !is_void<T>::value && !is_function<T>::value);
UNARY_TRAIT_DEFB (__is_referenceable, is_reference<T>::value || is_object<T>::value);
template <typename R, typename... Args>
struct __is_referenceable<R(Args...)> : public true_type {};
template <typename R, typename... Args>
struct __is_referenceable<R(Args...,...)> : public true_type {};

//}}}-------------------------------------------------------------------
//{{{ Composite type categories

UNARY_TRAIT_DEFB (is_arithmetic,	is_integral<T>::value || is_floating_point<T>::value);
UNARY_TRAIT_DEFB (is_fundamental,	is_arithmetic<T>::value || is_void<T>::value);
UNARY_TRAIT_DEFB (is_scalar,		is_arithmetic<T>::value || is_enum<T>::value || is_pointer<T>::value || is_member_pointer<T>::value);
UNARY_TRAIT_DEFB (is_compound,		!is_fundamental<T>::value);

template <typename T, bool = __is_referenceable<T>::value> struct __add_lvalue_reference { using type = T; };
template <typename T> struct __add_lvalue_reference<T, true> { using type = T&; };
template <typename T> struct add_lvalue_reference : public __add_lvalue_reference<T> {};
template <typename T> using add_lvalue_reference_t = typename add_lvalue_reference<T>::type;

template <typename T, bool = __is_referenceable<T>::value> struct __add_rvalue_reference { using type = T; };
template <typename T> struct __add_rvalue_reference<T, true> { using type = T&&; };
template <typename T> struct add_rvalue_reference : public __add_rvalue_reference<T> {};
template <typename T> using add_rvalue_reference_t = typename add_rvalue_reference<T>::type;

/// Unusable default value for T. Use with decltype.
template <typename T> add_rvalue_reference_t<T> declval (void) noexcept;

//}}}-------------------------------------------------------------------
//{{{ Type properties

UNARY_TRAIT_DEFN (is_const);
template <typename T> struct is_const<T const> : public true_type {};
UNARY_TRAIT_DEFN (is_volatile);
template <typename T> struct is_volatile<T volatile> : public true_type {};

UNARY_TRAIT_DEFB (is_empty,		__is_empty(T));
UNARY_TRAIT_DEFB (is_abstract,		__is_abstract(T));
UNARY_TRAIT_DEFB (is_literal_type,	__is_literal_type(T));
UNARY_TRAIT_DEFB (is_polymorphic,	__is_polymorphic(T));
#if HAVE_CPP14
UNARY_TRAIT_DEFB (is_final,		__is_final(T));
#endif
UNARY_TRAIT_DEFB (is_standard_layout,	__is_standard_layout(T));
UNARY_TRAIT_DEFB (is_pod,		__is_pod(T) || is_scalar<T>::value || (is_array<T>::value && is_scalar<remove_all_extents_t<T>>::value));
UNARY_TRAIT_DEFB (has_unique_object_representations,	is_pod<T>::value);
UNARY_TRAIT_DEFB (is_trivial,			is_pod<T>::value || __is_trivial(T));
UNARY_TRAIT_DEFB (is_swappable,			is_trivial<T>::value);
UNARY_TRAIT_DEFB (is_nothrow_swappable,		is_trivial<T>::value);
UNARY_TRAIT_DEFB (has_trivial_copy,		is_pod<T>::value || __has_trivial_copy(T));
UNARY_TRAIT_DEFB (has_trivial_assign,		is_pod<T>::value || __has_trivial_assign(T));
UNARY_TRAIT_DEFB (has_trivial_constructor,	is_pod<T>::value || __has_trivial_constructor(T));
UNARY_TRAIT_DEFB (has_trivial_destructor,	is_pod<T>::value || __has_trivial_destructor(T));
UNARY_TRAIT_DEFB (has_virtual_destructor,	__has_virtual_destructor(T));
UNARY_TRAIT_DEFB (has_nothrow_assign,		__has_nothrow_assign(T));
UNARY_TRAIT_DEFB (has_nothrow_copy,		__has_nothrow_copy(T));
UNARY_TRAIT_DEFB (has_nothrow_constructor,	__has_nothrow_constructor(T));

template <typename T> struct alignment_of : public integral_constant<size_t, alignof(T)> {};

template <typename T> struct rank		: public integral_constant<size_t, 0> {};
template <typename T> struct rank<T[]>		: public integral_constant<size_t, 1 + rank<T>::value> {};
template <typename T, size_t N> struct rank<T[N]> : public integral_constant<size_t, 1 + rank<T>::value> {};

template <typename T, unsigned I = 0> struct extent		{ static constexpr const size_t value = 0; };
template <typename T, unsigned I> struct extent<T[],I>		{ static constexpr const size_t value = I ? extent<T,I-1>::value : 0; };
template <typename T, unsigned I, size_t N> struct extent<T[N],I> { static constexpr const size_t value = I ? extent<T,I-1>::value : N; };

template <typename T, bool IsArray = is_array<T>::value, bool IsFunction = is_function<T>::value> struct __decay;
template <typename T> struct __decay<T, false, false>	{ using type = remove_cv_t<T>; };
template <typename T> struct __decay<T, true, false>	{ using type = remove_extent_t<T>*; };
template <typename T> struct __decay<T, false, true>	{ using type = add_pointer_t<T>; };
template <typename T> struct decay : public __decay<remove_reference_t<T>> {};
template <typename T> using decay_t = typename decay<T>::type;

template <typename ...T> struct common_type;
template <typename T> struct common_type<T> { using type = decay_t<T>; };
template <typename ...T> using common_type_t = typename common_type<T...>::type;
template <typename T, typename U> struct common_type<T, U>
    { using type = decay_t<decltype(true ? declval<T>() : declval<U>())>; };
template <typename T, typename U, typename... V>
struct common_type<T, U, V...>
    { using type = common_type_t<common_type_t<T, U>, V...>; };

//}}}-------------------------------------------------------------------
//{{{ Constructability and destructability

// All these use the standard SFINAE technique
struct __is_destructible {
    template <typename T, typename = decltype(declval<T&>().~T())> static true_type test (int);
    template <typename T> static false_type test (...);
};
template <typename T> struct is_destructible : public decltype(__is_destructible::test<T>(0)) {};

struct __is_nothrow_destructible {
    template <typename T> static integral_constant<bool, noexcept(declval<T&>().~T())> test (int);
    template<typename> static false_type test (...);
};
template<typename T>
struct is_nothrow_destructible : public decltype(__is_nothrow_destructible::test<T>(0)) {};

struct __is_default_constructible {
    template <typename T, typename = decltype(T())> static true_type test (int);
    template <typename T> static false_type test (...);
};
template <typename T> struct is_default_constructible : public decltype(__is_default_constructible::test<T>(0)) {};

struct __is_nothrow_default_constructible {
    template <typename T, typename = decltype(T())> static integral_constant<bool, noexcept(T())> test (int);
    template <typename T> static false_type test (...);
};
template <typename T> struct is_nothrow_default_constructible : public decltype(__is_nothrow_default_constructible::test<T>(0)) {};

template <typename T> struct is_constructible : public is_default_constructible<T> {};
template <typename T> struct is_nothrow_constructible : public is_nothrow_default_constructible<T> {};

struct __is_copy_constructible {
    template <typename T, typename = decltype(T(declval<T&>()))> static true_type test (int);
    template <typename T> static false_type test (...);
};
template <typename T> struct is_copy_constructible : public decltype(__is_copy_constructible::test<T>(0)) {};

struct __is_move_constructible {
    template <typename T, typename = decltype(T(declval<T&&>()))> static true_type test (int);
    template <typename T> static false_type test (...);
};
template <typename T> struct is_move_constructible : public decltype(__is_move_constructible::test<T>(0)) {};

#if __clang_major__ > 3 || (__clang_major__ == 3 && __clang_minor__ >= 9) || __GNUC__ >= 8
template <typename T, typename U> struct is_assignable : public integral_constant<bool, __is_assignable(T,U)> {};
#else
struct __is_assignable {
    template <typename T, typename U, typename = decltype(declval<T>() = declval<U>())> static true_type test (int);
    template <typename T, typename U> static false_type test (...);
};
template <typename T, typename U> struct is_assignable : public decltype(__is_assignable::test<T,U>(0)) {};
#endif

template <typename T> struct is_copy_assignable : public is_assignable<T&, const T&> {};
template <typename T> struct is_move_assignable : public is_assignable<T&, T&&> {};

// TODO: later
template <typename T> struct is_nothrow_copy_constructible : public false_type {};
template <typename T> struct is_nothrow_move_constructible : public false_type {};
template <typename T, typename U> struct is_nothrow_assignable : public false_type {};
template <typename T> struct is_nothrow_copy_assignable : public false_type {};
template <typename T> struct is_nothrow_move_assignable : public false_type {};

#if __GNUC__ >= 5
UNARY_TRAIT_DEFB (is_trivially_copyable,	__is_trivially_copyable(T));
template <typename T, typename... Args>
struct is_trivially_constructible : public integral_constant<bool, __is_trivially_constructible(T, Args...)> {};

template<typename T>
struct is_trivially_copy_constructible : public
     integral_constant<bool, is_copy_constructible<T>::value
				 && __is_trivially_constructible(T, const T&)> {};

template<typename T>
struct is_trivially_move_constructible : public
     integral_constant<bool, is_move_constructible<T>::value
				 && __is_trivially_constructible(T, T&&)> {};

template<typename T, typename U>
struct is_trivially_assignable : public integral_constant<bool, __is_trivially_assignable(T, U)> {};

UNARY_TRAIT_DEFB (is_trivially_default_constructible,	__is_trivially_constructible(T));
UNARY_TRAIT_DEFB (is_trivially_copy_assignable,	__is_trivially_assignable(T,const T&));
UNARY_TRAIT_DEFB (is_trivially_move_assignable,	__is_trivially_assignable(T,T&&));
#else
UNARY_TRAIT_DEFB (is_trivially_copyable,		__has_trivial_copy(T));
UNARY_TRAIT_DEFB (is_trivially_default_constructible,	__has_trivial_constructor(T));
UNARY_TRAIT_DEFB (is_trivially_copy_assignable,		__has_trivial_assign(T));
UNARY_TRAIT_DEFB (is_trivially_move_assignable,		false);
#endif

UNARY_TRAIT_DEFB (is_trivially_destructible,	__has_trivial_destructor(T));
UNARY_TRAIT_DEFB (has_trivial_copy_constructor,	__has_trivial_copy(T));
UNARY_TRAIT_DEFB (has_trivial_copy_assign,	__has_trivial_assign(T));

//}}}-------------------------------------------------------------------
//{{{ Type relations

template <typename T, typename U> struct is_same : public false_type {};
template <typename T> struct is_same<T,T> : public true_type {};

#if __clang__	// clang has __is_convertible builtin

template <typename F, typename T>
struct is_convertible : public integral_constant<bool, __is_convertible(F, T)> {};

#else

template <typename F, typename T, bool = is_void<F>::value || is_function<T>::value || is_array<T>::value>
class __is_convertible : public integral_constant<bool, is_void<T>::value> {};
template <typename F, typename T>
class __is_convertible<F, T, false> {
    template <typename TT> static void __test_aux(TT);
    template <typename FF, typename TT, typename = decltype(__test_aux<TT>(declval<FF>()))>
					static true_type __test(int);
    template <typename FF, typename TT> static false_type __test(...);
public:
    using type = decltype(__test<F, T>(0));
};
template <typename F, typename T>
struct is_convertible : public __is_convertible<F, T>::type {};

#endif

template <typename T, typename U> struct is_swappable_with
    : public integral_constant<bool,
		is_convertible<U,T>::value && is_convertible<T,U>::value> {};
template <typename T, typename U> struct is_nothrow_swappable_with
    : public integral_constant<bool,
		is_convertible<U,T>::value && is_convertible<T,U>::value> {};

/// Defines a has_member_function_name template where has_member_function_name<O>::value is true when O::name exists
/// Example: HAS_MEMBER_FUNCTION(read, void (O::*)(istream&)); has_member_function_read<vector<int>>::value == true
#define HAS_MEMBER_FUNCTION(name, signature)	\
template <typename T>				\
class __has_member_function_##name {		\
    template <typename O, signature> struct test_for_##name {};\
    template <typename O> static true_type found (test_for_##name<O,&O::name>*);\
    template <typename O> static false_type found (...);\
public:						\
    using type = decltype(found<T>(nullptr));	\
};						\
template <typename T>				\
struct has_member_function_##name : public __has_member_function_##name<T>::type {}

/// Defines a has_static_member_variable template where has_static_member_variable_name<O>::value is true when O::name exists
/// Example: HAS_STATIC_MEMBER_VARIABLE(int, _val); has_static_member_variable__val<A>::value == true
#define HAS_STATIC_MEMBER_VARIABLE(varT,name)	\
template <typename T>				\
class __has_static_member_variable_##name {	\
    template <typename O, add_pointer_t<decay_t<varT>> V> struct test_for_##name {};\
    template <typename O> static true_type found (test_for_##name<O,&O::name>*);\
    template <typename O> static false_type found (...);\
public:						\
    using type = decltype(found<T>(nullptr));	\
};						\
template <typename T>				\
struct has_static_member_variable_##name : public __has_static_member_variable_##name<T>::type {}

template <typename T, typename U> struct is_base_of {
    static constexpr const bool value = __is_base_of(T,U);
};
template <typename T> struct is_base_of<T,T> : public false_type {};
template <typename T> struct is_base_of<void,T> : public false_type {};

template <size_t Size, size_t Grain> struct aligned_storage
    { struct type { alignas(Grain) unsigned char _data[Size]; }; };

//}}}-------------------------------------------------------------------
//{{{ Helper templates and specs
#undef UNARY_TRAIT_DEFN
#undef UNARY_TRAIT_DEFB
#define POD_CLASS(T)			namespace ustl { UNARY_TRAIT_TRUE(is_pod,T); }
//}}}

} // namespace ustl
#endif // HAVE_CPP11
