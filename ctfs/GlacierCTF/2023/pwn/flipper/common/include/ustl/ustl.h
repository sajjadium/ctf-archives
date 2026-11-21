// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "ustl/uspecial.h"
#include "ustl/umap.h"
#include "ustl/umultimap.h"
#include "ustl/ustack.h"
#include "ustl/uqueue.h"
#include "ustl/unumeric.h"
#include "ustl/ulist.h"
#include "ustl/uheap.h"

/// \mainpage
///
/// \section intro Introduction
///
/// uSTL is a partial implementation of the STL specification intended to
/// reduce code size of the derivative programs. Usually, the STL containers
/// manage their own storage with new[] and delete[] operators, which create
/// strongly typed storage. That is the standard way of allocating C++ object
/// vectors, allowing appropriate constructors and destructors to be called on
/// the allocated storage and ensuring that objects are copied via their copy
/// operators. Although type safety is a good thing, placing memory management
/// code into a template necessitates its reinstantiation for every template
/// instance used by the derivative program. This produces substantial code
/// bloat, that is frequently derided by C developers and used by them as
/// an argument that C is better than C++. The uSTL implementation solves
/// this problem by factoring memory management code into a non-template base
/// class, ustl::memblock, which performs unstructured memory allocation. STL
/// containers are then implemented as template wrappers for memblock to
/// provide a measure of type safety. The result is that each template
/// instantiation contains less code, and although it does not completely
/// "disappear", due to the requirement for calling placement constructors
/// on the allocated memory, most of it does, being replaced by calls to
/// memblock methods. The base classes for unstructured storage management
/// (cmemlink - link to constant memory, memlink - link to mutable memory,
/// and memblock - owner of mutable memory) are, of course, also available
/// for use as data buffers wherever those are needed, and streams that
/// efficiently read and write binary data into them are also available.
//
/// \defgroup Containers Containers
/// Here you'll find all the containers for your objects and data.
//
///	\defgroup MemoryManagement Memory Management
///	\ingroup Containers
///	Classes that implement low-level memory management and form the base for
///	all containers in the library. Almost all functionality in the containers
///	is reduced to calls to these base classes through a great deal of inline
///	crunching by the compiler, and thus you end up storing all your data in
///	ustl::memblock objects with the container templates as mere syntactic sugar.
//
///	\defgroup Sequences Sequence Containers
///	\ingroup Containers
///	Containers containing sequences of objects.
//
///	\defgroup AssociativeContainers Associative Containers
///	\ingroup Containers
///	Containers containing associations of objects.
//
/// \defgroup Streams Streams
/// Streams convert objects into flat data.
//
/// 	\defgroup BinaryStreams Binary Streams
///	\ingroup Streams
///	Unlike the C++ standard library,
///	the default behaviour is very strongly biased toward binary streams. I
///	believe that text formats should be used very sparingly due to numerous
///	problems they cause, such as total lack of structure, buffer overflows,
///	the great multitude of formats and encodings for even the most
///	trivial of things like integers, and the utter lack of readability
///	despite ardent claims to the contrary. Binary formats are well-structured,
///	are simpler to define exhaustively, are aggregates of basic types which
///	are universal to all architectures (with the exception of two types of
///	byte ordering, which I hope to be an issue that will go away soon), and
///	are much more readable (through an appropriate formatting tool equipped
///	to read binary format specifications).
//
///		\defgroup BinaryStreamIterators Binary Stream Iterators
///		\ingroup BinaryStreams
///		\ingroup Iterators
///		Iterators for using STL algorithms with binary streams.
//
///	\defgroup TextStreams TextStreams
///	\ingroup Streams
///	Streams converting objects into streams of text.
//
///		\defgroup DeviceStreams Device Streams
///		\ingroup Streams
///		Standard cout, cerr, and cin implementations for reading
///		and writing text through standard file descriptors.
//
/// \defgroup Iterators Iterators
/// Generalizations of the pointer concept, allowing algorithms to treat
/// all containers in a unified fashion.
//
///	\defgroup IteratorAdaptors Iterator Adaptors
///	\ingroup Iterators
///	Iterators made out of other iterators.
//
/// \defgroup Algorithms Algorithms
/// STL algorithms are the heart of generic programming. The idea is to
/// separate algorithms from containers to take advantage of the fact that
/// there are fewer distinct algorithms than typed containers. This is
/// diametrically opposed to object oriented programming, where each object
/// must contain all functionality related to its internal data. You will
/// find, I think, that in practice, generic programming is not terribly
/// convenient because it prevents you from encapsulating all your data.
/// The best approach is to compromise and have raw data classes that will
/// be manipulated by algorithms and to treat the rest of the objects as
/// stateful data transformers.
//
///	\defgroup MutatingAlgorithms Mutating Algorithms
///	\ingroup Algorithms
///	Algorithms for modifying your data in some way.
//
///		\defgroup SortingAlgorithms Sorting Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for sorting containers.
//
///		\defgroup GeneratorAlgorithms Generator Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for generating data.
//
///		\defgroup NumericAlgorithms Numeric Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms generalizing mathematical operations.
//
///		\defgroup SetAlgorithms Set Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for working with sorted sets.
//
///		\defgroup HeapAlgorithms Heap Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for generating and manipulating heaps.
//
///		\defgroup SwapAlgorithms Swap Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for swapping elements.
//
///		\defgroup RawStorageAlgorithms Raw Storage Algorithms
///		\ingroup MutatingAlgorithms
///		Algorithms for manipulating unstructured memory.
//
///	\defgroup ConditionAlgorithms Condition Algorithms
///	\ingroup Algorithms
///	Algorithms for obtaining information about data.
//
///		\defgroup SearchingAlgorithms Searching Algorithms
///		\ingroup ConditionAlgorithms
///		Algorithms for searching through containers.
//
///	\defgroup PredicateAlgorithms Predicate Algorithms
///	\ingroup Algorithms
///	Algorithms that take a functor object. Avoid these if you can,
///	and carefully check the generated assembly if you can't. These
///	algorithms can and will generate prodigious amounts of bloat
///	if you are not very very careful about writing your functors.
//
/// \defgroup Functors Functors
/// Functors are inteded to be passed as arguments to \link PredicateAlgorithms
/// predicate algorithms\endlink. Ivory tower academics make much of this capability,
/// no doubt happy that C++ can now be made to look just like their precious lisp.
/// In practice, however, functors and predicate algorithms are mostly useless.
/// An iterative solution using \ref foreach is usually far simpler to write
/// and to maintain. Furthermore, functional programming in C++ often
/// generates much bloat and slowness, which is difficult to avoid with any
/// but the most primitive functors. Try them if you wish, now and then, but
/// compare with an iterative solution to see if the compiler really can see
/// through all your functional trickery.
//
///	\defgroup FunctorObjects Functor Objects
///	\ingroup Functors
///	Objects that wrap other functors to provide new functionality.
//
///	\defgroup FunctorAccessors Functor Object Accessors
///	\ingroup Functors
///	Because C++ is so very unsuited to functional programming, trying
///	to do so may require a lot of typing. These accessor functions
///	are somewhat helpful in making functional constructs more readable.
