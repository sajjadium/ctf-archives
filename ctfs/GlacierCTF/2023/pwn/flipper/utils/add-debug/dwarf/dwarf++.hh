#ifndef _DWARFPP_HH_
#define _DWARFPP_HH_

#ifndef DWARFPP_BEGIN_NAMESPACE
#define DWARFPP_BEGIN_NAMESPACE namespace dwarf {
#define DWARFPP_END_NAMESPACE   }
#endif

#include "data.hh"
#include "small_vector.hh"

#include <initializer_list>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

DWARFPP_BEGIN_NAMESPACE

// Forward declarations
class dwarf;
class loader;
class compilation_unit;
class type_unit;
class die;
class value;
class expr;
class expr_context;
class expr_result;
class rangelist;
class line_table;

// Internal type forward-declarations
struct section;
struct abbrev_entry;
struct cursor;

// XXX Audit for binary-compatibility

// XXX Might be able to reduce private coupling by making class
// section public (and clean it up and maybe rename it slice) and
// provide methods to get the backing data of things.
//
// XXX Make slice generic, without formatting information?  Still want
// lightweight cursors, so maybe the cursor methods that need the
// format should take a const reference to a format stored in the
// compilation unit?

// XXX operator==/!= and hash functions

// XXX Support non-native byte order

// XXX Indicate DWARF4 in all spec references

// XXX Big missing support: .debug_aranges, .debug_frame, loclists,
// macros

//////////////////////////////////////////////////////////////////
// DWARF files
//

/**
 * An exception indicating malformed DWARF data.
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
 * DWARF section types.  These correspond to the names of ELF
 * sections, though DWARF can be embedded in other formats.
 */
enum class section_type
{
        abbrev,
        aranges,
        frame,
        info,
        line,
        loc,
        macinfo,
        pubnames,
        pubtypes,
        ranges,
        str,
        types,
};

std::string
to_string(section_type v);

/**
 * A DWARF file.  This class is internally reference counted and can
 * be efficiently copied.
 *
 * Objects retrieved from this object may depend on it; the caller is
 * responsible for keeping this object live as long as any retrieved
 * object may be in use.
 */
class dwarf
{
public:
        /**
         * Construct a DWARF file that is backed by sections read from
         * the given loader.
         */
        explicit dwarf(const std::shared_ptr<loader> &l);

        /**
         * Construct a DWARF file that is initially not valid.
         */
        dwarf() = default;
        dwarf(const dwarf&) = default;
        dwarf(dwarf&&) = default;
        ~dwarf();

        dwarf& operator=(const dwarf &o) = default;
        dwarf& operator=(dwarf &&o) = default;

        bool operator==(const dwarf &o) const
        {
                return m == o.m;
        }

        bool operator!=(const dwarf &o) const
        {
                return m != o.m;
        }

        /**
         * Return true if this object represents a DWARF file.
         * Default constructed dwarf objects are not valid.
         */
        bool valid() const
        {
                return !!m;
        }

        // XXX This allows the compilation units to be modified and
        // ties us to a vector.  Probably should return an opaque
        // iterable collection over const references.
        /**
         * Return the list of compilation units in this DWARF file.
         */
        const std::vector<compilation_unit> &compilation_units() const;

        /**
         * Return the type unit with the given signature.  If the
         * signature does not correspond to a type unit, throws
         * out_of_range.
         */
        const type_unit &get_type_unit(uint64_t type_signature) const;

        /**
         * \internal Retrieve the specified section from this file.
         * If the section does not exist, throws format_error.
         */
        std::shared_ptr<section> get_section(section_type type) const;

private:
        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * An interface for lazily loading DWARF sections.
 */
class loader
{
public:
        virtual ~loader() { }

        /**
         * Load the requested DWARF section into memory and return a
         * pointer to the beginning of it.  This memory must remain
         * valid and unchanged until the loader is destroyed.  If the
         * requested section does not exist, this should return
         * nullptr.  If the section exists but cannot be loaded for
         * any reason, this should throw an exception.
         */
        virtual const void *load(section_type section, size_t *size_out) = 0;
};

/**
 * The base class for a compilation unit or type unit within a DWARF
 * file.  A unit consists of a rooted tree of DIEs, plus additional
 * metadata that depends on the type of unit.
 */
class unit
{
public:
        virtual ~unit() = 0;

        bool operator==(const unit &o) const
        {
                return m == o.m;
        }

        bool operator!=(const unit &o) const
        {
                return m != o.m;
        }

        /**
         * Return true if this object is valid.  Default constructed
         * unit objects are not valid.
         */
        bool valid() const
        {
                return !!m;
        }

        /**
         * Return the dwarf file this unit is in.
         */
        const dwarf &get_dwarf() const;

