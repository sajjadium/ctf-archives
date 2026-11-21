#include "internal.hh"

using namespace std;

DWARFPP_BEGIN_NAMESPACE

static value::type
resolve_type(DW_AT name, DW_FORM form)
{
        switch (form) {
        case DW_FORM::addr:
                return value::type::address;

        case DW_FORM::block:
        case DW_FORM::block1:
        case DW_FORM::block2:
        case DW_FORM::block4:
                // Prior to DWARF 4, exprlocs didn't have their own
                // form and were represented as blocks.
                // XXX Should this be predicated on version?
                switch (name) {
                case DW_AT::location:
                case DW_AT::byte_size:
                case DW_AT::bit_offset:
                case DW_AT::bit_size:
                case DW_AT::string_length:
                case DW_AT::lower_bound:
                case DW_AT::return_addr:
                case DW_AT::bit_stride:
                case DW_AT::upper_bound:
                case DW_AT::count:
                case DW_AT::data_member_location:
                case DW_AT::frame_base:
                case DW_AT::segment:
                case DW_AT::static_link:
                case DW_AT::use_location:
                case DW_AT::vtable_elem_location:
                case DW_AT::allocated:
                case DW_AT::associated:
                case DW_AT::data_location:
                case DW_AT::byte_stride:
                        return value::type::exprloc;
                default:
                        return value::type::block;
                }

        case DW_FORM::data4:
        case DW_FORM::data8:
                // Prior to DWARF 4, section offsets didn't have their
                // own form and were represented as data4 or data8.
                // DWARF 3 clarified that types that accepted both
                // constants and section offsets were to treat data4
                // and data8 as section offsets and other constant
                // forms as constants.
                // XXX Should this be predicated on version?
                switch (name) {
                case DW_AT::location:
                case DW_AT::stmt_list:
                case DW_AT::string_length:
                case DW_AT::return_addr:
                case DW_AT::start_scope:
                case DW_AT::data_member_location:
                case DW_AT::frame_base:
                case DW_AT::macro_info:
                case DW_AT::segment:
                case DW_AT::static_link:
                case DW_AT::use_location:
                case DW_AT::vtable_elem_location:
                case DW_AT::ranges:
                        goto sec_offset;
                default:
                        // fallthrough
                        break;
                } // fallthrough
        case DW_FORM::data1:
        case DW_FORM::data2:
                return value::type::constant;
        case DW_FORM::udata:
                return value::type::uconstant;
        case DW_FORM::sdata:
                return value::type::sconstant;

        case DW_FORM::exprloc:
                return value::type::exprloc;

        case DW_FORM::flag:
        case DW_FORM::flag_present:
                return value::type::flag;

        case DW_FORM::ref1:
        case DW_FORM::ref2:
        case DW_FORM::ref4:
        case DW_FORM::ref8:
        case DW_FORM::ref_addr:
        case DW_FORM::ref_sig8:
        case DW_FORM::ref_udata:
                return value::type::reference;

        case DW_FORM::string:
        case DW_FORM::strp:
                return value::type::string;

        case DW_FORM::indirect:
                // There's nothing meaningful we can do
                return value::type::invalid;

        case DW_FORM::sec_offset:
        sec_offset:
                // The type of this form depends on the attribute
                switch (name) {
                case DW_AT::stmt_list:
                        return value::type::line;

                case DW_AT::location:
                case DW_AT::string_length:
                case DW_AT::return_addr:
                case DW_AT::data_member_location:
                case DW_AT::frame_base:
                case DW_AT::segment:
                case DW_AT::static_link:
                case DW_AT::use_location:
                case DW_AT::vtable_elem_location:
                        return value::type::loclist;

                case DW_AT::macro_info:
                        return value::type::mac;

                case DW_AT::start_scope:
                case DW_AT::ranges:
                        return value::type::rangelist;

                default:
                        throw format_error("DW_FORM_sec_offset not expected for attribute " +
                                           to_string(name));
                }
        }
        throw format_error("unknown attribute form " + to_string(form));
}

attribute_spec::attribute_spec(DW_AT name, DW_FORM form)
        : name(name), form(form), type(resolve_type(name, form))
{
}

bool
abbrev_entry::read(cursor *cur)
{
        attributes.clear();

        // Section 7.5.3
        code = cur->uleb128();
        if (!code)
                return false;

        tag = (DW_TAG)cur->uleb128();
        children = cur->fixed<DW_CHILDREN>() == DW_CHILDREN::yes;
        while (1) {
                DW_AT name = (DW_AT)cur->uleb128();
                DW_FORM form = (DW_FORM)cur->uleb128();
                if (name == (DW_AT)0 && form == (DW_FORM)0)
                        break;
                attributes.push_back(attribute_spec(name, form));
        }
        attributes.shrink_to_fit();
        return true;
}

DWARFPP_END_NAMESPACE
