#include "dwarf++.hh"

#include <cstring>

using namespace std;

DWARFPP_BEGIN_NAMESPACE

static const struct
{
        const char *name;
        section_type type;
} sections[] = {
        {".debug_abbrev",   section_type::abbrev},
        {".debug_aranges",  section_type::aranges},
        {".debug_frame",    section_type::frame},
        {".debug_info",     section_type::info},
        {".debug_line",     section_type::line},
        {".debug_loc",      section_type::loc},
        {".debug_macinfo",  section_type::macinfo},
        {".debug_pubnames", section_type::pubnames},
        {".debug_pubtypes", section_type::pubtypes},
        {".debug_ranges",   section_type::ranges},
        {".debug_str",      section_type::str},
        {".debug_types",    section_type::types},
};

bool
elf::section_name_to_type(const char *name, section_type *out)
{
        for (auto &sec : sections) {
                if (strcmp(sec.name, name) == 0) {
                        *out = sec.type;
                        return true;
                }
        }
        return false;
}

const char *
elf::section_type_to_name(section_type type)
{
        for (auto &sec : sections) {
                if (sec.type == type)
                        return sec.name;
        }
        return nullptr;
}

DWARFPP_END_NAMESPACE
