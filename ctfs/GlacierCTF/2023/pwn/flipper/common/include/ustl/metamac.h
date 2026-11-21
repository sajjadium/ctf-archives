// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.
//
/// \file metamac.h
/// \brief Macros for complex metaprogramming involving pseudoiteration.

#pragma once

//----------------------------------------------------------------------
// Functors and general utilities.
//----------------------------------------------------------------------

/// Evaluates to itself
#define ITSELF(x)		x

/// Concatenates \p a and \p b
#define PASTE(a,b)	a##b

//----------------------------------------------------------------------
// Lists and other iterators
//----------------------------------------------------------------------

/// The maximum number of elements in REPEAT, LIST, and COMMA_LIST
#define METAMAC_MAXN	9

/// Simple list with no separators. Repeats x N times.
/// @{
#define REPEAT_1(x)	x(1)
#define REPEAT_2(x)	REPEAT_1(x) x(2)
#define REPEAT_3(x)	REPEAT_2(x) x(3)
#define REPEAT_4(x)	REPEAT_3(x) x(4)
#define REPEAT_5(x)	REPEAT_4(x) x(5)
#define REPEAT_6(x)	REPEAT_5(x) x(6)
#define REPEAT_7(x)	REPEAT_6(x) x(7)
#define REPEAT_8(x)	REPEAT_7(x) x(8)
#define REPEAT_9(x)	REPEAT_8(x) x(9)
#define REPEAT(N,x)	PASTE(REPEAT_,N)(x)
/// @}

/// Simple separated list. Repeats x N times with sep in between.
/// @{
#define LIST_1(x,sep)	x(1)
#define LIST_2(x,sep)	LIST_1(x,sep) sep x(2)
#define LIST_3(x,sep)	LIST_2(x,sep) sep x(3)
#define LIST_4(x,sep)	LIST_3(x,sep) sep x(4)
#define LIST_5(x,sep)	LIST_4(x,sep) sep x(5)
#define LIST_6(x,sep)	LIST_5(x,sep) sep x(6)
#define LIST_7(x,sep)	LIST_6(x,sep) sep x(7)
#define LIST_8(x,sep)	LIST_7(x,sep) sep x(8)
#define LIST_9(x,sep)	LIST_8(x,sep) sep x(9)
#define LIST(N,x,sep)	PASTE(LIST_,N)(x,sep)
/// @}

/// Comma separated list. A special case of LIST needed because the preprocessor can't substitute commas.
/// @{
#define COMMA_LIST_1(x)	x(1)
#define COMMA_LIST_2(x)	COMMA_LIST_1(x), x(2)
#define COMMA_LIST_3(x)	COMMA_LIST_2(x), x(3)
#define COMMA_LIST_4(x)	COMMA_LIST_3(x), x(4)
#define COMMA_LIST_5(x)	COMMA_LIST_4(x), x(5)
#define COMMA_LIST_6(x)	COMMA_LIST_5(x), x(6)
#define COMMA_LIST_7(x)	COMMA_LIST_6(x), x(7)
#define COMMA_LIST_8(x)	COMMA_LIST_7(x), x(8)
#define COMMA_LIST_9(x)	COMMA_LIST_8(x), x(9)
#define COMMA_LIST(N,x)	PASTE(COMMA_LIST_,N)(x)
/// @}

//----------------------------------------------------------------------
// Macros for defining LIST arguments.
//----------------------------------------------------------------------

/// Ignores N, producing lists of identically named arguments.
#define LARG_NONE(name,N)	name

/// Appends N to name.
#define LARG_NUMBER(name,N)	name##N

/// name is a reference type.
#define LARG_REF(name,N)	name##N&

/// Sequential parameter passed by value with sequential types.
#define LARG_MT_PARAM_BY_VALUE(type,name,N)	type##N name##N

/// Sequential parameter passed by reference with sequential types.
#define LARG_MT_PARAM_BY_REF(type,name,N)	type##N& name##N

//----------------------------------------------------------------------