        /**
         * Return the byte offset of this unit's header in its
         * section (.debug_info or .debug_types).
         */
        section_offset get_section_offset() const;

        /**
         * Return the root DIE of this unit.  For a compilation unit,
         * this should be a DW_TAG::compilation_unit or
         * DW_TAG::partial_unit.
         */
        const die &root() const;

        /**
         * \internal Return the data for this unit.
         */
        const std::shared_ptr<section> &data() const;

        /**
         * \internal Return the abbrev for the specified abbrev
         * code.
         */
        const abbrev_entry &get_abbrev(std::uint64_t acode) const;

protected:
        friend struct ::std::hash<unit>;
        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * A compilation unit within a DWARF file.  Most of the information
 * in a DWARF file is divided up by compilation unit.  This class is
 * internally reference counted and can be efficiently copied.
 */
class compilation_unit : public unit
{
public:
        compilation_unit() = default;
        compilation_unit(const compilation_unit &o) = default;
        compilation_unit(compilation_unit &&o) = default;

        compilation_unit& operator=(const compilation_unit &o) = default;
        compilation_unit& operator=(compilation_unit &&o) = default;

        /**
         * \internal Construct a compilation unit whose header begins
         * offset bytes into the .debug_info section of file.
         */
        compilation_unit(const dwarf &file, section_offset offset);

        /**
         * Return the line number table of this compilation unit.
         * Returns an invalid line table if this unit has no line
         * table.
         */
        const line_table &get_line_table() const;
};

/**
 * A type unit.  Type units allow complex type information to be
 * shared between compilation units.
 */
class type_unit : public unit
{
public:
        type_unit() = default;
        type_unit(const type_unit &o) = default;
        type_unit(type_unit &&o) = default;

        type_unit &operator=(const type_unit &o) = default;
        type_unit &operator=(type_unit &&o) = default;

        /**
         * \internal Construct a type unit whose header begins offset
         * bytes into the .debug_types section of file.
         */
        type_unit(const dwarf &file, section_offset offset);

        /**
         * Return the 64-bit unique signature that identifies this
         * type unit.  This is how DIEs from other units refer to type
         * described by this unit.
         */
        uint64_t get_type_signature() const;

        // XXX Can a type unit contain more than one top-level DIE?
        // The description of type_offset makes it sound like it
        // might.

        /**
         * Return the DIE of the type described by this type unit.
         * This may not be the root DIE of this unit if the type is
         * nested in namespaces or other structures.
         */
        const die &type() const;
};

//////////////////////////////////////////////////////////////////
// Debugging information entries (DIEs)
//

/**
 * A Debugging Information Entry, or DIE.  The basic unit of
 * information in a DWARF file.
 */
class die
{
        // XXX Make this class better for use in maps.  Currently dies
        // are fairly big and expensive to copy, but most of that
        // information can be constructed lazily.  This is also bad
        // for use in caches since it will keep the DWARF file alive.
        // OTOH, maybe caches need eviction anyway.
public:
        DW_TAG tag;

        die() : cu(nullptr), abbrev(nullptr) { }
        die(const die &o) = default;
        die(die &&o) = default;

        die& operator=(const die &o) = default;
        die& operator=(die &&o) = default;

        /**
         * Return true if this object represents a DIE in a DWARF
         * file.  Default constructed objects are not valid and some
         * methods return invalid DIEs to indicate failures.
         */
        bool valid() const
        {
                return abbrev != nullptr;
        }

        /**
         * Return the unit containing this DIE.
         */
        const unit &get_unit() const;

        /**
         * Return this DIE's byte offset within its compilation unit.
         */
        section_offset get_unit_offset() const
        {
                return offset;
        }

        /**
         * Return this DIE's byte offset within its section.
         */
        section_offset get_section_offset() const;

        /**
         * Return true if this DIE has the requested attribute.
         */
        bool has(DW_AT attr) const;

        /**
         * Return the value of attr.  Throws out_of_range if this DIE
         * does not have the specified attribute.  It is generally
         * better to use the type-safe attribute getters (the global
         * functions beginning with at_*) when possible.
         */
        value operator[](DW_AT attr) const;

        /**
         * Return the value of attr after resolving specification and
         * abstract origin references.  If the attribute cannot be
         * resolved, returns an invalid value.  Declaration DIEs can
         * "complete" a previous non-defining declaration DIE and
         * similarly inherit the non-defining declaration's attributes
         * (DWARF4 section 2.13) Likewise, any DIE that is a child of
         * a concrete inlined instance can specify another DIE as its
         * "abstract origin" and the original DIE will inherit the
         * attributes of its abstract origin (DWARF4 section 3.3.8.2).
         */
        value resolve(DW_AT attr) const;

