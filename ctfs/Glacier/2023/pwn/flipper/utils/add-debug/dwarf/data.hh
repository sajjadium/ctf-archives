#ifndef _DWARFPP_DW_HH_
#define _DWARFPP_DW_HH_

#include <cstdint>
#include <string>

DWARFPP_BEGIN_NAMESPACE

// Integer representations (Section 7.26)
typedef std::int8_t sbyte;
typedef std::uint8_t ubyte;
typedef std::uint16_t uhalf;
typedef std::uint32_t uword;

// Section offsets and lengths
typedef std::uint64_t section_offset;
typedef std::uint64_t section_length;

// A target machine address.  Targets may use smaller addresses; this
// represents the largest supported address type.
typedef std::uint64_t taddr;

// DIE tags (Section 7, figure 18).  typedef, friend, and namespace
// have a trailing underscore because they are reserved words.
enum class DW_TAG
{
        array_type               = 0x01,
        class_type               = 0x02,
        entry_point              = 0x03,
        enumeration_type         = 0x04,
        formal_parameter         = 0x05,
        imported_declaration     = 0x08,
        label                    = 0x0a,
        lexical_block            = 0x0b,
        member                   = 0x0d,
        pointer_type             = 0x0f,
        reference_type           = 0x10,
        compile_unit             = 0x11,
        string_type              = 0x12,
        structure_type           = 0x13,
        subroutine_type          = 0x15,
        typedef_                 = 0x16,

        union_type               = 0x17,
        unspecified_parameters   = 0x18,
        variant                  = 0x19,
        common_block             = 0x1a,
        common_inclusion         = 0x1b,
        inheritance              = 0x1c,
        inlined_subroutine       = 0x1d,
        module                   = 0x1e,
        ptr_to_member_type       = 0x1f,
        set_type                 = 0x20,
        subrange_type            = 0x21,
        with_stmt                = 0x22,
        access_declaration       = 0x23,
        base_type                = 0x24,
        catch_block              = 0x25,
        const_type               = 0x26,
        constant                 = 0x27,
        enumerator               = 0x28,
        file_type                = 0x29,
        friend_                  = 0x2a,

        namelist                 = 0x2b,
        namelist_item            = 0x2c,
        packed_type              = 0x2d,
        subprogram               = 0x2e,
        template_type_parameter  = 0x2f,
        template_value_parameter = 0x30,
        thrown_type              = 0x31,
        try_block                = 0x32,
        variant_part             = 0x33,
        variable                 = 0x34,
        volatile_type            = 0x35,
        dwarf_procedure          = 0x36,
        restrict_type            = 0x37,
        interface_type           = 0x38,
        namespace_               = 0x39,
        imported_module          = 0x3a,
        unspecified_type         = 0x3b,
        partial_unit             = 0x3c,
        imported_unit            = 0x3d,
        condition                = 0x3f,

        shared_type              = 0x40,
        type_unit                = 0x41,
        rvalue_reference_type    = 0x42,
        template_alias           = 0x43,
        lo_user                  = 0x4080,
        hi_user                  = 0xffff,
};

std::string
to_string(DW_TAG v);

// Child determination (Section 7, figure 19).
enum class DW_CHILDREN : ubyte
{
        no  = 0x00,
        yes = 0x01,
};

std::string
to_string(DW_CHILDREN v);

// Attribute names (Section 7, figure 20).  inline, friend, mutable,
// and explicit have a trailing underscore because they are reserved
// words.
enum class DW_AT
{
        sibling              = 0x01, // reference
        location             = 0x02, // exprloc, loclistptr
        name                 = 0x03, // string
        ordering             = 0x09, // constant
        byte_size            = 0x0b, // constant, exprloc, reference
        bit_offset           = 0x0c, // constant, exprloc, reference
        bit_size             = 0x0d, // constant, exprloc, reference
        stmt_list            = 0x10, // lineptr
        low_pc               = 0x11, // address
        high_pc              = 0x12, // address, constant
        language             = 0x13, // constant
        discr                = 0x15, // reference
        discr_value          = 0x16, // constant
        visibility           = 0x17, // constant
        import               = 0x18, // reference
        string_length        = 0x19, // exprloc, loclistptr
        common_reference     = 0x1a, // reference
        comp_dir             = 0x1b, // string
        const_value          = 0x1c, // block, constant, string

