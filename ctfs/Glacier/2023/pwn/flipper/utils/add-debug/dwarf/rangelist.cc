#include "internal.hh"

using namespace std;

DWARFPP_BEGIN_NAMESPACE

rangelist::rangelist(const std::shared_ptr<section> &sec, section_offset off,
                     unsigned cu_addr_size, taddr cu_low_pc)
        : sec(sec->slice(off, ~0, format::unknown, cu_addr_size)),
          base_addr(cu_low_pc)
{
}

rangelist::rangelist(const initializer_list<pair<taddr, taddr> > &ranges)
{
        synthetic.reserve(ranges.size() * 2 + 2);
        for (auto &range : ranges) {
                synthetic.push_back(range.first);
                synthetic.push_back(range.second);
        }
        synthetic.push_back(0);
        synthetic.push_back(0);

        sec = make_shared<section>(
                section_type::ranges, (const char*)synthetic.data(),
                synthetic.size() * sizeof(taddr), format::unknown,
                sizeof(taddr));

        base_addr = 0;
}

rangelist::iterator
rangelist::begin() const
{
        if (sec)
                return iterator(sec, base_addr);
        return end();
}

rangelist::iterator
rangelist::end() const
{
        return iterator();
}

bool
rangelist::contains(taddr addr) const
{
        for (auto ent : *this)
                if (ent.contains(addr))
                        return true;
        return false;
}

rangelist::iterator::iterator(const std::shared_ptr<section> &sec, taddr base_addr)
        : sec(sec), base_addr(base_addr), pos(0)
{
        // Read in the first entry
        ++(*this);
}

rangelist::iterator &
rangelist::iterator::operator++()
{
        // DWARF4 section 2.17.3
        taddr largest_offset = ~(taddr)0;
        if (sec->addr_size < sizeof(taddr))
                largest_offset += 1 << (8 * sec->addr_size);

        // Read in entries until we reach a regular entry of an
        // end-of-list.  Note that pos points to the beginning of the
        // entry *following* the current entry, so that's where we
        // start.
        cursor cur(sec, pos);
        while (true) {
                entry.low = cur.address();
                entry.high = cur.address();

                if (entry.low == 0 && entry.high == 0) {
                        // End of list
                        sec.reset();
                        pos = 0;
                        break;
                } else if (entry.low == largest_offset) {
                        // Base address change
                        base_addr = entry.high;
                } else {
                        // Regular entry.  Adjust by base address.
                        entry.low += base_addr;
                        entry.high += base_addr;
                        pos = cur.get_section_offset();
                        break;
                }
        }

        return *this;
}

DWARFPP_END_NAMESPACE
