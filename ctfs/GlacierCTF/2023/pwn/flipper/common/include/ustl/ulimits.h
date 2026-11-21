// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "utypes.h"
#include "traits.h"
#if HAVE_CPP11
    #include "uttraits.h"
#endif

namespace ustl {

enum float_denorm_style {
    denorm_indeterminate = -1,
    denorm_absent,
    denorm_present
};

enum float_round_style {
    round_indeterminate = -1,
    round_toward_zero,
    round_to_nearest,
    round_toward_infinity,
    round_toward_neg_infinity
};

namespace {
    template <typename T>
	struct __limits_digits { enum { value = sizeof(T)*8 };};
    template <typename T>
	struct __limits_digits10 { enum { value = sizeof(T)*8*643/2136+1 };};
}

/// \class numeric_limits ulimits.h ustl.h
/// \brief Defines numeric limits for a type.
///
template <typename T> 
struct numeric_limits {
    static inline constexpr T min (void)	{ return T(); }	// Returns the minimum value for type T.
    static inline constexpr T max (void)	{ return T(); }	// Returns the minimum value for type T.
    static inline constexpr T lowest (void)	{ return T(); }
    static inline constexpr T epsilon (void)		{ return T(); }
    static inline constexpr T round_error (void)	{ return T(); }
    static inline constexpr T infinity (void)		{ return T(); }
    static inline constexpr T quiet_NaN (void)		{ return T(); }
    static inline constexpr T signaling_NaN (void)	{ return T(); }
    static inline constexpr T denorm_min (void)		{ return T(); }
    static constexpr const bool is_specialized = false;
    static constexpr const bool is_signed = tm::TypeTraits<T>::isSigned;	///< True if the type is signed.
    static constexpr const bool is_integer = tm::TypeTraits<T>::isIntegral;	///< True if stores an exact value.
    static constexpr const bool is_exact = tm::TypeTraits<T>::isIntegral;	///< True if stores an exact value.
    static constexpr const bool is_integral = tm::TypeTraits<T>::isFundamental;	///< True if fixed size and cast-copyable.
    static constexpr const bool is_iec559 = false;
    static constexpr const bool is_bounded = false;
    static constexpr const bool is_modulo = false;
    static constexpr const bool has_infinity = false;
    static constexpr const bool has_quiet_NaN = false;
    static constexpr const bool has_signaling_NaN = false;
    static constexpr const bool has_denorm_loss = false;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = false;
    static constexpr const int radix = 0;
    static constexpr const int min_exponent = 0;
    static constexpr const int min_exponent10 = 0;
    static constexpr const int max_exponent = 0;
    static constexpr const int max_exponent10 = 0;
    static constexpr const float_denorm_style has_denorm = denorm_absent;
    static constexpr const float_round_style round_style = round_toward_zero;
    static constexpr const unsigned digits = __limits_digits<T>::value;		///< Number of bits in T
    static constexpr const unsigned digits10 = 0;
    static constexpr const unsigned max_digits10 = 0;
};

#ifndef DOXYGEN_SHOULD_SKIP_THIS

template <typename T>
struct numeric_limits<T*> {
    static inline constexpr T* min (void)	{ return nullptr; }
    static inline constexpr T* max (void)	{ return reinterpret_cast<T*>(UINTPTR_MAX); }
    static inline constexpr T* lowest (void)	{ return nullptr; }
    static inline constexpr T* epsilon (void)		{ return nullptr; }
    static inline constexpr T* round_error (void)	{ return nullptr; }
    static inline constexpr T* infinity (void)		{ return nullptr; }
    static inline constexpr T* quiet_NaN (void)		{ return nullptr; }
    static inline constexpr T* signaling_NaN (void)	{ return nullptr; }
    static inline constexpr T* denorm_min (void)	{ return nullptr; }
    static constexpr const bool is_specialized = false;
    static constexpr const bool is_signed = false;
    static constexpr const bool is_integer = true;
    static constexpr const bool is_exact = true;
    static constexpr const bool is_integral = true;
    static constexpr const bool is_iec559 = false;
    static constexpr const bool is_bounded = true;
    static constexpr const bool is_modulo = true;
    static constexpr const bool has_infinity = false;
    static constexpr const bool has_quiet_NaN = false;
    static constexpr const bool has_signaling_NaN = false;
    static constexpr const bool has_denorm_loss = false;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = false;
    static constexpr const int radix = 2;
    static constexpr const int min_exponent = 0;
    static constexpr const int min_exponent10 = 0;
    static constexpr const int max_exponent = 0;
    static constexpr const int max_exponent10 = 0;
    static constexpr const float_denorm_style has_denorm = denorm_absent;
    static constexpr const float_round_style round_style = round_toward_zero;
    static constexpr const unsigned digits = __limits_digits<T*>::value;
    static constexpr const unsigned digits10 = __limits_digits10<T*>::value;
    static constexpr const unsigned max_digits10 = 0;
};
/*
template <> struct numeric_limits<float> {
    static inline constexpr float min (void)		{ return FLT_MIN; }
    static inline constexpr float max (void)		{ return FLT_MAX; }
    static inline constexpr float lowest (void)		{ return -FLT_MAX; }
    static inline constexpr float epsilon (void)	{ return FLT_EPSILON; }
    static inline constexpr float round_error (void)	{ return 0.5f; }
    static inline constexpr float infinity (void)	{ return __builtin_huge_valf(); }
    static inline constexpr float quiet_NaN (void)	{ return __builtin_nanf(""); }
    static inline constexpr float signaling_NaN (void)	{ return __builtin_nansf(""); }
    static inline constexpr float denorm_min (void)	{ return __FLT_DENORM_MIN__; }
    static constexpr const bool is_specialized = true;
    static constexpr const bool is_signed = true;
    static constexpr const bool is_integer = false;
    static constexpr const bool is_exact = false;
    static constexpr const bool is_integral = true;
    static constexpr const bool is_iec559 = true;
    static constexpr const bool is_bounded = true;
    static constexpr const bool is_modulo = false;
    static constexpr const bool has_infinity = __FLT_HAS_INFINITY__;
    static constexpr const bool has_quiet_NaN = __FLT_HAS_QUIET_NAN__;
    static constexpr const bool has_signaling_NaN = __FLT_HAS_QUIET_NAN__;
    static constexpr const bool has_denorm_loss = true;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = true;
    static constexpr const int radix = FLT_RADIX;
    static constexpr const int min_exponent = FLT_MIN_EXP;
    static constexpr const int min_exponent10 = FLT_MIN_10_EXP;
    static constexpr const int max_exponent = FLT_MAX_EXP;
    static constexpr const int max_exponent10 = FLT_MAX_10_EXP;
    static constexpr const float_denorm_style has_denorm = denorm_present;
    static constexpr const float_round_style round_style = round_to_nearest;
    static constexpr const unsigned digits = FLT_MANT_DIG;
    static constexpr const unsigned digits10 = FLT_DIG;
    static constexpr const unsigned max_digits10 = FLT_MANT_DIG;
};

template <> struct numeric_limits<double> {
    static inline constexpr double min (void)		{ return DBL_MIN; }
    static inline constexpr double max (void)		{ return DBL_MAX; }
    static inline constexpr double lowest (void)		{ return -DBL_MAX; }
    static inline constexpr double epsilon (void)	{ return DBL_EPSILON; }
    static inline constexpr double round_error (void)	{ return 0.5; }
    static inline constexpr double infinity (void)	{ return __builtin_huge_val(); }
    static inline constexpr double quiet_NaN (void)	{ return __builtin_nan(""); }
    static inline constexpr double signaling_NaN (void)	{ return __builtin_nans(""); }
    static inline constexpr double denorm_min (void)	{ return __DBL_DENORM_MIN__; }
    static constexpr const bool is_specialized = true;
    static constexpr const bool is_signed = true;
    static constexpr const bool is_integer = false;
    static constexpr const bool is_exact = false;
    static constexpr const bool is_integral = true;
    static constexpr const bool is_iec559 = true;
    static constexpr const bool is_bounded = true;
    static constexpr const bool is_modulo = false;
    static constexpr const bool has_infinity = __DBL_HAS_INFINITY__;
    static constexpr const bool has_quiet_NaN = __DBL_HAS_QUIET_NAN__;
    static constexpr const bool has_signaling_NaN = __DBL_HAS_QUIET_NAN__;
    static constexpr const bool has_denorm_loss = true;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = true;
    static constexpr const int radix = FLT_RADIX;
    static constexpr const int min_exponent = DBL_MIN_EXP;
    static constexpr const int min_exponent10 = DBL_MIN_10_EXP;
    static constexpr const int max_exponent = DBL_MAX_EXP;
    static constexpr const int max_exponent10 = DBL_MAX_10_EXP;
    static constexpr const float_denorm_style has_denorm = denorm_present;
    static constexpr const float_round_style round_style = round_to_nearest;
    static constexpr const unsigned digits = DBL_MANT_DIG;
    static constexpr const unsigned digits10 = DBL_DIG;
    static constexpr const unsigned max_digits10 = DBL_MANT_DIG;
};

template <> struct numeric_limits<long double> {
    static inline constexpr long double min (void)		{ return LDBL_MIN; }
    static inline constexpr long double max (void)		{ return LDBL_MAX; }
    static inline constexpr long double lowest (void)		{ return -LDBL_MAX; }
    static inline constexpr long double epsilon (void)		{ return LDBL_EPSILON; }
    static inline constexpr long double round_error (void)	{ return 0.5l; }
    static inline constexpr long double infinity (void)		{ return __builtin_huge_vall(); }
    static inline constexpr long double quiet_NaN (void)	{ return __builtin_nanl(""); }
    static inline constexpr long double signaling_NaN (void)	{ return __builtin_nansl(""); }
    static inline constexpr long double denorm_min (void)	{ return __LDBL_DENORM_MIN__; }
    static constexpr const bool is_specialized = true;
    static constexpr const bool is_signed = true;
    static constexpr const bool is_integer = false;
    static constexpr const bool is_exact = false;
    static constexpr const bool is_integral = true;
    static constexpr const bool is_iec559 = true;
    static constexpr const bool is_bounded = true;
    static constexpr const bool is_modulo = false;
    static constexpr const bool has_infinity = __LDBL_HAS_INFINITY__;
    static constexpr const bool has_quiet_NaN = __LDBL_HAS_QUIET_NAN__;
    static constexpr const bool has_signaling_NaN = __LDBL_HAS_QUIET_NAN__;
    static constexpr const bool has_denorm_loss = true;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = true;
    static constexpr const int radix = FLT_RADIX;
    static constexpr const int min_exponent = LDBL_MIN_EXP;
    static constexpr const int min_exponent10 = LDBL_MIN_10_EXP;
    static constexpr const int max_exponent = LDBL_MAX_EXP;
    static constexpr const int max_exponent10 = LDBL_MAX_10_EXP;
    static constexpr const float_denorm_style has_denorm = denorm_present;
    static constexpr const float_round_style round_style = round_to_nearest;
    static constexpr const unsigned digits = LDBL_MANT_DIG;
    static constexpr const unsigned digits10 = LDBL_DIG;
    static constexpr const unsigned max_digits10 = LDBL_MANT_DIG;
};

template <> struct numeric_limits<long double> {
    static inline constexpr long double min (void)		{ return LDBL_MIN; }
    static inline constexpr long double max (void)		{ return LDBL_MAX; }
    static inline constexpr long double lowest (void)		{ return -LDBL_MAX; }
    static inline constexpr long double epsilon (void)		{ return LDBL_EPSILON; }
    static inline constexpr long double round_error (void)	{ return 0.5l; }
    static inline constexpr long double infinity (void)		{ return __builtin_huge_vall(); }
    static inline constexpr long double quiet_NaN (void)	{ return __builtin_nanl(""); }
    static inline constexpr long double signaling_NaN (void)	{ return __builtin_nansl(""); }
    static inline constexpr long double denorm_min (void)	{ return __LDBL_DENORM_MIN__; }
    static constexpr const bool is_specialized = true;
    static constexpr const bool is_signed = true;
    static constexpr const bool is_integer = false;
    static constexpr const bool is_exact = false;
    static constexpr const bool is_integral = true;
    static constexpr const bool is_iec559 = true;
    static constexpr const bool is_bounded = true;
    static constexpr const bool is_modulo = false;
    static constexpr const bool has_infinity = __LDBL_HAS_INFINITY__;
    static constexpr const bool has_quiet_NaN = __LDBL_HAS_QUIET_NAN__;
    static constexpr const bool has_signaling_NaN = __LDBL_HAS_QUIET_NAN__;
    static constexpr const bool has_denorm_loss = true;
    static constexpr const bool traps = false;
    static constexpr const bool tinyness_before = true;
    static constexpr const int radix = FLT_RADIX;
    static constexpr const int min_exponent = LDBL_MIN_EXP;
    static constexpr const int min_exponent10 = LDBL_MIN_10_EXP;
    static constexpr const int max_exponent = LDBL_MAX_EXP;
    static constexpr const int max_exponent10 = LDBL_MAX_10_EXP;
    static constexpr const float_denorm_style has_denorm = denorm_present;
    static constexpr const float_round_style round_style = round_to_nearest;
    static constexpr const unsigned digits = LDBL_MANT_DIG;
    static constexpr const unsigned digits10 = LDBL_DIG;
    static constexpr const unsigned max_digits10 = LDBL_MANT_DIG;
    };*/

#define _NUMERIC_LIMITS(type, minVal, maxVal, bSigned, bInteger, bIntegral)	\
template <> struct numeric_limits<type> {					\
    static inline constexpr type min (void)		{ return minVal; }	\
    static inline constexpr type max (void)		{ return maxVal; }	\
    static inline constexpr type lowest (void)		{ return minVal; }	\
    static inline constexpr type epsilon (void)		{ return 0; }	\
    static inline constexpr type round_error (void)	{ return 0; }	\
    static inline constexpr type infinity (void)	{ return 0; }	\
    static inline constexpr type quiet_NaN (void)	{ return 0; }	\
    static inline constexpr type signaling_NaN (void)	{ return 0; }	\
    static inline constexpr type denorm_min (void)	{ return 0; }	\
    static constexpr const bool is_specialized = true;		\
    static constexpr const bool is_signed = bSigned;		\
    static constexpr const bool is_integer = bInteger;		\
    static constexpr const bool is_exact = bInteger;		\
    static constexpr const bool is_integral = bIntegral;	\
    static constexpr const bool is_iec559 = false;		\
    static constexpr const bool is_bounded = true;		\
    static constexpr const bool is_modulo = bIntegral;		\
    static constexpr const bool has_infinity = false;		\
    static constexpr const bool has_quiet_NaN = false;		\
    static constexpr const bool has_signaling_NaN = false;	\
    static constexpr const bool has_denorm_loss = false;	\
    static constexpr const bool traps = false;			\
    static constexpr const bool tinyness_before = false;	\
    static constexpr const int radix = 2;			\
    static constexpr const int min_exponent = 0;		\
    static constexpr const int min_exponent10 = 0;		\
    static constexpr const int max_exponent = 0;		\
    static constexpr const int max_exponent10 = 0;		\
    static constexpr const float_denorm_style has_denorm = denorm_absent;	\
    static constexpr const float_round_style round_style = round_toward_zero;	\
    static constexpr const unsigned digits = __limits_digits<type>::value;	\
    static constexpr const unsigned digits10 = __limits_digits10<type>::value;	\
    static constexpr const unsigned max_digits10 = 0;		\
}

//--------------------------------------------------------------------------------------
//		type		min		max		signed	integer	integral
//--------------------------------------------------------------------------------------
_NUMERIC_LIMITS (bool,		false,		true,		false,	false,	true);
_NUMERIC_LIMITS (char,		CHAR_MIN,	CHAR_MAX,	true,	true,	true);
_NUMERIC_LIMITS (int,		INT_MIN,	INT_MAX,	true,	true,	true);
_NUMERIC_LIMITS (short,		SHRT_MIN,	SHRT_MAX,	true,	true,	true);
_NUMERIC_LIMITS (long,		LONG_MIN,	LONG_MAX,	true,	true,	true);
#if HAVE_THREE_CHAR_TYPES
_NUMERIC_LIMITS (signed char,	SCHAR_MIN,	SCHAR_MAX,	true,	true,	true);
#endif
_NUMERIC_LIMITS (unsigned char,	0,		UCHAR_MAX,	false,	true,	true);
_NUMERIC_LIMITS (unsigned int,	0,		UINT_MAX,	false,	true,	true);
_NUMERIC_LIMITS (unsigned short,0,		USHRT_MAX,	false,	true,	true);
_NUMERIC_LIMITS (unsigned long,	0,		ULONG_MAX,	false,	true,	true);
_NUMERIC_LIMITS (wchar_t,	0,		WCHAR_MAX,	false,	true,	true);
#if HAVE_LONG_LONG
_NUMERIC_LIMITS (long long,	LLONG_MIN,	LLONG_MAX,	true,	true,	true);
_NUMERIC_LIMITS (unsigned long long,	0,	ULLONG_MAX,	false,	true,	true);
#endif
//--------------------------------------------------------------------------------------

#endif // DOXYGEN_SHOULD_SKIP_THIS

/// Macro for defining numeric_limits specializations
#define NUMERIC_LIMITS(type, minVal, maxVal, bSigned, bInteger, bIntegral)	\
namespace ustl { _NUMERIC_LIMITS (type, minVal, maxVal, bSigned, bInteger, bIntegral); }

} // namespace ustl
