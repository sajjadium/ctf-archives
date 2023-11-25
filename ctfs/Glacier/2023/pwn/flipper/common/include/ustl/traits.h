// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2007 by Mike Sharov <msharov@users.sourceforge.net>
//
// This implementation is adapted from the Loki library, distributed under
// the MIT license with Copyright (c) 2001 by Andrei Alexandrescu.

#pragma once
#include "typelist.h"

namespace ustl {
namespace tm {

//----------------------------------------------------------------------
// Type classes and type modifiers
//----------------------------------------------------------------------

typedef tl::Seq<unsigned char, unsigned short, unsigned, unsigned long>::Type
							StdUnsignedInts;
typedef tl::Seq<signed char, short, int, long>::Type	StdSignedInts;
typedef tl::Seq<bool, char, wchar_t>::Type		StdOtherInts;
typedef tl::Seq</*float, double*/>::Type			StdFloats;

template <typename U> struct Identity			{ typedef U Result; };
template <typename U> struct AddPointer			{ typedef U* Result; };
template <typename U> struct AddPointer<U&>		{ typedef U* Result; };
template <typename U> struct AddReference		{ typedef U& Result; };
template <typename U> struct AddReference<U&>		{ typedef U& Result; };
template <>           struct AddReference<void>		{ typedef NullType Result; };
template <typename U> struct AddParameterType		{ typedef const U& Result; };
template <typename U> struct AddParameterType<U&>	{ typedef U& Result; };
template <>           struct AddParameterType<void>	{ typedef NullType Result; };
template <typename U> struct RemoveReference		{ typedef U Result; };
template <typename U> struct RemoveReference<U&>	{ typedef U Result; };
#if HAVE_CPP11
template <typename U> struct RemoveReference<U&&>	{ typedef U Result; };
#endif
template <bool, typename T> struct EnableIf		{ typedef void Result; };
template <typename T> struct EnableIf<true, T>		{ typedef T Result; };


//----------------------------------------------------------------------
// Function pointer testers
//----------------------------------------------------------------------
// Macros expand to numerous parameters

template <typename T>
struct IsFunctionPointerRaw { enum { result = false}; };
template <typename T>
struct IsMemberFunctionPointerRaw { enum { result = false}; };

#define TM_FPR_MAXN		9
#define TM_FPR_TYPE(n)		PASTE(T,n)
#define TM_FPR_TYPENAME(n)	typename TM_FPR_TYPE(n)

// First specialize for regular functions
template <typename T>
struct IsFunctionPointerRaw<T(*)(void)> 
{enum {result = true};};

#define TM_FPR_SPEC(n)		\
template <typename T, COMMA_LIST(n, TM_FPR_TYPENAME)>		\
struct IsFunctionPointerRaw<T(*)(COMMA_LIST(n, TM_FPR_TYPE))>	\
{ enum { result = true }; }

LIST (TM_FPR_MAXN, TM_FPR_SPEC, ;);

// Then for those with an ellipsis argument
template <typename T>
struct IsFunctionPointerRaw<T(*)(...)> 
{enum {result = true};};

#define TM_FPR_SPEC_ELLIPSIS(n)	\
template <typename T, COMMA_LIST(n, TM_FPR_TYPENAME)>			\
struct IsFunctionPointerRaw<T(*)(COMMA_LIST(n, TM_FPR_TYPE), ...)>	\
{ enum { result = true }; }

LIST (TM_FPR_MAXN, TM_FPR_SPEC_ELLIPSIS, ;);

// Then for member function pointers
template <typename T, typename S>
struct IsMemberFunctionPointerRaw<T (S::*)(void)> 
{ enum { result = true }; };

#define TM_MFPR_SPEC(n)		\
template <typename T, typename S, COMMA_LIST(n, TM_FPR_TYPENAME)>	\
struct IsMemberFunctionPointerRaw<T (S::*)(COMMA_LIST(n, TM_FPR_TYPE))>	\
{ enum { result = true };};

LIST (TM_FPR_MAXN, TM_MFPR_SPEC, ;);

// Then for member function pointers with an ellipsis argument
template <typename T, typename S>
struct IsMemberFunctionPointerRaw<T (S::*)(...)> 
{ enum { result = true }; };

#define TM_MFPR_SPEC_ELLIPSIS(n)		\
template <typename T, typename S, COMMA_LIST(n, TM_FPR_TYPENAME)>	\
struct IsMemberFunctionPointerRaw<T (S::*)(COMMA_LIST(n, TM_FPR_TYPE), ...)> \
{ enum { result = true }; };

LIST (TM_FPR_MAXN, TM_MFPR_SPEC_ELLIPSIS, ;);

// Then for const member function pointers (getting tired yet?)
template <typename T, typename S>
struct IsMemberFunctionPointerRaw<T (S::*)(void) const> 
{ enum { result = true }; };

#define TM_CMFPR_SPEC(n)	\
template <typename T, typename S, COMMA_LIST(n, TM_FPR_TYPENAME)>	\
struct IsMemberFunctionPointerRaw<T (S::*)(COMMA_LIST(n, TM_FPR_TYPE)) const>	\
{ enum { result = true };};

LIST (TM_FPR_MAXN, TM_CMFPR_SPEC, ;);

// Finally for const member function pointers with an ellipsis argument (whew!)
template <typename T, typename S>
struct IsMemberFunctionPointerRaw<T (S::*)(...) const> 
{ enum { result = true }; };

#define TM_CMFPR_SPEC_ELLIPSIS(n)		\
template <typename T, typename S, COMMA_LIST(n, TM_FPR_TYPENAME)>	\
struct IsMemberFunctionPointerRaw<T (S::*)(COMMA_LIST(n, TM_FPR_TYPE), ...) const> \
{ enum { result = true }; };

LIST (TM_FPR_MAXN, TM_CMFPR_SPEC_ELLIPSIS, ;);

#undef TM_FPR_SPEC
#undef TM_FPR_SPEC_ELLIPSIS
#undef TM_MFPR_SPEC
#undef TM_MFPR_SPEC_ELLIPSIS
#undef TM_CMFPR_SPEC
#undef TM_CMFPR_SPEC_ELLIPSIS
#undef TM_FPR_TYPENAME
#undef TM_FPR_TYPE
#undef TM_FPR_MAXN

//----------------------------------------------------------------------
// Type traits template
//----------------------------------------------------------------------

/// Figures out at compile time various properties of any given type
/// Invocations (T is a type, TypeTraits<T>::Propertie):
///
/// - isPointer       : returns true if T is a pointer type
/// - PointeeType     : returns the type to which T points if T is a pointer 
///                     type, NullType otherwise
/// - isReference     : returns true if T is a reference type
/// - isLValue        : returns true if T is an lvalue
/// - isRValue        : returns true if T is an rvalue
/// - ReferredType    : returns the type to which T refers if T is a reference 
///                     type, NullType otherwise
/// - isMemberPointer : returns true if T is a pointer to member type
/// - isStdUnsignedInt: returns true if T is a standard unsigned integral type
/// - isStdSignedInt  : returns true if T is a standard signed integral type
/// - isStdIntegral   : returns true if T is a standard integral type
/// - isStdFloat      : returns true if T is a standard floating-point type
/// - isStdArith      : returns true if T is a standard arithmetic type
/// - isStdFundamental: returns true if T is a standard fundamental type
/// - isUnsignedInt   : returns true if T is a unsigned integral type
/// - isSignedInt     : returns true if T is a signed integral type
/// - isIntegral      : returns true if T is a integral type
/// - isFloat         : returns true if T is a floating-point type
/// - isArith         : returns true if T is a arithmetic type
/// - isFundamental   : returns true if T is a fundamental type
/// - ParameterType   : returns the optimal type to be used as a parameter for 
///                     functions that take Ts
/// - isConst         : returns true if T is a const-qualified type
/// - NonConstType    : Type with removed 'const' qualifier from T, if any
/// - isVolatile      : returns true if T is a volatile-qualified type
/// - NonVolatileType : Type with removed 'volatile' qualifier from T, if any
/// - UnqualifiedType : Type with removed 'const' and 'volatile' qualifiers from 
///                     T, if any
/// - ConstParameterType: returns the optimal type to be used as a parameter 
///                       for functions that take 'const T's
///
template <typename T>
class TypeTraits {
private:
    #define TMTT1	template <typename U> struct
    #define TMTT2	template <typename U, typename V> struct
    TMTT1 ReferenceTraits	{ enum { result = false, lvalue = true, rvalue = false }; typedef U ReferredType; };
    TMTT1 ReferenceTraits<U&>	{ enum { result = true,  lvalue = true, rvalue = false }; typedef U ReferredType; };
    TMTT1 PointerTraits		{ enum { result = false }; typedef NullType PointeeType; };
    TMTT1 PointerTraits<U*>	{ enum { result = true  }; typedef U PointeeType; };
    TMTT1 PointerTraits<U*&>	{ enum { result = true  }; typedef U PointeeType; };
    TMTT1 PToMTraits		{ enum { result = false }; };
    TMTT2 PToMTraits<U V::*>	{ enum { result = true  }; };
    TMTT2 PToMTraits<U V::*&>	{ enum { result = true  }; };
    TMTT1 FunctionPointerTraits	{ enum { result = IsFunctionPointerRaw<U>::result }; };
    TMTT1 PToMFunctionTraits	{ enum { result = IsMemberFunctionPointerRaw<U>::result }; };
    TMTT1 UnConst		{ typedef U Result;  enum { isConst = false }; };
    TMTT1 UnConst<const U>	{ typedef U Result;  enum { isConst = true  }; };
    TMTT1 UnConst<const U&>	{ typedef U& Result; enum { isConst = true  }; };
    TMTT1 UnVolatile		{ typedef U Result;  enum { isVolatile = false }; };
    TMTT1 UnVolatile<volatile U>{ typedef U Result;  enum { isVolatile = true  }; };
    TMTT1 UnVolatile<volatile U&> {typedef U& Result;enum { isVolatile = true  }; };
#if HAVE_CPP11
    TMTT1 ReferenceTraits<U&&>	{ enum { result = true,  lvalue = false, rvalue = true }; typedef U ReferredType; };
    TMTT1 PointerTraits<U*&&>	{ enum { result = true  }; typedef U PointeeType; };
    TMTT2 PToMTraits<U V::*&&>	{ enum { result = true  }; };
    TMTT1 UnConst<const U&&>	{ typedef U&& Result; enum { isConst = true  }; };
    TMTT1 UnVolatile<volatile U&&> {typedef U&& Result;enum { isVolatile = true  }; };
#endif
    #undef TMTT2
    #undef TMTT1
public:
    typedef typename UnConst<T>::Result 
	NonConstType;
    typedef typename UnVolatile<T>::Result 
	NonVolatileType;
    typedef typename UnVolatile<typename UnConst<T>::Result>::Result 
	UnqualifiedType;
    typedef typename PointerTraits<UnqualifiedType>::PointeeType 
	PointeeType;
    typedef typename ReferenceTraits<T>::ReferredType 
	ReferredType;

