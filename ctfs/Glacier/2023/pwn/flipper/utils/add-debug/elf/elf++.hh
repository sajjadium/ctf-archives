#ifndef _ELFPP_HH_
#define _ELFPP_HH_

#include "common.hh"
#include "data.hh"

#include <cstddef>
#include <memory>
#include <stdexcept>
#include <vector>

ELFPP_BEGIN_NAMESPACE

class elf;
class loader;
class section;
class strtab;
class symtab;

// XXX Audit for binary compatibility

// XXX Segments, other section types

/**
 * An exception indicating malformed ELF data.
 */
class format_error : public std::runtime_error
{
public:
        explicit format_error(const std::string &what_arg)
                : std::runtime_error(what_arg) { }
        explicit format_error(const char *what_arg)
                : std::runtime_error(what_arg) { }
};

/**
 * An ELF file.
 *
 * This class is internally reference counted and efficiently
 * copyable.
 *
 * Raw pointers to ELF data returned by any method of this object or
 * any object derived from this object point directly into loaded
 * section data.  Hence, callers must ensure that the loader passed to
 * this file remains live as long as any such pointer is in use.
 * Keeping any object that can return such a pointer live is
 * sufficieint to keep the loader live.
 */
class elf
{
public:
        /**
         * Construct an ELF file that is backed by data read from the
         * given loader.
         */
        explicit elf(const std::shared_ptr<loader> &l);

        /**
         * Construct an ELF file that is initially not valid.  Calling
         * methods other than operator= and valid on this results in
         * undefined behavior.
         */
        elf() = default;
        elf(const elf &o) = default;
        elf(elf &&o) = default;

        elf& operator=(const elf &o) = default;

        bool valid() const
        {
                return !!m;
        }

        /**
         * Return the ELF file header in canonical form (ELF64 in
         * native byte order).
         */
        const Ehdr<> &get_hdr() const;

        /**
         * Return the loader used by this file.
         */
        std::shared_ptr<loader> get_loader() const;

        /**
         * Return the sections in this file.
         */
        const std::vector<section> &sections() const;

        /**
         * Return the section with the specified name.  If no such
         * section is found, return an invalid section.
         */
        const section &get_section(const std::string &name) const;

        /**
         * Return the section at the given index.  If no such section
         * is found, return an invalid section.
         */
        const section &get_section(unsigned index) const;

private:
        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * An interface for loading sections of an ELF file.
 */
class loader
{
public:
        virtual ~loader() { }

        /**
         * Load the requested file section into memory and return a
         * pointer to the beginning of it.  This memory must remain
         * valid and unchanged until the loader is destroyed.  If the
         * loader cannot satisfy the full request for any reason
         * (including a premature EOF), it must throw an exception.
         */
        virtual const void *load(off_t offset, size_t size) = 0;
};

/**
 * An mmap-based loader that maps requested sections on demand.  This
 * will close fd when done, so the caller should dup the file
 * descriptor if it intends to continue using it.
 */
std::shared_ptr<loader> create_mmap_loader(int fd);

/**
 * An exception indicating that a section is not of the requested type.
 */
class section_type_mismatch : public std::logic_error
{
public:
        explicit section_type_mismatch(const std::string &what_arg)
                : std::logic_error(what_arg) { }
        explicit section_type_mismatch(const char *what_arg)
                : std::logic_error(what_arg) { }
};

/**
 * An ELF section.
 *
 * This class is internally reference counted and efficiently
 * copyable.
 */
class section
{
public:
        /**
         * Construct a section that is initially not valid.  Calling
         * methods other than operator= and valid on this results in
         * undefined behavior.
         */
        section() { }

        section(const elf &f, const void *hdr);
        section(const section &o) = default;
        section(section &&o) = default;

        /**
         * Return true if this section is valid and corresponds to a
         * section in the ELF file.
         */
        bool valid() const
        {
                return !!m;
        }