        class iterator;

        /**
         * Return an iterator over the children of this DIE.  Note
         * that the DIEs returned by this iterator are temporary, so
         * if you need to store a DIE for more than one loop
         * iteration, you must copy it.
         */
        iterator begin() const;
        iterator end() const;

        /**
         * Return a vector of the attributes of this DIE.
         */
        const std::vector<std::pair<DW_AT, value> > attributes() const;

        bool operator==(const die &o) const;
        bool operator!=(const die &o) const;

private:
        friend class unit;
        friend class type_unit;
        friend class value;
        // XXX If we can get the CU, we don't need this
        friend struct ::std::hash<die>;

        const unit *cu;
        // The abbrev of this DIE.  By convention, if this DIE
        // represents a sibling list terminator, this is null.  This
        // object is kept live by the CU.
        const abbrev_entry *abbrev;
        // The beginning of this DIE, relative to the CU.
        section_offset offset;
        // Offsets of attributes, relative to cu's subsection.  The
        // vast majority of DIEs tend to have six or fewer attributes,
        // so we reserve space in the DIE itself for six attributes.
        small_vector<section_offset, 6> attrs;
        // The offset of the next DIE, relative to cu'd subsection.
        // This is set even for sibling list terminators.
        section_offset next;

        die(const unit *cu);

        /**
         * Read this DIE from the given offset in cu.
         */
        void read(section_offset off);
};

/**
 * An iterator over a sequence of sibling DIEs.
 */
class die::iterator
{
public:
        iterator() = default;
        iterator(const iterator &o) = default;
        iterator(iterator &&o) = default;

        iterator& operator=(const iterator &o) = default;
        iterator& operator=(iterator &&o) = default;

        const die &operator*() const
        {
                return d;
        }

        const die *operator->() const
        {
                return &d;
        }

        // XXX Make this less confusing by implementing operator== instead
        bool operator!=(const iterator &o) const
        {
                // Quick test of abbrevs.  In particular, this weeds
                // out non-end against end, which is a common
                // comparison while iterating, though it also weeds
                // out many other things.
                if (d.abbrev != o.d.abbrev)
                        return true;

                // Same, possibly NULL abbrev.  If abbrev is NULL,
                // then next's are uncomparable, so we need to stop
                // now.  We consider all ends to be the same, without
                // comparing cu's.
                if (d.abbrev == nullptr)
                        return false;

                // Comparing two non-end abbrevs.
                return d.next != o.d.next || d.cu != o.d.cu;
        }

        iterator &operator++();

private:
        friend class die;

        iterator(const unit *cu, section_offset off);

        die d;
};

inline die::iterator
die::end() const
{
        return iterator();
}

/**
 * An exception indicating that a value is not of the requested type.
 */
class value_type_mismatch : public std::logic_error
{
public:
        explicit value_type_mismatch(const std::string &what_arg)
                : std::logic_error(what_arg) { }
        explicit value_type_mismatch(const char *what_arg)
                : std::logic_error(what_arg) { }
};

/**
 * The value of a DIE attribute.
 *
 * This is logically a union of many different types.  Each type has a
 * corresponding as_* methods that will return the value as that type
 * or throw value_type_mismatch if the attribute is not of the
 * requested type.
 *
 * Values of "constant" type are somewhat ambiguous and
 * context-dependent.  Constant forms with specified signed-ness have
 * type "uconstant" or "sconstant", while other constant forms have
 * type "constant".  If the value's type is "constant", it can be
 * retrieved using either as_uconstant or as_sconstant.
 *
 * Some other types can also be coerced.  These are documented on the
 * individual as_* methods.
 *
 * There is no as_line; while there is an attribute for line tables,
 * line tables are really associated with compilation units (and
 * require additional context from the compilation unit).  Use
 * compilation_unit::get_line_table instead.
 */
class value
{
public:
        enum class type
        {
                invalid,
                address,
                block,
                constant,
                uconstant,
                sconstant,
                exprloc,
                flag,
                line,
                loclist,
                mac,
                rangelist,
                reference,
                string
        };

        /**
         * Construct a value with type `type::invalid`.
         */
        value() : cu(nullptr), typ(type::invalid) { }

        value(const value &o) = default;
        value(value &&o) = default;

        value& operator=(const value &o) = default;
        value& operator=(value &&o) = default;

        /**
         * Return true if this object represents a valid value.
         * Default constructed line tables are not valid.
         */
        bool valid() const
        {
                return typ != type::invalid;
        }

        /**
         * Return this value's byte offset within its compilation
         * unit.
         */
        section_offset get_unit_offset() const
        {
                return offset;
        }

