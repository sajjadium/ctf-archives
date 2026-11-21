// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#include "ustring.h"
#include "mistream.h"
#include "mostream.h"
#include "ualgo.h"
#include "ustringformat.h" // for vsnprintf (in string::format)

extern char data_end_address;

namespace ustl {

//----------------------------------------------------------------------

constexpr const string::pos_type string::npos;

//----------------------------------------------------------------------

/// Assigns itself the value of string \p s
string::string (const string& s)
: memblock ((s.size()+1) & (s.is_linked()-1))	// +1 because base ctor can't call virtuals of this class
{
//    if (s.is_linked())
//  relink (s.c_str(), s.size());
//    else {
  copy_n (s.begin(), size(), begin());
  relink (begin(), size()-1); // --m_Size
//    }
}

/// Links to \p s
string::string (const_pointer s) noexcept
: memblock (strlen(s)+1)
{
    if (!s) s = "";
    copy_n (s, strlen(s)+1, begin());
    relink (begin(), size()-1); // --m_Size
}

/// Creates a string of length \p n filled with character \p c.
string::string (size_type n, value_type c)
: memblock (n+1)	// +1 because base ctor can't call virtuals of this class
{
    relink (begin(), size()-1);	// --m_Size
    fill_n (begin(), n, c);
    at(n) = 0;
}

/// Resize the string to \p n characters. New space contents is undefined.
void string::resize (size_type n)
{
    if (!(n | memblock::capacity()))
	return relink ("",0);
    memblock::resize (n);
    at(n) = 0;
}

/// Assigns itself the value of string \p s
string& string::assign (const_pointer s)
{
    if (!s) s = "";
    assign (s, strlen (s));
    return *this;
}

/// Assigns itself the value of string \p s of length \p len.
string& string::assign (const_pointer s, size_type len)
{
    resize (len);
    copy_n (s, len, begin());
    return *this;
}

/// Appends to itself the value of string \p s of length \p len.
string& string::append (const_pointer s)
{
    if (!s) s = "";
    append (s, strlen (s));
    return *this;
}

/// Appends to itself the value of string \p s of length \p len.
string& string::append (const_pointer s, size_type len)
{
    resize (size() + len);
    copy_n (s, len, end() - len);
    return *this;
}

/// Appends to itself \p n characters of value \p c.
string& string::append (size_type n, value_type c)
{
    resize (size() + n);
    fill_n (end() - n, n, c);
    return *this;
}

/// Copies [start,start+n) into [p,n). The result is not null terminated.
string::size_type string::copy (pointer p, size_type n, pos_type start) const noexcept
{
    assert (p && n && start <= size());
    const size_type btc = min(n, size()-start);
    copy_n (iat(start), btc, p);
    return btc;
}

/// Returns comparison value regarding string \p s.
/// The return value is:
/// \li 1 if this string is greater (by value, not length) than string \p s
/// \li 0 if this string is equal to string \p s
/// \li -1 if this string is less than string \p s
///
int string::compare (const_iterator first1, const_iterator last1, const_iterator first2, const_iterator last2) noexcept // static
{
    assert (first1 <= last1 && (first2 <= last2 || !last2) && "Negative ranges result in memory allocation errors.");
    const size_type len1 = distance (first1, last1), len2 = distance (first2, last2);
    const int rvbylen = sign (int(len1 - len2));
    int rv = memcmp (first1, first2, min (len1, len2));
    return rv ? rv : rvbylen;
}

/// Returns true if this string is equal to string \p s.
bool string::operator== (const_pointer s) const noexcept
{
    if (!s) s = "";
    return size() == strlen(s) && 0 == memcmp (c_str(), s, size());
}

/// Returns the beginning of character \p i.
string::const_iterator string::wiat (pos_type i) const noexcept
{
    utf8in_iterator<string::const_iterator> cfinder (begin());
    cfinder += i;
    return cfinder.base();
}

/// Inserts wide character \p c at \p ipo \p n times as a UTF-8 string.
///
/// \p ipo is a byte position, not a character position, and is intended
/// to be obtained from one of the find functions. Generally you are not
/// able to know the character position in a localized string; different
/// languages will have different character counts, so use find instead.
///
string& string::insert (pos_type ipo, size_type n, wvalue_type c)
{
    iterator ip (iat(ipo));
    ip = iterator (memblock::insert (memblock::iterator(ip), n * Utf8Bytes(c)));
    fill_n (utf8out (ip), n, c);
    *end() = 0;
    return *this;
}

/// Inserts sequence of wide characters at \p ipo (byte position from a find call)
string& string::insert (pos_type ipo, const wvalue_type* first, const wvalue_type* last, const size_type n)
{
    iterator ip (iat(ipo));
    size_type nti = distance (first, last), bti = 0;
    for (size_type i = 0; i < nti; ++ i)
	bti += Utf8Bytes(first[i]);
    ip = iterator (memblock::insert (memblock::iterator(ip), n * bti));
    utf8out_iterator<string::iterator> uout (utf8out (ip));
    for (size_type j = 0; j < n; ++ j)
	for (size_type k = 0; k < nti; ++ k, ++ uout)
	    *uout = first[k];
    *end() = 0;
    return *this;
}

/// Inserts character \p c into this string at \p start.
string::iterator string::insert (const_iterator start, size_type n, value_type c)
{
    memblock::iterator ip = memblock::insert (memblock::const_iterator(start), n);
    fill_n (ip, n, c);
    *end() = 0;
    return iterator(ip);
}

/// Inserts \p count instances of string \p s at offset \p start.
string::iterator string::insert (const_iterator start, const_pointer s, size_type n)
{
    if (!s) s = "";
    return insert (start, s, s + strlen(s), n);
}

/// Inserts [first,last] \p n times.
string::iterator string::insert (const_iterator start, const_pointer first, const_pointer last, size_type n)
{
    assert (first <= last);
    assert (begin() <= start && end() >= start);
    assert ((first < begin() || first >= end() || size() + abs_distance(first,last) < capacity()) && "Insertion of self with autoresize is not supported");
    memblock::iterator ip = iterator (memblock::insert (memblock::const_iterator(start), distance(first, last) * n));
    fill (ip, first, distance(first, last), n);
    *end() = 0;
    return iterator(ip);
}

/// Erases \p size bytes at \p ep.
string::iterator string::erase (const_iterator ep, size_type n)
{
    string::iterator rv = memblock::erase (memblock::const_iterator(ep), n);
    *end() = 0;
    return rv;
}

/// Erases \p n bytes at byte offset \p epo.
string& string::erase (pos_type epo, size_type n)
{
    erase (iat(epo), min (n, size()-epo));
    return *this;
}

/// Replaces range [\p start, \p start + \p len] with string \p s.
string& string::replace (const_iterator first, const_iterator last, const_pointer s)
{
    if (!s) s = "";
    replace (first, last, s, s + strlen(s));
    return *this;
}

/// Replaces range [\p start, \p start + \p len] with \p count instances of string \p s.
string& string::replace (const_iterator first, const_iterator last, const_pointer i1, const_pointer i2, size_type n)
{
    assert (first <= last);
    assert (n || distance(first, last));
    assert (first >= begin() && first <= end() && last >= first && last <= end());
    assert ((i1 < begin() || i1 >= end() || abs_distance(i1,i2) * n + size() < capacity()) && "Replacement by self can not autoresize");
    const size_type bte = distance(first, last), bti = distance(i1, i2) * n;
    memblock::const_iterator rp = static_cast<memblock::const_iterator>(first);
    if (bti < bte)
	rp = memblock::erase (rp, bte - bti);
    else if (bte < bti)
	rp = memblock::insert (rp, bti - bte);
    fill (rp, i1, distance(i1, i2), n);
    *end() = 0;
    return *this;
}

/// Returns the offset of the first occurence of \p c after \p pos.
string::pos_type string::find (value_type c, pos_type pos) const noexcept
{
    const_iterator found = ::ustl::find (iat(pos), end(), c);
    return found < end() ? pos_type (distance(begin(),found)) : npos;
}

/// Returns the offset of the first occurence of substring \p s of length \p n after \p pos.
string::pos_type string::find (const string& s, pos_type pos) const noexcept
{
    if (s.empty() || s.size() > size() - pos)
	return npos;
    pos_type endi = s.size() - 1;
    value_type endchar = s[endi];
    pos_type lastPos = endi;
    while (lastPos-- && s[lastPos] != endchar) ;
    const size_type skip = endi - lastPos;
    const_iterator i = iat(pos) + endi;
    for (; i < end() && (i = ::ustl::find (i, end(), endchar)) < end(); i += skip)
	if (memcmp (i - endi, s.c_str(), s.size()) == 0)
	    return distance (begin(), i) - endi;
    return npos;
}

/// Returns the offset of the last occurence of character \p c before \p pos.
string::pos_type string::rfind (value_type c, pos_type pos) const noexcept
{
    for (int i = min(pos,pos_type(size()-1)); i >= 0; --i)
	if (at(i) == c)
	    return i;
    return npos;
}

/// Returns the offset of the last occurence of substring \p s of size \p n before \p pos.
string::pos_type string::rfind (const string& s, pos_type pos) const noexcept
{
    const_iterator d = iat(pos) - 1;
    const_iterator sp = begin() + s.size() - 1;
    const_iterator m = s.end() - 1;
    for (long int i = 0; d > sp && size_type(i) < s.size(); -- d)
	for (i = 0; size_type(i) < s.size(); ++ i)
	    if (m[-i] != d[-i])
		break;
    return d > sp ? pos_type (distance (begin(), d + 2 - s.size())) : npos;
}

/// Returns the offset of the first occurence of one of characters in \p s of size \p n after \p pos.
string::pos_type string::find_first_of (const string& s, pos_type pos) const noexcept
{
    for (size_type i = min(size_type(pos),size()); i < size(); ++ i)
	if (s.find (at(i)) != npos)
	    return i;
    return npos;
}

/// Returns the offset of the first occurence of one of characters not in \p s of size \p n after \p pos.
string::pos_type string::find_first_not_of (const string& s, pos_type pos) const noexcept
{
    for (size_type i = min(size_type(pos),size()); i < size(); ++ i)
	if (s.find (at(i)) == npos)
	    return i;
    return npos;
}

/// Returns the offset of the last occurence of one of characters in \p s of size \p n before \p pos.
string::pos_type string::find_last_of (const string& s, pos_type pos) const noexcept
{
    for (int i = min(size_type(pos),size()-1); i >= 0; -- i)
	if (s.find (at(i)) != npos)
	    return i;
    return npos;
}

/// Returns the offset of the last occurence of one of characters not in \p s of size \p n before \p pos.
string::pos_type string::find_last_not_of (const string& s, pos_type pos) const noexcept
{
    for (int i = min(pos,pos_type(size()-1)); i >= 0; -- i)
	if (s.find (at(i)) == npos)
	    return i;
    return npos;
}

/// Equivalent to a vsprintf on the string.
int string::vformat (const char* fmt, va_list args)
{
#if HAVE_VA_COPY
    va_list args2;
#else
    #define args2 args
    #undef __va_copy
    #define __va_copy(x,y)
#endif
    int rv = size(), wcap;
    do {
	__va_copy (args2, args);
	rv = vsnprintf (data(), wcap = memblock::capacity(), fmt, args2);
	resize (rv);
    } while (rv >= wcap);
    return rv;
}

/// Equivalent to a sprintf on the string.
int string::format (const char* fmt, ...)
{
    va_list args;
    va_start (args, fmt);
    const int rv = vformat (fmt, args);
    va_end (args);
    return rv;
}

/// Returns the number of bytes required to write this object to a stream.
size_t string::stream_size (void) const noexcept
{
    return Utf8Bytes(size()) + size();
}

/// Reads the object from stream \p os
/*void string::read (istream& is)
{
    char szbuf [8];
    is >> szbuf[0];
    size_t szsz (Utf8SequenceBytes (szbuf[0]) - 1), n = 0;
    if (!is.verify_remaining ("read", "ustl::string", szsz)) return;
    is.read (szbuf + 1, szsz);
    n = *utf8in(szbuf);
    if (!is.verify_remaining ("read", "ustl::string", n)) return;
    resize (n);
    is.read (data(), size());
}

/// Writes the object to stream \p os
void string::write (ostream& os) const
{
    const written_size_type sz (size());
    assert (sz == size() && "No support for writing strings larger than 4G");

    char szbuf [8];
    utf8out_iterator<char*> szout (szbuf);
    *szout = sz;
    size_t szsz = distance (szbuf, szout.base());

    if (!os.verify_remaining ("write", "ustl::string", szsz + sz)) return;
    os.write (szbuf, szsz);
    os.write (cdata(), sz);
}*/

/// Returns a hash value for [first, last)
hashvalue_t string::hash (const char* first, const char* last) noexcept // static
{
    hashvalue_t h = 0;
    // This has the bits flowing into each other from both sides of the number
    for (; first < last; ++ first)
	h = *first + ((h << 7) | (h >> (BitsInType(hashvalue_t) - 7)));
    return h;
}

string::size_type string::minimumFreeCapacity (void) const noexcept { return 1; }

} // namespace ustl
