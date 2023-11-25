#include "internal.hh"

using namespace std;

DWARFPP_BEGIN_NAMESPACE

die::die(const unit *cu)
        : cu(cu), abbrev(nullptr)
{
}

const unit &
die::get_unit() const
{
        return *cu;
}

section_offset
die::get_section_offset() const
{
        return cu->get_section_offset() + offset;
}

void
die::read(section_offset off)
{
        cursor cur(cu->data(), off);

        offset = off;

        abbrev_code acode = cur.uleb128();
        if (acode == 0) {
                abbrev = nullptr;
                next = cur.get_section_offset();
                return;
        }
        abbrev = &cu->get_abbrev(acode);

        tag = abbrev->tag;

        // XXX We can pre-compute almost all of this work in the
        // abbrev_entry.
        attrs.clear();
        attrs.reserve(abbrev->attributes.size());
        for (auto &attr : abbrev->attributes) {
                attrs.push_back(cur.get_section_offset());
                cur.skip_form(attr.form);
        }
        next = cur.get_section_offset();
}

bool
die::has(DW_AT attr) const
{
        if (!abbrev)
                return false;
        // XXX Totally lame
        for (auto &a : abbrev->attributes)
                if (a.name == attr)
                        return true;
        return false;
}

value
die::operator[](DW_AT attr) const
{
        // XXX We can pre-compute almost all of this work in the
        // abbrev_entry.
        if (abbrev) {
                int i = 0;
                for (auto &a : abbrev->attributes) {
                        if (a.name == attr)
                                return value(cu, a.name, a.form, a.type, attrs[i]);
                        i++;
                }
        }
        throw out_of_range("DIE does not have attribute " + to_string(attr));
}

value
die::resolve(DW_AT attr) const
{
        // DWARF4 section 2.13, DWARF4 section 3.3.8

        // DWARF4 is unclear about what to do when there's both a
        // DW_AT::specification and a DW_AT::abstract_origin.
        // Conceptually, though, a concrete inlined instance cannot
        // itself complete an external function that wasn't first
        // completed by its abstract instance, so we first try to
        // resolve abstract_origin, then we resolve specification.

        // XXX This traverses the abbrevs at least twice and
        // potentially several more times

        if (has(attr))
                return (*this)[attr];

        if (has(DW_AT::abstract_origin)) {
                die ao = (*this)[DW_AT::abstract_origin].as_reference();
                if (ao.has(attr))
                        return ao[attr];
                if (ao.has(DW_AT::specification)) {
                        die s = ao[DW_AT::specification].as_reference();
                        if (s.has(attr))
                                return s[attr];
                }
        } else if (has(DW_AT::specification)) {
                die s = (*this)[DW_AT::specification].as_reference();
                if (s.has(attr))
                        return s[attr];
        }

        return value();
}

die::iterator
die::begin() const
{
        if (!abbrev || !abbrev->children)
                return end();
        return iterator(cu, next);
}

die::iterator::iterator(const unit *cu, section_offset off)
        : d(cu)
{
        d.read(off);
}

die::iterator &
die::iterator::operator++()
{
        if (!d.abbrev)
                return *this;

        if (!d.abbrev->children) {
                // The DIE has no children, so its successor follows
                // immediately
                d.read(d.next);
        } else if (d.has(DW_AT::sibling)) {
                // They made it easy on us.  Follow the sibling
                // pointer.  XXX Probably worth optimizing
                d = d[DW_AT::sibling].as_reference();
        } else {
                // It's a hard-knock life.  We have to iterate through
                // the children to find the next DIE.
                // XXX Particularly unfortunate if the user is doing a
                // DFS, since this will result in N^2 behavior.  Maybe
                // a small cache of terminator locations in the CU?
                iterator sub(d.cu, d.next);
                while (sub->abbrev)
                        ++sub;
                d.read(sub->next);
        }

        return *this;
}

const vector<pair<DW_AT, value> >
die::attributes() const
{
        vector<pair<DW_AT, value> > res;

        if (!abbrev)
                return res;

        // XXX Quite slow, especially when using this to traverse an
        // entire DIE tree since each DIE will produce a new vector
        // (whereas other vectors get reused).  Might be worth a
        // custom iterator.
        int i = 0;
        for (auto &a : abbrev->attributes) {
                res.push_back(make_pair(a.name, value(cu, a.name, a.form, a.type, attrs[i])));
                i++;
        }
        return res;
}

bool
die::operator==(const die &o) const
{
        return cu == o.cu && offset == o.offset;
}

bool
die::operator!=(const die &o) const
{
        return !(*this == o);
}

DWARFPP_END_NAMESPACE

size_t
std::hash<dwarf::die>::operator()(const dwarf::die &a) const
{
        return hash<decltype(a.cu)>()(a.cu) ^
                hash<decltype(a.get_unit_offset())>()(a.get_unit_offset());
}