        /**
         * Return this value's byte offset within its section.
         */
        section_offset get_section_offset() const;

        type get_type() const
        {
                return typ;
        }

        /**
         * Return this value's attribute encoding.  This automatically
         * resolves indirect encodings, so this will never return
         * DW_FORM::indirect.  Note that the mapping from forms to
         * types is non-trivial and often depends on the attribute
         * (especially prior to DWARF 4).
         */
        DW_FORM get_form() const
        {
                return form;
        }

        /**
         * Return this value as a target machine address.
         */
        taddr as_address() const;

        /**
         * Return this value as a block.  The returned pointer points
         * directly into the section data, so the caller must ensure
         * that remains valid as long as the data is in use.
         * *size_out is set to the length of the returned block, in
         * bytes.
         *
         * This automatically coerces "exprloc" type values by
         * returning the raw bytes of the encoded expression.
         */
        const void *as_block(size_t *size_out) const;

        /**
         * Return this value as an unsigned constant.  This
         * automatically coerces "constant" type values by
         * interpreting their bytes as unsigned.
         */
        uint64_t as_uconstant() const;

        /**
         * Return this value as a signed constant.  This automatically
         * coerces "constant" type values by interpreting their bytes
         * as twos-complement signed values.
         */
        int64_t as_sconstant() const;

        /**
         * Return this value as an expression.  This automatically
         * coerces "block" type values by interpreting the bytes in
         * the block as an expression (prior to DWARF 4, exprlocs were
         * always encoded as blocks, though the library automatically
         * distinguishes these types based on context).
         */
        expr as_exprloc() const;

        /**
         * Return this value as a boolean flag.
         */
        bool as_flag() const;

        // XXX loclistptr, macptr

        /**
         * Return this value as a rangelist.
         */
        rangelist as_rangelist() const;

        /**
         * For a reference type value, return the referenced DIE.
         * This DIE may be in a different compilation unit or could
         * be a DIE in a type unit.
         */
        die as_reference() const;

        /**
         * Return this value as a string.
         */
        std::string as_string() const;

        /**
         * Fill the given string buffer with the string value of this
         * value.  This is useful to minimize allocation when reading
         * several string-type values.
         */
        void as_string(std::string &buf) const;

        /**
         * Return this value as a NUL-terminated character string.
         * The returned pointer points directly into the section data,
         * so the caller must ensure that remains valid as long as the
         * data is in use.  *size_out, if not NULL, is set to the
         * length of the returned string without the NUL-terminator.
         */
        const char *as_cstr(size_t *size_out = nullptr) const;

        /**
         * Return this value as a section offset.  This is applicable
         * to lineptr, loclistptr, macptr, and rangelistptr.
         */
        section_offset as_sec_offset() const;

private:
        friend class die;

        value(const unit *cu,
              DW_AT name, DW_FORM form, type typ, section_offset offset);

        void resolve_indirect(DW_AT name);

        const unit *cu;
        DW_FORM form;
        type typ;
        section_offset offset;
};

std::string
to_string(value::type v);

std::string
to_string(const value &v);

//////////////////////////////////////////////////////////////////
// Expressions and location descriptions
//

/**
 * An exception during expression evaluation.
 */
class expr_error : public std::runtime_error
{
public:
        explicit expr_error(const std::string &what_arg)
                : std::runtime_error(what_arg) { }
        explicit expr_error(const char *what_arg)
                : std::runtime_error(what_arg) { }
};

/**
 * A DWARF expression or location description.
 */
class expr
{
public:
        /**
         * Short-hand for evaluate(ctx, {}).
         */
        expr_result evaluate(expr_context *ctx) const;

        /**
         * Short-hand for evaluate(ctx, {argument}).
         */
        expr_result evaluate(expr_context *ctx, taddr argument) const;

        /**
         * Return the result of evaluating this expression using the
         * specified expression context.  The expression stack will be
         * initialized with the given arguments such that the first
         * arguments is at the top of the stack and the last argument
         * at the bottom of the stack.
         *
         * Throws expr_error if there is an error evaluating the
         * expression (such as an unknown operation, stack underflow,
         * bounds error, etc.)
         */
        expr_result evaluate(expr_context *ctx, const std::initializer_list<taddr> &arguments) const;

private:
        // XXX This will need more information for some operations
        expr(const unit *cu,
             section_offset offset, section_length len);

        friend class value;

        const unit *cu;
        section_offset offset;
        section_length len;
};

/**
 * An interface that provides contextual information for expression
 * evaluation.  Callers of expr::evaluate are expected to subclass
 * this in order to provide this information to the expression
 * evaluation engine.  The default implementation throws expr_error
 * for all methods.
 */
class expr_context
{
public:
        virtual ~expr_context() { }