        containing_type      = 0x1d, // reference
        default_value        = 0x1e, // reference
        inline_              = 0x20, // constant
        is_optional          = 0x21, // flag
        lower_bound          = 0x22, // constant, exprloc, reference
        producer             = 0x25, // string
        prototyped           = 0x27, // flag
        return_addr          = 0x2a, // exprloc, loclistptr
        start_scope          = 0x2c, // constant, rangelistptr
        bit_stride           = 0x2e, // constant, exprloc, reference
        upper_bound          = 0x2f, // constant, exprloc, reference
        abstract_origin      = 0x31, // reference
        accessibility        = 0x32, // constant
        address_class        = 0x33, // constant
        artificial           = 0x34, // flag
        base_types           = 0x35, // reference
        calling_convention   = 0x36, // constant
        count                = 0x37, // constant, exprloc, reference
        data_member_location = 0x38, // constant, exprloc, loclistptr
        decl_column          = 0x39, // constant

        decl_file            = 0x3a, // constant
        decl_line            = 0x3b, // constant
        declaration          = 0x3c, // flag
        discr_list           = 0x3d, // block
        encoding             = 0x3e, // constant
        external             = 0x3f, // flag
        frame_base           = 0x40, // exprloc, loclistptr
        friend_              = 0x41, // reference
        identifier_case      = 0x42, // constant
        macro_info           = 0x43, // macptr
        namelist_item        = 0x44, // reference
        priority             = 0x45, // reference
        segment              = 0x46, // exprloc, loclistptr
        specification        = 0x47, // reference
        static_link          = 0x48, // exprloc, loclistptr
        type                 = 0x49, // reference
        use_location         = 0x4a, // exprloc, loclistptr
        variable_parameter   = 0x4b, // flag
        virtuality           = 0x4c, // constant
        vtable_elem_location = 0x4d, // exprloc, loclistptr

        // DWARF 3
        allocated            = 0x4e, // constant, exprloc, reference
        associated           = 0x4f, // constant, exprloc, reference
        data_location        = 0x50, // exprloc
        byte_stride          = 0x51, // constant, exprloc, reference
        entry_pc             = 0x52, // address
        use_UTF8             = 0x53, // flag
        extension            = 0x54, // reference
        ranges               = 0x55, // rangelistptr
        trampoline           = 0x56, // address, flag, reference, string
        call_column          = 0x57, // constant
        call_file            = 0x58, // constant
        call_line            = 0x59, // constant
        description          = 0x5a, // string
        binary_scale         = 0x5b, // constant
        decimal_scale        = 0x5c, // constant
        small                = 0x5d, // reference
        decimal_sign         = 0x5e, // constant
        digit_count          = 0x5f, // constant
        picture_string       = 0x60, // string
        mutable_             = 0x61, // flag

        threads_scaled       = 0x62, // flag
        explicit_            = 0x63, // flag
        object_pointer       = 0x64, // reference
        endianity            = 0x65, // constant
        elemental            = 0x66, // flag
        pure                 = 0x67, // flag
        recursive            = 0x68, // flag

        // DWARF 4
        signature            = 0x69, // reference
        main_subprogram      = 0x6a, // flag
        data_bit_offset      = 0x6b, // constant
        const_expr           = 0x6c, // flag
        enum_class           = 0x6d, // flag
        linkage_name         = 0x6e, // string

        lo_user              = 0x2000,
        hi_user              = 0x3fff,
};

std::string
to_string(DW_AT v);

// Attribute form encodings (Section 7, figure 21)
enum class DW_FORM
{
        addr         = 0x01,    // address
        block2       = 0x03,    // block
        block4       = 0x04,    // block
        data2        = 0x05,    // constant
        data4        = 0x06,    // constant
        data8        = 0x07,    // constant
        string       = 0x08,    // string
        block        = 0x09,    // block
        block1       = 0x0a,    // block
        data1        = 0x0b,    // constant
        flag         = 0x0c,    // flag
        sdata        = 0x0d,    // constant
        strp         = 0x0e,    // string
        udata        = 0x0f,    // constant
        ref_addr     = 0x10,    // reference
        ref1         = 0x11,    // reference
        ref2         = 0x12,    // reference
        ref4         = 0x13,    // reference
        ref8         = 0x14,    // reference

        ref_udata    = 0x15,    // reference
        indirect     = 0x16,    // (Section 7.5.3)

        // DWARF 4
        sec_offset   = 0x17,    // lineptr, loclistptr, macptr, rangelistptr
        exprloc      = 0x18,    // exprloc
        flag_present = 0x19,    // flag
        ref_sig8     = 0x20,    // reference
};

std::string
to_string(DW_FORM v);

