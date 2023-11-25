#pragma once

#include "sostream.h"
#include "kprintf.h"
#include "uios.h"

namespace ustl {


/// \class coutclass sostream.h ustl.h
/// \ingroup TextStreams
///
/// \brief This stream writes textual data into a memory block.
///
class coutclass : public ostream {
  public:
    static void init();
    coutclass();
    coutclass(void* p, size_t n);
    coutclass(void(*m_kprintf)(const char*, ...));
    coutclass(void* p, size_t n, void(*m_kprintf)(const char*, ...));
    void      iwrite (uint8_t v);
    void      iwrite (wchar_t v);
    inline void     iwrite (int v)      { iformat (v); }
    inline void     iwrite (unsigned int v)   { iformat (v); }
    inline void     iwrite (long int v)   { iformat (v); }
    inline void     iwrite (unsigned long int v)  { iformat (v); }
    void      iwrite (bool v);
    inline void     iwrite (const char* s)    { write (s, strlen(s)); }
    inline void     iwrite (const string& v)  { write (v.begin(), v.size()); }
    inline void     iwrite (fmtflags f);
#if HAVE_LONG_LONG
    inline void     iwrite (long long v)    { iformat (v); }
    inline void     iwrite (unsigned long long v) { iformat (v); }
#endif
    inline size_type    max_size (void) const   { return 0; }
    inline coutclass& put (char c)      { iwrite (uint8_t(c)); return (*this); }
    int       format (const char* fmt, ...) __attribute__((__format__(__printf__, 2, 3)));
    inline void     set_base (uint16_t b)   { m_Base = b; }
    inline void     set_width (uint16_t w)    { m_Width = w; }
    inline void     set_decimal_separator (char)  { }
    inline void     set_thousand_separator (char) { }
    inline void     set_precision (uint16_t v)  { m_Precision = v; }
    void      link (void* p, size_type n);
    inline void     link (memlink& l)   { link (l.data(), l.writable_size()); }
    void      str (const string& s);
    coutclass&    write (const void* buffer, size_type size);
    inline coutclass& write (const cmemlink& buf) { return (write (buf.begin(), buf.size())); }
    inline coutclass& seekp (off_t p __attribute__((unused)), __attribute__((unused)) seekdir d =beg) { return (*this); }
    coutclass&    flush (void)      { return (*this); }
    virtual size_type   overflow (size_type n = 1);
protected:
    inline void     reserve (__attribute__((unused)) size_type n)   { }
    inline size_type    capacity (void) const   { return 0; }
private:
    inline void     write_strz (const char*)  { assert (!"Writing nul characters into a text stream is not allowed"); }
    inline char*    encode_dec (char* fmt, uint32_t n) const;
    void      fmtstring (char* fmt, const char* typestr, bool bInteger) const;
    template <typename T>
    void      iformat (T v);
private:
    uint32_t      m_Flags;    ///< See ios_base::fmtflags.
    uint16_t      m_Width;    ///< Field width.
    uint8_t     m_Base;     ///< Numeric base for writing numbers.
    uint8_t     m_Precision;    ///< Number of digits after the decimal separator.
    void (*m_kprintf)(const char*, ...);
};

//----------------------------------------------------------------------

template <typename T>
void coutclass::iformat (T v)
{
    char fmt [16];
    fmtstring (fmt, printf_typestring(v), numeric_limits<T>::is_integer);
    kprintf(fmt, v);
}

/// Sets the flag \p f in the stream.
inline void coutclass::iwrite (fmtflags f)
{
    switch (f.f) {
  case oct: set_base (8); break;
  case dec: set_base (10);  break;
  case hex: set_base (16);  break;
  case left:  m_Flags |= left; m_Flags &= ~right; break;
  case right: m_Flags |= right; m_Flags &= ~left; break;
  default:  m_Flags |= f.f; break;
    }
}

//----------------------------------------------------------------------

template <typename T> struct object_text_writer_cout {
    inline void operator()(coutclass& os, const T& v) const { v.text_write (os); }
};
template <typename T> struct integral_text_object_writer_cout {
    inline void operator()(coutclass& os, const T& v) const { os.iwrite (v); }
};
template <typename T>
inline coutclass& operator<< (coutclass& os, const T& v) {
    typedef typename tm::Select <numeric_limits<T>::is_integral,
  integral_text_object_writer_cout<T>, object_text_writer_cout<T> >::Result object_writer_t;
    object_writer_t()(os, v);
    return (os);
}
// Needed because if called with a char[], numeric_limits will not work. Should be removed if I find out how to partial specialize for arrays...
inline coutclass& operator<< (coutclass& os, const char* v)
    { os.iwrite (v); return (os); }
inline coutclass& operator<< (coutclass& os, char* v)
    { os.iwrite (v); return (os); }

//----------------------------------------------------------------------

template <> struct object_text_writer_cout<string> {
    inline void operator()(coutclass& os, const string& v) const { os.iwrite (v); }
};
template <typename T> struct integral_text_object_writer_cout<T*> {
    inline void operator() (coutclass& os, const T* const& v) const
  { os.iwrite ((uintptr_t)(v)); }
};
#define COUTCLASS_CAST_OPERATOR(RealT, CastT)   \
template <> inline coutclass& operator<< (coutclass& os, const RealT& v) \
    { os.iwrite ((CastT)(v)); return (os); }
COUTCLASS_CAST_OPERATOR (uint8_t* const,  const char*)
COUTCLASS_CAST_OPERATOR (int8_t,    uint8_t)
COUTCLASS_CAST_OPERATOR (short int,   int)
COUTCLASS_CAST_OPERATOR (unsigned short,  unsigned int)
#if HAVE_THREE_CHAR_TYPES
COUTCLASS_CAST_OPERATOR (char,      uint8_t)
#endif
#undef COUTCLASS_CAST_OPERATOR

};