        /**
         * Return the value stored in register regnum.  This is used
         * to implement DW_OP_breg* operations.
         */
        virtual taddr reg([[gnu::unused]] unsigned regnum)
        {
                throw expr_error("DW_OP_breg* operations not supported");
        }

        /**
         * Implement DW_OP_deref_size.
         */
        virtual taddr deref_size([[gnu::unused]] taddr address, [[gnu::unused]] unsigned size)
        {
                throw expr_error("DW_OP_deref_size operations not supported");
        }

        /**
         * Implement DW_OP_xderef_size.
         */
        virtual taddr xderef_size([[gnu::unused]] taddr address, [[gnu::unused]] taddr asid, [[gnu::unused]] unsigned size)
        {
                throw expr_error("DW_OP_xderef_size operations not supported");
        }

        /**
         * Implement DW_OP_form_tls_address.
         */
        virtual taddr form_tls_address([[gnu::unused]] taddr address)
        {
                throw expr_error("DW_OP_form_tls_address operations not supported");
        }
};

/**
 * An instance of expr_context that throws expr_error for all methods.
 * This is equivalent to the default construction of expr_context, but
 * often more convenient to use.
 */
extern expr_context no_expr_context;

// XXX Provide methods to check type and fetch value?
/**
 * The result of evaluating a DWARF expression or location
 * description.
 */
class expr_result
{
public:
        enum class type {
                /**
                 * value specifies the address in memory of an object.
                 * This is also the result type used for general
                 * expressions that do not refer to object locations.
                 */
                address,
                /**
                 * value specifies a register storing an object.
                 */
                reg,
                /**
                 * The object does not have a location.  value is the
                 * value of the object.
                 */
                literal,
                /**
                 * The object does not have a location.  Its value is
                 * pointed to by the 'implicit' field.
                 */
                implicit,
                /**
                 * The object is present in the source, but not in the
                 * object code, and hence does not have a location or
                 * a value.
                 */
                empty,
        };

        /**
         * For location descriptions, the type of location this result
         * describes.
         */
        type location_type;

        /**
         * For general-purpose expressions, the result of expression.
         * For address location descriptions, the address in memory of
         * the object.  For register location descriptions, the
         * register storing the object.  For literal location
         * descriptions, the value of the object.
         */
        taddr value;

        /**
         * For implicit location descriptions, a pointer to a block
         * representing the value in the memory representation of the
         * target machine.
         */
        const char *implicit;
        size_t implicit_len;

        // XXX Composite locations
};

std::string
to_string(expr_result::type v);

//////////////////////////////////////////////////////////////////
// Range lists
//

/**
 * A DWARF range list describing a set of possibly non-contiguous
 * addresses.
 */
class rangelist
{
public:
        /**
         * \internal Construct a range list whose data begins at the
         * given offset in sec.  cu_addr_size is the address size of
         * the associated compilation unit.  cu_low_pc is the
         * DW_AT::low_pc attribute of the compilation unit containing
         * the referring DIE or 0 (this is used as the base address of
         * the range list).
         */
        rangelist(const std::shared_ptr<section> &sec, section_offset off,
                  unsigned cu_addr_size, taddr cu_low_pc);

        /**
         * Construct a range list from a sequence of {low, high}
         * pairs.
         */
        rangelist(const std::initializer_list<std::pair<taddr, taddr> > &ranges);

        /**
         * Construct an empty range list.
         */
        rangelist() = default;

        /** Copy constructor */
        rangelist(const rangelist &o) = default;
        /** Move constructor */
        rangelist(rangelist &&o) = default;

        rangelist& operator=(const rangelist &o) = default;
        rangelist& operator=(rangelist &&o) = default;

        class entry;
        typedef entry value_type;

        class iterator;

        /**
         * Return an iterator over the entries in this range list.
         * The ranges returned by this iterator are temporary, so if
         * you need to store a range for more than one loop iteration,
         * you must copy it.
         */
        iterator begin() const;

        /**
         * Return an iterator to one past the last entry in this range
         * list.
         */
        iterator end() const;

        /**
         * Return true if this range list contains the given address.
         */
        bool contains(taddr addr) const;

private:
        std::vector<taddr> synthetic;
        std::shared_ptr<section> sec;
        taddr base_addr;
};

/**
 * An entry in a range list.  The range spans addresses [low, high).
 */
class rangelist::entry
{
public:
        taddr low, high;

        /**
         * Return true if addr is within this entry's bounds.
         */
        bool contains(taddr addr) const
        {
                return low <= addr && addr < high;
        }
};

/**
 * An iterator over a sequence of ranges in a range list.
 */
class rangelist::iterator
{
public:
        /**
         * \internal Construct an end iterator.
         */
        iterator() : sec(nullptr), base_addr(0), pos(0) { }