// DWARF operation encodings (Section 7.7.1 and figure 24)
enum class DW_OP : ubyte
{
        addr                = 0x03, // [constant address (size target specific)]
        deref               = 0x06,

        const1u             = 0x08, // [1-byte constant]
        const1s             = 0x09, // [1-byte constant]
        const2u             = 0x0a, // [2-byte constant]
        const2s             = 0x0b, // [2-byte constant]
        const4u             = 0x0c, // [4-byte constant]
        const4s             = 0x0d, // [4-byte constant]
        const8u             = 0x0e, // [8-byte constant]
        const8s             = 0x0f, // [8-byte constant]
        constu              = 0x10, // [ULEB128 constant]
        consts              = 0x11, // [SLEB128 constant]
        dup                 = 0x12,
        drop                = 0x13,
        over                = 0x14,
        pick                = 0x15, // [1-byte stack index]
        swap                = 0x16,
        rot                 = 0x17,
        xderef              = 0x18,
        abs                 = 0x19,
        and_                = 0x1a,
        div                 = 0x1b,

        minus               = 0x1c,
        mod                 = 0x1d,
        mul                 = 0x1e,
        neg                 = 0x1f,
        not_                = 0x20,
        or_                 = 0x21,
        plus                = 0x22,
        plus_uconst         = 0x23, // [ULEB128 addend]
        shl                 = 0x24,
        shr                 = 0x25,
        shra                = 0x26,
        xor_                = 0x27,
        skip                = 0x2f, // [signed 2-byte constant]
        bra                 = 0x28, // [signed 2-byte constant]
        eq                  = 0x29,
        ge                  = 0x2a,
        gt                  = 0x2b,
        le                  = 0x2c,
        lt                  = 0x2d,
        ne                  = 0x2e,

        // Literals 0..31 = (lit0 + literal)
        lit0                = 0x30,
        lit31               = 0x4f,

        // Registers 0..31 = (reg0 + regnum)
        reg0                = 0x50,
        reg31               = 0x6f,

        // Base register 0..31 = (breg0 + regnum)
        breg0               = 0x70, // [SLEB128 offset]
        breg31              = 0x8f, // [SLEB128 offset]

        regx                = 0x90, // [ULEB128 register]
        fbreg               = 0x91, // [SLEB128 offset]
        bregx               = 0x92, // [ULEB128 register, SLEB128 offset]
        piece               = 0x93, // [ULEB128 size of piece addressed]
        deref_size          = 0x94, // [1-byte size of data retrieved]
        xderef_size         = 0x95, // [1-byte size of data retrieved]
        nop                 = 0x96,

        // DWARF 3
        push_object_address = 0x97,
        call2               = 0x98, // [2-byte offset of DIE]
        call4               = 0x99, // [4-byte offset of DIE]
        call_ref            = 0x9a, // [4- or 8-byte offset of DIE]
        form_tls_address    = 0x9b,
        call_frame_cfa      = 0x9c,
        bit_piece           = 0x9d, // [ULEB128 size, ULEB128 offset]

        // DWARF 4
        implicit_value      = 0x9e, // [ULEB128 size, block of that size]
        stack_value         = 0x9f,

        lo_user             = 0xe0,
        hi_user             = 0xff,
};

std::string
to_string(DW_OP v);

// DW_AT::encoding constants (DWARF4 section 7.8 figure 25)
enum class DW_ATE
{
        address         = 0x01,
        boolean         = 0x02,
        complex_float   = 0x03,
        float_          = 0x04,
        signed_         = 0x05,
        signed_char     = 0x06,
        unsigned_       = 0x07,
        unsigned_char   = 0x08,
        imaginary_float = 0x09,
        packed_decimal  = 0x0a,
        numeric_string  = 0x0b,
        edited          = 0x0c,
        signed_fixed    = 0x0d,
        unsigned_fixed  = 0x0e,
        decimal_float   = 0x0f,

        // DWARF 4
        UTF             = 0x10,

        lo_user         = 0x80,
        hi_user         = 0xff,
};

std::string
to_string(DW_ATE v);

// DW_AT::decimal_sign constants (DWARF4 section 7.8 figure 26)
enum class DW_DS
{
        unsigned_          = 0x01,
        leading_overpunch  = 0x02,
        trailing_overpunch = 0x03,
        leading_separate   = 0x04,
        trailing_separate  = 0x05,
};

std::string
to_string(DW_DS v);

// DW_AT::endianity constants (DWARF4 section 7.8 figure 27)
enum class DW_END
{
        default_ = 0x00,
        big      = 0x01,
        little   = 0x02,
        lo_user  = 0x40,
        hi_user  = 0xff,
};

