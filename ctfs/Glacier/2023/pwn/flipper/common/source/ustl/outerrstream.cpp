#include "outerrstream.h"
#include "ustringformat.h" // for vsnprintf (in string::format)

namespace ustl
{

coutclass cout_obj;
coutclass cerr_obj;
coutclass& cout = cout_obj;
coutclass& cerr = cerr_obj;

void coutclass::init()
{
  new (&cout_obj) coutclass(&kprintf);
  new (&cerr_obj) coutclass(&kprintfd);
}


/// Creates an output string stream linked to the given memory area.
coutclass::coutclass (void* p __attribute__((unused)), size_t n __attribute__((unused)))
: ostream (),
  m_Flags (0),
  m_Width (0),
  m_Base (10),
  m_Precision (2),
  m_kprintf(&kprintf)
{
    exceptions (goodbit);
}
/// Creates an output string stream linked to the given memory area.
coutclass::coutclass (void* p __attribute__((unused)), size_t n __attribute__((unused)), void (*m_kprintf)(const char*, ...))
: ostream (),
  m_Flags (0),
  m_Width (0),
  m_Base (10),
  m_Precision (2),
  m_kprintf(m_kprintf)
{
    exceptions (goodbit);
}

/// Creates an output string stream, initializing the buffer with v.
coutclass::coutclass ()
: ostream (),
  m_Flags (0),
  m_Width (0),
  m_Base (10),
  m_Precision (2),
  m_kprintf(&kprintf)
{
    exceptions (goodbit);
}

/// Creates an output string stream, initializing the buffer with v.
coutclass::coutclass (void (*m_kprintf)(const char*, ...))
: ostream (),
  m_Flags (0),
  m_Width (0),
  m_Base (10),
  m_Precision (2),
  m_kprintf(m_kprintf)
{
    exceptions (goodbit);
}

/// Writes a single character into the stream.
void coutclass::iwrite (uint8_t v)
{
  //debug(SCHEDULER, "writing single character: %d\n", v);
  m_kprintf("%c", v);
}

/// Writes the contents of \p buffer of \p size into the stream.
coutclass& coutclass::write (const void* buffer, size_type sz)
{
    kprintf("%.*s",(int)sz,(const char*)buffer);
    return (*this);
}

/// Simple decimal encoding of \p n into \p fmt.
inline char* coutclass::encode_dec (char* fmt, uint32_t n) const
{
    do {
  *fmt++ = '0' + n % 10;
    } while (n /= 10);
    return (fmt);
}

/// Generates a sprintf format string for the given type.
void coutclass::fmtstring (char* fmt, const char* typestr, bool bInteger) const
{
    *fmt++ = '%';
    if (m_Width)
  fmt = encode_dec (fmt, m_Width);
    if (m_Flags & left)
  *fmt++ = '-';
    if (!bInteger) {
  *fmt++ = '.';
  fmt = encode_dec (fmt, m_Precision);
    }
    while (*typestr)
  *fmt++ = *typestr++;
    if (bInteger) {
  if (m_Base == 16)
      fmt[-1] = 'X';
  else if (m_Base == 8)
      fmt[-1] = 'o';
    } else {
  if (m_Flags & scientific)
      fmt[-1] = 'E';
    }
    *fmt = 0;
}

/// Writes \p v into the stream as utf8
void coutclass::iwrite (wchar_t v)
{
    char buffer [8];
    *utf8out(buffer) = v;
    write (buffer, Utf8Bytes(v));
}

/// Writes value \p v into the stream as text.
void coutclass::iwrite (bool v)
{
    static const char tf[2][8] = { "false", "true" };
    write (tf[v], 5 - v);
}

/// Equivalent to a sprintf on the string.
int coutclass::format (const char* fmt, ...)
{
    va_list args;
    va_start (args, fmt);
    m_kprintf(fmt, args);
    va_end (args);
    return (0);
}

/// Links to string \p l as resizable.
void coutclass::link (void* p, size_type n)
{
    assert ((p || !n) && "The output string buffer must not be read-only");
}

/// Attempts to create more output space. Returns remaining().
coutclass::size_type coutclass::overflow (size_type n __attribute__((unused)))
{
    return remaining();
}

}