        /**
         * \internal Construct an iterator that reads rangelist data
         * from the beginning of the given section and starts with the
         * given base address.
         */
        iterator(const std::shared_ptr<section> &sec, taddr base_addr);

        /** Copy constructor */
        iterator(const iterator &o) = default;
        /** Move constructor */
        iterator(iterator &&o) = default;

        iterator& operator=(const iterator &o) = default;
        iterator& operator=(iterator &&o) = default;

        /**
         * Return the current range list entry.  This entry is reused
         * internally, so the caller should copy it if it needs to
         * persist past the next increment.
         */
        const rangelist::entry &operator*() const
        {
                return entry;
        }

        /** Dereference operator */
        const rangelist::entry *operator->() const
        {
                return &entry;
        }

        /** Equality operator */
        bool operator==(const iterator &o) const
        {
                return sec == o.sec && pos == o.pos;
        }

        /** Inequality operator */
        bool operator!=(const iterator &o) const
        {
                return !(*this == o);
        }

        /**
         * Increment this iterator to point to the next range list
         * entry.
         */
        iterator &operator++();

private:
        std::shared_ptr<section> sec;
        taddr base_addr;
        section_offset pos;
        rangelist::entry entry;
};

//////////////////////////////////////////////////////////////////
// Line number tables
//

/**
 * A DWARF line number table.  A line number table is a list of line
 * table entries, broken up into "sequences".  Within a sequence,
 * entries are in order of increasing program counter ("address") and
 * an entry provides information for all program counters between the
 * entry's address and the address of the next entry.  Each sequence
 * is terminated by a special entry with its
 * line_table::entry::end_sequence flag set.  The line number table
 * also records the set of source files for a given compilation unit,
 * which can be referred to from other DIE attributes.
 */
class line_table
{
public:
        /**
         * \internal Construct a line number table whose header begins
         * at the given offset in sec.  cu_addr_size is the address
         * size of the associated compilation unit.  cu_comp_dir and
         * cu_name give the DW_AT::comp_dir and DW_AT::name attributes
         * of the associated compilation unit.
         */
        line_table(const std::shared_ptr<section> &sec, section_offset offset,
                   unsigned cu_addr_size, const std::string &cu_comp_dir,
                   const std::string &cu_name);

        /**
         * Construct an invalid, empty line table.
         */
        line_table() = default;

        /** Copy constructor */
        line_table(const line_table &o) = default;
        /** Move constructor */
        line_table(line_table &&o) = default;

        line_table &operator=(const line_table &o) = default;
        line_table &operator=(line_table &&o) = default;

        /**
         * Return true if this object represents an initialized line
         * table.  Default constructed line tables are not valid.
         */
        bool valid() const
        {
                return !!m;
        }

        class file;
        class entry;
        typedef entry value_type;

        class iterator;

        /**
         * Return an iterator to the beginning of this line number
         * table.  If called on an invalid line table, this will
         * return an iterator equal to end().
         */
        iterator begin() const;

        /**
         * Return an iterator to one past the last entry in this line
         * number table.
         */
        iterator end() const;

        /**
         * Return an iterator to the line table entry containing addr
         * (roughly, the entry with the highest address less than or
         * equal to addr, but accounting for end_sequence entries).
         * Returns end() if there is no such entry.
         */
        iterator find_address(taddr addr) const;

        /**
         * Return the index'th file in the line table.  These indexes
         * are typically used by declaration and call coordinates.  If
         * index is out of range, throws out_of_range.
         */
        const file *get_file(unsigned index) const;

private:
        friend class iterator;

        struct impl;
        std::shared_ptr<impl> m;
};

/**
 * A source file in a line table.
 */
class line_table::file
{
public:
        /**
         * The absolute path of this source file.
         */
        std::string path;

        /**
         * The last modification time of this source file in an
         * implementation-defined encoding or 0 if unknown.
         */
        uint64_t mtime;

        /**
         * The size in bytes of this source file or 0 if unknown.
         */
        uint64_t length;

        /**
         * Construct a source file object.
         */
        file(std::string path = "", uint64_t mtime = 0, uint64_t length = 0);
};

/**
 * An entry in the line table.
 */
class line_table::entry
{
public:
        /**
         * The program counter value corresponding to a machine
         * instruction generated by the compiler.
         */
        taddr address;

        /**
         * The index of an operation within a VLIW instruction. The
         * index of the first operation is 0. For non-VLIW
         * architectures, this will always be 0.
         */
        unsigned op_index;

        /**
         * The source file containing this instruction.
         */
        const line_table::file *file;

        /**
         * The index of the source file containing this instruction.
         */
        unsigned file_index;