std::string
to_string(DW_END v);

// DW_AT::accessibility constants (DWARF4 section 7.9 figure 28)
enum class DW_ACCESS
{
        public_    = 0x01,
        protected_ = 0x02,
        private_   = 0x03,
};

std::string
to_string(DW_ACCESS v);

// DW_AT::visibility constants (DWARF4 section 7.10 figure 29)
enum class DW_VIS
{
        local     = 0x01,
        exported  = 0x02,
        qualified = 0x03,
};

std::string
to_string(DW_VIS v);

// DW_AT::virtuality constants (DWARF4 section 7.11 figure 30)
enum class DW_VIRTUALITY
{
        none         = 0x00,
        virtual_     = 0x01,
        pure_virtual = 0x02,
};

std::string
to_string(DW_VIRTUALITY v);

// DW_AT::language constants (DWARF4 section 7.12 figure 31)
enum class DW_LANG
{
        C89            = 0x0001, // Lower bound 0
        C              = 0x0002, // Lower bound 0
        Ada83          = 0x0003, // Lower bound 1
        C_plus_plus    = 0x0004, // Lower bound 0
        Cobol74        = 0x0005, // Lower bound 1
        Cobol85        = 0x0006, // Lower bound 1
        Fortran77      = 0x0007, // Lower bound 1
        Fortran90      = 0x0008, // Lower bound 1
        Pascal83       = 0x0009, // Lower bound 1
        Modula2        = 0x000a, // Lower bound 1
        Java           = 0x000b, // Lower bound 0
        C99            = 0x000c, // Lower bound 0
        Ada95          = 0x000d, // Lower bound 1
        Fortran95      = 0x000e, // Lower bound 1
        PLI            = 0x000f, // Lower bound 1

        ObjC           = 0x0010, // Lower bound 0
        ObjC_plus_plus = 0x0011, // Lower bound 0
        UPC            = 0x0012, // Lower bound 0
        D              = 0x0013, // Lower bound 0
        Python         = 0x0014, // Lower bound 0
        lo_user        = 0x8000,
        hi_user        = 0xffff,
};

std::string
to_string(DW_LANG v);

// DW_AT::identifier_case constants (DWARF4 section 7.14 figure 32)
enum class DW_ID
{
        case_sensitive   = 0x00,
        up_case          = 0x01,
        down_case        = 0x02,
        case_insensitive = 0x03,
};

std::string
to_string(DW_ID v);

// DW_AT::calling_convention constants (DWARF4 section 7.15 figure 33)
enum class DW_CC
{
        normal = 0x01,
        program = 0x02,
        nocall = 0x03,
        lo_user = 0x40,
        hi_user = 0xff,
};

std::string
to_string(DW_CC v);

// DW_AT::inline constants (DWARF4 section 7.16 figure 34)
enum class DW_INL
{
        not_inlined = 0x00,
        inlined = 0x01,
        declared_not_inlined = 0x02,
        declared_inlined = 0x03,
};

std::string
to_string(DW_INL v);

// DW_AT::ordering constants (DWARF4 section 7.17 figure 35)
enum class DW_ORD
{
        row_major = 0x00,
        col_major = 0x01,
};

std::string
to_string(DW_ORD v);

// DW_AT::discr_list constants (DWARF4 section 7.18 figure 36)
enum class DW_DSC
{
        label = 0x00,
        range = 0x01,
};

std::string
to_string(DW_DSC v);

// Line number standard opcodes (DWARF4 section 7.21 figure 37)
enum class DW_LNS
{
        copy = 0x01,
        advance_pc = 0x02,
        advance_line = 0x03,
        set_file = 0x04,
        set_column = 0x05,
        negate_stmt = 0x06,
        set_basic_block = 0x07,
        const_add_pc = 0x08,
        fixed_advance_pc = 0x09,

        // DWARF 3
        set_prologue_end = 0x0a,
        set_epilogue_begin = 0x0b,
        set_isa = 0x0c,
};

std::string
to_string(DW_LNS v);

// Line number extended opcodes (DWARF4 section 7.21 figure 38)
enum class DW_LNE
{
        end_sequence = 0x01,
        set_address = 0x02,
        define_file = 0x03,

        // DWARF 4
        set_discriminator = 0x04,

        // DWARF 3
        lo_user = 0x80,
        hi_user = 0xff,
};

std::string
to_string(DW_LNE v);

DWARFPP_END_NAMESPACE

#endif