    enum { isConst		= UnConst<T>::isConst };
    enum { isVolatile		= UnVolatile<T>::isVolatile };
    enum { isReference		= ReferenceTraits<UnqualifiedType>::result };
    enum { isLValue		= ReferenceTraits<UnqualifiedType>::lvalue };
    enum { isRValue		= ReferenceTraits<UnqualifiedType>::rvalue };
    enum { isFunction		= FunctionPointerTraits<typename AddPointer<T>::Result >::result };
    enum { isFunctionPointer	= FunctionPointerTraits<
				    typename ReferenceTraits<UnqualifiedType>::ReferredType >::result };
    enum { isMemberFunctionPointer= PToMFunctionTraits<
				    typename ReferenceTraits<UnqualifiedType>::ReferredType >::result };
    enum { isMemberPointer	= PToMTraits<
				    typename ReferenceTraits<UnqualifiedType>::ReferredType >::result ||
				    isMemberFunctionPointer };
    enum { isPointer		= PointerTraits<
				    typename ReferenceTraits<UnqualifiedType>::ReferredType >::result ||
				    isFunctionPointer };
    enum { isStdUnsignedInt	= tl::IndexOf<StdUnsignedInts, UnqualifiedType>::value >= 0 ||
				    tl::IndexOf<StdUnsignedInts,
					typename ReferenceTraits<UnqualifiedType>::ReferredType>::value >= 0};
    enum { isStdSignedInt	= tl::IndexOf<StdSignedInts, UnqualifiedType>::value >= 0 ||
				    tl::IndexOf<StdSignedInts,
					typename ReferenceTraits<UnqualifiedType>::ReferredType>::value >= 0};
    enum { isStdIntegral	= isStdUnsignedInt || isStdSignedInt ||
				    tl::IndexOf<StdOtherInts, UnqualifiedType>::value >= 0 ||
				    tl::IndexOf<StdOtherInts,
					typename ReferenceTraits<UnqualifiedType>::ReferredType>::value >= 0};
    enum { isStdFloat		= tl::IndexOf<StdFloats, UnqualifiedType>::value >= 0 ||
				    tl::IndexOf<StdFloats,
					typename ReferenceTraits<UnqualifiedType>::ReferredType>::value >= 0};
    enum { isStdArith		= isStdIntegral || isStdFloat };
    enum { isStdFundamental	= isStdArith || isStdFloat || Conversion<T, void>::sameType };

    enum { isUnsignedInt	= isStdUnsignedInt };
    enum { isUnsigned		= isUnsignedInt || isPointer };
    enum { isSignedInt		= isStdSignedInt };
    enum { isIntegral		= isStdIntegral || isUnsignedInt || isSignedInt };
    enum { isFloat		= isStdFloat };
    enum { isSigned		= isSignedInt || isFloat };
    enum { isArith		= isIntegral || isFloat };
    enum { isFundamental	= isStdFundamental || isArith };
    
    typedef typename Select<isStdArith || isPointer || isMemberPointer, T, 
	    typename AddParameterType<T>::Result>::Result
	ParameterType;
};

} // namespace tm
} // namespace ustl