        /**
         * The source line number of this instruction, starting at 1.
         * This may be 0 if this instruction cannot be attributed to
         * any source line.
         */
        unsigned line;

        /**
         * The column number within this source line, starting at 1.
         * The value 0 indicates that a statement begins at the "left
         * edge" of the line, whatever that means.
         */
        unsigned column;

        /**
         * True if this instruction is a recommended breakpoint
         * location.  Typically this is the beginning of a statement.
         */
        bool is_stmt;

        /**
         * True if this instruction is the beginning of a basic block.
         */
        bool basic_block;

        /**
         * True if this address is the first byte after the end of a
         * sequence of target machine instructions.  In this case, all
         * other fields besides address are not meaningful.
         */
        bool end_sequence;

        /**
         * True if this address is one where execution should be
         * suspended for an entry breakpoint of a function.
         */
        bool prologue_end;

        /**
         * True if this address is one where execution should be
         * suspended for an exit breakpoint of a function.
         */
        bool epilogue_begin;

        /**
         * The instruction set architecture of this instruction.  The
         * meaning of this field is generally defined by an
         * architecture's ABI.
         */
        unsigned isa;

        /**
         * A number that identifies the block containing the current
         * instruction if multiple blocks are associated with the same
         * source file, line, and column.
         */
        unsigned discriminator;

        /**
         * Reset this line info object to the default initial values
         * for all fields.  is_stmt has no default value, so the
         * caller must provide it.
         */
        void reset(bool is_stmt);

        /**
         * Return a descriptive string of the form
         * "filename[:line[:column]]".
         */
        std::string get_description() const;
};

/**
 * An iterator over the entries in a line table.
 */
class line_table::iterator
{
public:
        /**
         * \internal Construct an iterator for the given line table
         * starting pos bytes into the table's section.
         */
        iterator(const line_table *table, section_offset pos);

        /** Copy constructor */
        iterator(const iterator &o) = default;
        /** Move constructor */
        iterator(iterator &&o) = default;

        iterator &operator=(const iterator &o) = default;
        iterator &operator=(iterator &&o) = default;

        /**
         * Return the current line table entry.  This entry is reused
         * internally, so the caller should copy it if it needs to
         * persist past the next increment.
         */
        const line_table::entry &operator*() const
        {
                return entry;
        }

        /** Dereference operator */
        const line_table::entry *operator->() const
        {
                return &entry;
        }

        /** Equality operator */
        bool operator==(const iterator &o) const
        {
                return o.pos == pos && o.table == table;
        }

        /** Inequality operator */
        bool operator!=(const iterator &o) const
        {
                return !(*this == o);
        }

        /**
         * Increment this iterator to point to the next line table
         * entry.
         */
        iterator &operator++();

        /** Post-increment operator */
        iterator operator++(int)
        {
                iterator tmp(*this);
                ++(*this);
                return tmp;
        }

private:
        const line_table *table;
        line_table::entry entry, regs;
        section_offset pos;

