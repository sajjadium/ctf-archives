// This file is part of the uSTL library, an STL implementation.
//
// Copyright (c) 2005 by Mike Sharov <msharov@users.sourceforge.net>
// This file is free software, distributed under the MIT License.

#pragma once
#include "memblock.h"
#include "utf8.h"
#include <stdarg.h>

namespace ustl {

/// \class string ustring.h ustl.h
/// \ingroup Sequences
///
/// \brief STL basic_string&lt;char&gt; equivalent.
///
/// An STL container for text string manipulation.
/// Differences from C++ standard:
///	- string is a class, not a template. Wide characters are assumed to be
///		encoded with utf8 at all times except when rendering or editing,
///		where you would use a utf8 iterator.
/// 	- format member function - you can, of course use an \ref ostringstream,
///		which also have format functions, but most of the time this way
///		is more convenient. Because uSTL does not implement locales,
///		format is the only way to create localized strings.
/// 	- const char* cast operator. It is much clearer to use this than having
/// 		to type .c_str() every time.
/// 	- length returns the number of _characters_, not bytes.
///		This function is O(N), so use wisely.
///
/// An additional note is in order regarding the use of indexes. All indexes
/// passed in as arguments or returned by find are byte offsets, not character
/// offsets. Likewise, sizes are specified in bytes, not characters. The
/// rationale is that there is no way for you to know what is in the string.
/// There is no way for you to know how many characters are needed to express
/// one thing or another. The only thing you can do to a localized string is
/// search for delimiters and modify text between them as opaque blocks. If you
/// do anything else, you are hardcoding yourself into a locale! So stop it!
///
class string : public memblock {
public:
    typedef char		value_type;
    typedef unsigned char	uvalue_type;
    typedef value_type*		pointer;
    typedef const value_type*	const_pointer;
    typedef wchar_t		wvalue_type;
    typedef wvalue_type*	wpointer;
    typedef const wvalue_type*	const_wpointer;
    typedef pointer		iterator;
    typedef const_pointer	const_iterator;
    typedef value_type&		reference;
    typedef value_type		const_reference;
    typedef ::ustl::reverse_iterator<iterator>		reverse_iterator;
    typedef ::ustl::reverse_iterator<const_iterator>	const_reverse_iterator;
    typedef utf8in_iterator<const_iterator>		utf8_iterator;
    typedef size_type		pos_type;
    static constexpr const pos_type npos = INT_MAX;	///< Value that means the end of string.
public:
    inline			string (void) noexcept		: memblock () { relink ("",0); }
				string (const string& s);
    inline			string (const string& s, pos_type o, size_type n = npos);
    inline explicit		string (const cmemlink& l);
				string (const_pointer s) noexcept;
    inline			string (const_pointer s, size_type len);
    inline			string (const_pointer s1, const_pointer s2);
				string (size_type n, value_type c);
    inline			~string (void) noexcept		{ }
    inline pointer		data (void)			{ return string::pointer (memblock::data()); }
    inline const_pointer	data (void) const		{ return string::const_pointer (memblock::data()); }
    inline const_pointer	c_str (void) const		{ return string::const_pointer (memblock::cdata()); }
    inline size_type		max_size (void) const		{ size_type s (memblock::max_size()); return s - !!s; }
    inline size_type		capacity (void) const		{ size_type c (memblock::capacity()); return c - !!c; }
    void			resize (size_type n);
    inline void			resize (size_type n, value_type c);
    inline void			clear (void)			{ resize (0); }
    inline iterator		begin (void)			{ return iterator (memblock::begin()); }
    inline const_iterator	begin (void) const		{ return const_iterator (memblock::begin()); }
    inline const_iterator	cbegin (void) const		{ return begin(); }
    inline iterator		end (void)			{ return iterator (memblock::end()); }
    inline const_iterator	end (void) const		{ return const_iterator (memblock::end()); }
    inline const_iterator	cend (void) const		{ return end(); }
    inline reverse_iterator	rbegin (void)			{ return reverse_iterator (end()); }
  inline const_reverse_iterator	rbegin (void) const		{ return const_reverse_iterator (end()); }
  inline const_reverse_iterator	crbegin (void) const		{ return rbegin(); }
    inline reverse_iterator	rend (void)			{ return reverse_iterator (begin()); }
  inline const_reverse_iterator	rend (void) const		{ return const_reverse_iterator (begin()); }
  inline const_reverse_iterator	crend (void) const		{ return rend(); }
    inline utf8_iterator	utf8_begin (void) const		{ return utf8_iterator (begin()); }
    inline utf8_iterator	utf8_end (void) const		{ return utf8_iterator (end()); }
    inline const_reference	at (pos_type pos) const		{ assert (pos <= size() && begin()); return begin()[pos]; }
    inline reference		at (pos_type pos)		{ assert (pos <= size() && begin()); return begin()[pos]; }
    inline const_iterator	iat (pos_type pos) const	{ return begin() + (__builtin_constant_p(pos) && pos >= npos ? size() : min(size_type(pos),size())); }
    inline iterator		iat (pos_type pos)		{ return const_cast<iterator>(const_cast<const string*>(this)->iat(pos)); }
    const_iterator		wiat (pos_type i) const noexcept;
    inline iterator		wiat (pos_type i)		{ return const_cast<iterator>(const_cast<const string*>(this)->wiat(i)); }
    inline const_reference	front (void) const		{ return at(0); }
    inline reference		front (void)			{ return at(0); }
    inline const_reference	back (void) const		{ return at(size()-1); }
    inline reference		back (void)			{ return at(size()-1); }
    inline size_type		length (void) const		{ return distance (utf8_begin(), utf8_end()); }
    inline string&		append (const_iterator i1, const_iterator i2)	{ return append (i1, distance (i1, i2)); }
    string&	   		append (const_pointer s, size_type len);
    string&	   		append (const_pointer s);
    string&			append (size_type n, value_type c);
    inline string&		append (size_type n, wvalue_type c)		{ insert (size(), n, c); return *this; }
    inline string&		append (const_wpointer s1, const_wpointer s2)	{ insert (size(), s1, s2); return *this; }
    inline string&		append (const_wpointer s)			{ const_wpointer se (s); for (;se&&*se;++se) {} return append (s, se); }
    inline string&		append (const string& s)			{ return append (s.begin(), s.end()); }
    inline string&		append (const string& s,pos_type o,size_type n)	{ return append (s.iat(o), s.iat(o+n)); }
    inline void			push_back (value_type c)			{ resize(size()+1); end()[-1] = c; }
    inline void			push_back (wvalue_type c)			{ append (1, c); }
    inline void			pop_back (void)					{ resize (size()-1); }
    inline string&		assign (const_iterator i1, const_iterator i2)	{ return assign (i1, distance (i1, i2)); }
    string&	    		assign (const_pointer s, size_type len);
    string&	    		assign (const_pointer s);
    inline string&		assign (const_wpointer s1, const_wpointer s2)	{ clear(); return append (s1, s2); }
    inline string&		assign (const_wpointer s1)			{ clear(); return append (s1); }
    inline string&		assign (const string& s)			{ return assign (s.begin(), s.end()); }
    inline string&		assign (const string& s, pos_type o, size_type n)	{ return assign (s.iat(o), s.iat(o+n)); }
    inline string&		assign (size_type n, value_type c)		{ clear(); return append (n, c); }
    inline string&		assign (size_type n, wvalue_type c)		{ clear(); return append (n, c); }
    size_type			copy (pointer p, size_type n, pos_type pos = 0) const noexcept;
    inline size_type		copyto (pointer p, size_type n, pos_type pos = 0) const noexcept { size_type bc = copy(p,n-1,pos); p[bc]=0; return bc; }
    inline int			compare (const string& s) const		{ return compare (begin(), end(), s.begin(), s.end()); }
    inline int			compare (pos_type start, size_type len, const string& s) const	{ return compare (iat(start), iat(start+len), s.begin(), s.end()); }
    inline int			compare (pos_type s1, size_type l1, const string& s, pos_type s2, size_type l2) const	{ return compare (iat(s1), iat(s1+l1), s.iat(s2), s.iat(s2+l2)); }
    inline int			compare (const_pointer s) const		{ return compare (begin(), end(), s, s + strlen(s)); }
    inline int			compare (pos_type s1, size_type l1, const_pointer s, size_type l2) const { return compare (iat(s1), iat(s1+l1), s, s+l2); }
    inline int			compare (pos_type s1, size_type l1, const_pointer s) const { return compare (s1, l1, s, strlen(s)); }
    static int			compare (const_iterator first1, const_iterator last1, const_iterator first2, const_iterator last2) noexcept;
    inline			operator const value_type* (void) const;
    inline			operator value_type* (void);
    inline const string&	operator= (const string& s)		{ return assign (s.begin(), s.end()); }
    inline const string&	operator= (const_reference c)		{ return assign (&c, 1); }
    inline const string&	operator= (const_pointer s)		{ return assign (s); }
    inline const string&	operator= (const_wpointer s)		{ return assign (s); }
    inline const string&	operator+= (const string& s)		{ return append (s.begin(), s.size()); }
    inline const string&	operator+= (value_type c)		{ push_back(c); return *this; }
    inline const string&	operator+= (const_pointer s)		{ return append (s); }
    inline const string&	operator+= (wvalue_type c)		{ return append (1, c); }
    inline const string&	operator+= (uvalue_type c)		{ return operator+= (value_type(c)); }
    inline const string&	operator+= (const_wpointer s)		{ return append (s); }
    inline string		operator+ (const string& s) const;
    inline bool			operator== (const string& s) const	{ return memblock::operator== (s); }
    bool			operator== (const_pointer s) const noexcept;
    inline bool			operator== (value_type c) const		{ return size() == 1 && c == at(0); }
    inline bool			operator== (uvalue_type c) const	{ return operator== (value_type(c)); }
    inline bool			operator!= (const string& s) const	{ return !operator== (s); }
    inline bool			operator!= (const_pointer s) const	{ return !operator== (s); }
    inline bool			operator!= (value_type c) const		{ return !operator== (c); }
    inline bool			operator!= (uvalue_type c) const	{ return !operator== (c); }
    inline bool			operator< (const string& s) const	{ return 0 > compare (s); }
    inline bool			operator< (const_pointer s) const	{ return 0 > compare (s); }
    inline bool			operator< (value_type c) const		{ return 0 > compare (begin(), end(), &c, &c + 1); }
    inline bool			operator< (uvalue_type c) const		{ return operator< (value_type(c)); }
    inline bool			operator> (const_pointer s) const	{ return 0 < compare (s); }
    inline string&		insert (pos_type ip, size_type n, value_type c)				{ insert (iat(ip), n, c); return *this; }
    inline string&		insert (pos_type ip, const_pointer s)					{ insert (iat(ip), s, s + strlen(s)); return *this; }
    inline string&		insert (pos_type ip, const_pointer s, size_type nlen)			{ insert (iat(ip), s, s + nlen); return *this; }
    inline string&		insert (pos_type ip, const string& s)					{ insert (iat(ip), s.c_str(), s.size()); return *this; }
    inline string&		insert (pos_type ip, const string& s, size_type sp, size_type slen)	{ insert (iat(ip), s.iat(sp), s.iat(sp + slen)); return *this; }
    string&			insert (pos_type ip, size_type n, wvalue_type c);
    string&			insert (pos_type ip, const_wpointer first, const_wpointer last, size_type n = 1);
    inline string&		insert (int ip, size_type n, value_type c)				{ insert (pos_type(ip), n, c); return *this; }
    inline string&		insert (int ip, const_pointer s, size_type nlen)			{ insert (pos_type(ip), s, nlen); return *this; }
    iterator			insert (const_iterator start, size_type n, value_type c);
    inline iterator		insert (const_iterator start, value_type c)				{ return insert (start, 1u, c); }
    iterator			insert (const_iterator start, const_pointer s, size_type n);
    iterator			insert (const_iterator start, const_pointer first, const_iterator last, size_type n = 1);
    iterator			erase (const_iterator epo, size_type n = 1);
    string&			erase (pos_type epo = 0, size_type n = npos);
    inline string&		erase (int epo, size_type n = npos)			{ return erase (pos_type(epo), n); }
    inline iterator		erase (const_iterator first, const_iterator last)	{ return erase (first, size_type(distance(first,last))); }
    inline iterator		eraser (pos_type first, pos_type last)			{ return erase (iat(first), iat(last)); }
    string&			replace (const_iterator first, const_iterator last, const_pointer i1, const_pointer i2, size_type n);
    template <typename InputIt>
    string&			replace (const_iterator first, const_iterator last, InputIt first2, InputIt last2)	{ return replace (first, last, first2, last2, 1); }
    inline string&		replace (const_iterator first, const_iterator last, const string& s)			{ return replace (first, last, s.begin(), s.end()); }
    string&			replace (const_iterator first, const_iterator last, const_pointer s);
    inline string&		replace (const_iterator first, const_iterator last, const_pointer s, size_type slen)	{ return replace (first, last, s, s + slen); }
    inline string&		replace (const_iterator first, const_iterator last, size_type n, value_type c)		{ return replace (first, last, &c, &c + 1, n); }
    inline string&		replace (pos_type rp, size_type n, const string& s)					{ return replace (iat(rp), iat(rp + n), s); }
    inline string&		replace (pos_type rp, size_type n, const string& s, uoff_t sp, size_type slen)		{ return replace (iat(rp), iat(rp + n), s.iat(sp), s.iat(sp + slen)); }
    inline string&		replace (pos_type rp, size_type n, const_pointer s, size_type slen)			{ return replace (iat(rp), iat(rp + n), s, s + slen); }
    inline string&		replace (pos_type rp, size_type n, const_pointer s)					{ return replace (iat(rp), iat(rp + n), string(s)); }
    inline string&		replace (pos_type rp, size_type n, size_type count, value_type c)			{ return replace (iat(rp), iat(rp + n), count, c); }
    inline string		substr (pos_type o = 0, size_type n = npos) const	{ return string (*this, o, n); }
    inline void			swap (string& v)					{ memblock::swap (v); }
    pos_type			find (value_type c, pos_type pos = 0) const noexcept;
    pos_type			find (const string& s, pos_type pos = 0) const noexcept;
    inline pos_type		find (uvalue_type c, pos_type pos = 0) const noexcept		{ return find (value_type(c), pos); }
    inline pos_type		find (const_pointer p, pos_type pos, size_type count) const	{ string sp; sp.link (p,count); return find (sp, pos); }
    pos_type			rfind (value_type c, pos_type pos = npos) const noexcept;
    pos_type			rfind (const string& s, pos_type pos = npos) const noexcept;
    inline pos_type		rfind (uvalue_type c, pos_type pos = npos) const noexcept	{ return rfind (value_type(c), pos); }
    inline pos_type		rfind (const_pointer p, pos_type pos, size_type count) const	{ string sp; sp.link (p,count); return rfind (sp, pos); }
    pos_type			find_first_of (const string& s, pos_type pos = 0) const noexcept;
    inline pos_type		find_first_of (value_type c, pos_type pos = 0) const				{ string sp (1, c); return find_first_of(sp,pos); }
    inline pos_type		find_first_of (uvalue_type c, pos_type pos = 0) const				{ return find_first_of (value_type(c), pos); }
    inline pos_type		find_first_of (const_pointer p, pos_type pos, size_type count) const		{ string sp; sp.link (p,count); return find_first_of (sp, pos); }
    pos_type			find_first_not_of (const string& s, pos_type pos = 0) const noexcept;
    inline pos_type		find_first_not_of (value_type c, pos_type pos = 0) const			{ string sp (1, c); return find_first_not_of(sp,pos); }
    inline pos_type		find_first_not_of (uvalue_type c, pos_type pos = 0) const			{ return find_first_not_of (value_type(c), pos); }
    inline pos_type		find_first_not_of (const_pointer p, pos_type pos, size_type count) const	{ string sp; sp.link (p,count); return find_first_not_of (sp, pos); }
    pos_type			find_last_of (const string& s, pos_type pos = npos) const noexcept;
    inline pos_type		find_last_of (value_type c, pos_type pos = npos) const				{ string sp (1, c); return find_last_of(sp,pos); }
    inline pos_type		find_last_of (uvalue_type c, pos_type pos = npos) const				{ return find_last_of (value_type(c), pos); }
    inline pos_type		find_last_of (const_pointer p, pos_type pos, size_type count) const		{ string sp; sp.link (p,count); return find_last_of (sp, pos); }
    pos_type			find_last_not_of (const string& s, pos_type pos = npos) const noexcept;
    inline pos_type		find_last_not_of (value_type c, pos_type pos = npos) const			{ string sp (1, c); return find_last_not_of(sp,pos); }
    inline pos_type		find_last_not_of (uvalue_type c, pos_type pos = npos) const			{ return find_last_not_of (value_type(c), pos); }
    inline pos_type		find_last_not_of (const_pointer p, pos_type pos, size_type count) const		{ string sp; sp.link (p,count); return find_last_not_of (sp, pos); }
    int				vformat (const char* fmt, va_list args);
    int				format (const char* fmt, ...) __attribute__((__format__(__printf__, 2, 3)));
    void			read (istream&);
    void			write (ostream& os) const;
    size_t			stream_size (void) const noexcept;
    static hashvalue_t		hash (const char* f1, const char* l1) noexcept;
#if HAVE_CPP11
    using initlist_t = std::initializer_list<value_type>;
    inline			string (string&& v)		: memblock (move(v)) {}
    inline			string (initlist_t v)		: memblock() { assign (v.begin(), v.size()); }
    inline string&		assign (string&& v)		{ swap (v); return *this; }
    inline string&		assign (initlist_t v)		{ return assign (v.begin(), v.size()); }
    inline string&		append (initlist_t v)		{ return append (v.begin(), v.size()); }
    inline string&		operator+= (initlist_t v)	{ return append (v.begin(), v.size()); }
    inline string&		operator= (string&& v)		{ return assign (move(v)); }
    inline string&		operator= (initlist_t v)	{ return assign (v.begin(), v.size()); }
    inline iterator		insert (const_iterator ip, initlist_t v)	{ return insert (ip, v.begin(), v.end()); }
    inline string&		replace (const_iterator first, const_iterator last, initlist_t v)	{ return replace (first, last, v.begin(), v.end()); }
#endif
private:
    virtual size_type		minimumFreeCapacity (void) const noexcept final override __attribute__((const));
};

//----------------------------------------------------------------------

/// Assigns itself the value of string \p s
inline string::string (const cmemlink& s)
: memblock ()
{
    assign (const_iterator (s.begin()), s.size());
}

/// Assigns itself a [o,o+n) substring of \p s.
inline string::string (const string& s, pos_type o, size_type n)
: memblock()
{
    assign (s, o, n);
}

/// Copies the value of \p s of length \p len into itself.
inline string::string (const_pointer s, size_type len)
: memblock ()
{
    assign (s, len);
}

/// Copies into itself the string data between \p s1 and \p s2
inline string::string (const_pointer s1, const_pointer s2)
: memblock ()
{
    assert (s1 <= s2 && "Negative ranges result in memory allocation errors.");
    assign (s1, s2);
}

/// Returns the pointer to the first character.
inline string::operator const string::value_type* (void) const
{
    assert ((!end() || !*end()) && "This string is linked to data that is not 0-terminated. This may cause serious security problems. Please assign the data instead of linking.");
    return begin();
}

/// Returns the pointer to the first character.
inline string::operator string::value_type* (void)
{
    assert ((end() && !*end()) && "This string is linked to data that is not 0-terminated. This may cause serious security problems. Please assign the data instead of linking.");
    return begin();
}

/// Concatenates itself with \p s
inline string string::operator+ (const string& s) const
{
    string result (*this);
    result += s;
    return result;
}

/// Resize to \p n and fill new entries with \p c
inline void string::resize (size_type n, value_type c)
{
    const size_type oldn = size();
    resize (n);
    fill_n (iat(oldn), max(ssize_t(n-oldn),0), c);
}

//----------------------------------------------------------------------
// Operators needed to avoid comparing pointer to pointer

#define PTR_STRING_CMP(op, impl)	\
inline bool op (const char* s1, const string& s2) { return impl; }
PTR_STRING_CMP (operator==, (s2 == s1))
PTR_STRING_CMP (operator!=, (s2 != s1))
PTR_STRING_CMP (operator<,  (s2 >  s1))
PTR_STRING_CMP (operator<=, (s2 >= s1))
PTR_STRING_CMP (operator>,  (s2 <  s1))
PTR_STRING_CMP (operator>=, (s2 <= s1))
#undef PTR_STRING_CMP

inline string operator+ (const char* cs, const string& ss) { string r; r.reserve (strlen(cs)+ss.size()); r += cs; r += ss; return r; }

//----------------------------------------------------------------------

inline hashvalue_t hash_value (const char* first, const char* last)
{ return string::hash (first, last); }
inline hashvalue_t hash_value (const char* v)
{ return hash_value (v, v + strlen(v)); }

//----------------------------------------------------------------------
// String-number conversions

#define STRING_TO_INT_CONVERTER(name,type,func)	\
inline type name (const string& str, size_t* idx = nullptr, int base = 10) \
{					\
    const char* sp = str.c_str();	\
    char* endp = nullptr;		\
    type r = func (sp, idx ? &endp : nullptr, base);\
    if (idx)				\
	*idx = endp - sp;		\
    return r;				\
}
/*STRING_TO_INT_CONVERTER(stoi,int,strtol)
STRING_TO_INT_CONVERTER(stol,long,strtol)
STRING_TO_INT_CONVERTER(stoul,unsigned long,strtoul)
#if HAVE_LONG_LONG
STRING_TO_INT_CONVERTER(stoll,long long,strtoll)
STRING_TO_INT_CONVERTER(stoull,unsigned long long,strtoull)
#endif*/
#undef STRING_TO_INT_CONVERTER

#define STRING_TO_FLOAT_CONVERTER(name,type,func) \
inline type name (const string& str, size_t* idx = nullptr) \
{					\
    const char* sp = str.c_str();	\
    char* endp = nullptr;		\
    type r = func (sp, idx ? &endp : nullptr);\
    if (idx)				\
	*idx = endp - sp;		\
    return r;				\
}
/*STRING_TO_FLOAT_CONVERTER(stof,float,strtof)
STRING_TO_FLOAT_CONVERTER(stod,double,strtod)
STRING_TO_FLOAT_CONVERTER(stold,long double,strtold)*/
#undef STRING_TO_FLOAT_CONVERTER

#define NUMBER_TO_STRING_CONVERTER(type,fmts)\
    inline string to_string (type v) { string r; r.format(fmts,v); return r; }
NUMBER_TO_STRING_CONVERTER(int,"%d")
NUMBER_TO_STRING_CONVERTER(long,"%ld")
NUMBER_TO_STRING_CONVERTER(unsigned long,"%lu")
#if HAVE_LONG_LONG
NUMBER_TO_STRING_CONVERTER(long long,"%lld")
NUMBER_TO_STRING_CONVERTER(unsigned long long,"%llu")
#endif
/*NUMBER_TO_STRING_CONVERTER(float,"%f")
NUMBER_TO_STRING_CONVERTER(double,"%lf")
NUMBER_TO_STRING_CONVERTER(long double,"%Lf")*/
#undef NUMBER_TO_STRING_CONVERTER

} // namespace ustl