        /**
         * Return the ELF section header in canonical form (ELF64 in
         * native byte order).
         */
        const Shdr<> &get_hdr() const;

        /**
         * Return this section's name.
         */
        const char *get_name(size_t *len_out) const;
        /**
         * Return this section's name.  The returned string copies its
         * data, so loader liveness requirements don't apply.
         */
        std::string get_name() const;

        /**
         * Return this section's data.  If this is a NOBITS section,
         * return nullptr.
         */
        const void *data() const;
        /**
         * Return the size of this section in bytes.
         */
        size_t size() const;

        /**
         * Return this section as a strtab.  Throws
         * section_type_mismatch if this section is not a string
         * table.
         */
        strtab as_strtab() const;

        /**
         * Return this section as a symtab.  Throws
         * section_type_mismatch if this section is not a symbol
         * table.
         */
        symtab as_symtab() const;

private:
        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * A string table.
 *
 * This class is internally reference counted and efficiently
 * copyable.
 */
class strtab
{
public:
        /**
         * Construct a strtab that is initially not valid.  Calling
         * methods other than operator= and valid on this results in
         * undefined behavior.
         */
        strtab() = default;
        strtab(elf f, const void *data, size_t size);

        bool valid() const
        {
                return !!m;
        }

        /**
         * Return the string at the given offset in this string table.
         * If the offset is out of bounds, throws std::range_error.
         * This is very efficient since the returned pointer points
         * directly into the loaded section, though this still
         * verifies that the returned string is NUL-terminated.
         */
        const char *get(Elf64::Off offset, size_t *len_out) const;
        /**
         * Return the string at the given offset in this string table.
         */
        std::string get(Elf64::Off offset) const;

private:
        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * A symbol from a symbol table.
 */
class sym
{
        const strtab strs;
        Sym<> data;

public:
        sym(elf f, const void *data, strtab strs);

        /**
         * Return this symbol's raw data.
         */
        const Sym<> &get_data() const
        {
                return data;
        }

        /**
         * Return this symbol's name.
         *
         * This returns a pointer into the string table and, as such,
         * is very efficient.  If len_out is non-nullptr, *len_out
         * will be set the length of the returned string.
         */
        const char *get_name(size_t *len_out) const;

        /**
         * Return this symbol's name as a string.
         */
        std::string get_name() const;
};

/**
 * A symbol table.
 *
 * This class is internally reference counted and efficiently
 * copyable.
 */
class symtab
{
public:
        /**
         * Construct a symtab that is initially not valid.  Calling
         * methods other than operator= and valid on this results in
         * undefined behavior.
         */
        symtab() = default;
        symtab(elf f, const void *data, size_t size, strtab strs);

        bool valid() const
        {
                return !!m;
        }

        class iterator
        {
                const elf f;
                const strtab strs;
                const char *pos;
                size_t stride;

                iterator(const symtab &tab, const char *pos);
                friend class symtab;

        public:
                sym operator*() const
                {
                        return sym(f, pos, strs);
                }

                iterator& operator++()
                {
                        return *this += 1;
                }

                iterator operator++(int)
                {
                        iterator cur(*this);
                        *this += 1;
                        return cur;
                }

                iterator& operator+=(std::ptrdiff_t x)
                {
                        pos += x * stride;
                        return *this;
                }

                iterator& operator-=(std::ptrdiff_t x)
                {
                        pos -= x * stride;
                        return *this;
                }

                bool operator==(iterator &o) const
                {
                        return pos == o.pos;
                }

                bool operator!=(iterator &o) const
                {
                        return pos != o.pos;
                }
        };

        /**
         * Return an iterator to the first symbol.
         */
        iterator begin() const;

        /**
         * Return an iterator just past the last symbol.
         */
        iterator end() const;

private:
        struct impl;
        std::shared_ptr<impl> m;
};

ELFPP_END_NAMESPACE

#endif