        /**
         * Process the next opcode.  If the opcode "adds a row to the
         * table", update entry to reflect the row and return true.
         */
        bool step(cursor *cur);
};

//////////////////////////////////////////////////////////////////
// Type-safe attribute getters
//

// XXX More

die at_abstract_origin(const die &d);
DW_ACCESS at_accessibility(const die &d);
uint64_t at_allocated(const die &d, expr_context *ctx);
bool at_artificial(const die &d);
uint64_t at_associated(const die &d, expr_context *ctx);
uint64_t at_bit_offset(const die &d, expr_context *ctx);
uint64_t at_bit_size(const die &d, expr_context *ctx);
uint64_t at_bit_stride(const die &d, expr_context *ctx);
uint64_t at_byte_size(const die &d, expr_context *ctx);
uint64_t at_byte_stride(const die &d, expr_context *ctx);
DW_CC at_calling_convention(const die &d);
die at_common_reference(const die &d);
std::string at_comp_dir(const die &d);
value at_const_value(const die &d);
bool at_const_expr(const die &d);
die at_containing_type(const die &d);
uint64_t at_count(const die &d, expr_context *ctx);
expr_result at_data_member_location(const die &d, expr_context *ctx, taddr base, taddr pc);
bool at_declaration(const die &d);
std::string at_description(const die &d);
die at_discr(const die &d);
value at_discr_value(const die &d);
bool at_elemental(const die &d);
DW_ATE at_encoding(const die &d);
DW_END at_endianity(const die &d);
taddr at_entry_pc(const die &d);
bool at_enum_class(const die &d);
bool at_explicit(const die &d);
die at_extension(const die &d);
bool at_external(const die &d);
die at_friend(const die &d);
taddr at_high_pc(const die &d);
DW_ID at_identifier_case(const die &d);
die at_import(const die &d);
DW_INL at_inline(const die &d);
bool at_is_optional(const die &d);
DW_LANG at_language(const die &d);
std::string at_linkage_name(const die &d);
taddr at_low_pc(const die &d);
uint64_t at_lower_bound(const die &d, expr_context *ctx);
bool at_main_subprogram(const die &d);
bool at_mutable(const die &d);
std::string at_name(const die &d);
die at_namelist_item(const die &d);
die at_object_pointer(const die &d);
DW_ORD at_ordering(const die &d);
std::string at_picture_string(const die &d);
die at_priority(const die &d);
std::string at_producer(const die &d);
bool at_prototyped(const die &d);
bool at_pure(const die &d);
rangelist at_ranges(const die &d);
bool at_recursive(const die &d);
die at_sibling(const die &d);
die at_signature(const die &d);
die at_small(const die &d);
die at_specification(const die &d);
bool at_threads_scaled(const die &d);
die at_type(const die &d);
uint64_t at_upper_bound(const die &d, expr_context *ctx);
bool at_use_UTF8(const die &d);
bool at_variable_parameter(const die &d);
DW_VIRTUALITY at_virtuality(const die &d);
DW_VIS at_visibility(const die &d);

/**
 * Return the PC range spanned by the code of a DIE.  The DIE must
 * either have DW_AT::ranges or DW_AT::low_pc.  It may optionally have
 * DW_AT::high_pc.
 */
rangelist die_pc_range(const die &d);

//////////////////////////////////////////////////////////////////
// Utilities
//

/**
 * An index of sibling DIEs by some string attribute.  This index is
 * lazily constructed and space-efficient.
 */
class die_str_map
{
public:
        /**
         * Construct the index of the attr attribute of all immediate
         * children of parent whose tags are in accept.
         */
        die_str_map(const die &parent, DW_AT attr,
                    const std::initializer_list<DW_TAG> &accept);

        die_str_map() = default;
        die_str_map(const die_str_map &o) = default;
        die_str_map(die_str_map &&o) = default;

        die_str_map& operator=(const die_str_map &o) = default;
        die_str_map& operator=(die_str_map &&o) = default;

        /**
         * Construct a string map for the type names of parent's
         * immediate children.
         *
         * XXX This should use .debug_pubtypes if parent is a compile
         * unit's root DIE, but it currently does not.
         */
        static die_str_map from_type_names(const die &parent);

        /**
         * Return the DIE whose attribute matches val.  If no such DIE
         * exists, return an invalid die object.
         */
        const die &operator[](const char *val) const;

        /**
         * Short-hand for [value.c_str()].
         */
        const die &operator[](const std::string &val) const
        {
                return (*this)[val.c_str()];
        }

private:
        struct impl;
        std::shared_ptr<impl> m;
};

//////////////////////////////////////////////////////////////////
// ELF support
//

namespace elf
{
        /**
         * Translate an ELF section name info a DWARF section type.
         * If the section is a valid DWARF section name, sets *out to
         * the type and returns true.  If not, returns false.
         */
        bool section_name_to_type(const char *name, section_type *out);

        /**
         * Translate a DWARF section type into an ELF section name.
         */
        const char *section_type_to_name(section_type type);

        template<typename Elf>
        class elf_loader : public loader
        {
                Elf f;

        public:
                elf_loader(const Elf &file) : f(file) { }

                const void *load(section_type section, size_t *size_out)
                {
                        auto sec = f.get_section(section_type_to_name(section));
                        if (!sec.valid())
                                return nullptr;
                        *size_out = sec.size();
                        return sec.data();
                }
        };

        /**
         * Create a DWARF section loader backed by the given ELF
         * file.  This is templatized to eliminate a static dependency
         * between the libelf++ and libdwarf++, though it can only
         * reasonably be used with elf::elf from libelf++.
         */
        template<typename Elf>
        std::shared_ptr<elf_loader<Elf> > create_loader(const Elf &f)
        {
                return std::make_shared<elf_loader<Elf> >(f);
        }
};

DWARFPP_END_NAMESPACE

//////////////////////////////////////////////////////////////////
// Hash specializations
//

namespace std
{
        template<>
        struct hash<dwarf::unit>
        {
                typedef size_t result_type;
                typedef const dwarf::unit &argument_type;
                result_type operator()(argument_type a) const
                {
                        return hash<decltype(a.m)>()(a.m);
                }
        };

        template<>
        struct hash<dwarf::die>
        {
                typedef size_t result_type;
                typedef const dwarf::die &argument_type;
                result_type operator()(argument_type a) const;
        };
}

#endif
