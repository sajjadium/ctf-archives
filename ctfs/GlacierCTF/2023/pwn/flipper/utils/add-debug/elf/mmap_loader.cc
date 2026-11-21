#include "elf++.hh"

#include <system_error>

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

using namespace std;

ELFPP_BEGIN_NAMESPACE

class mmap_loader : public loader
{
        void *base;
        size_t lim;

public:
        mmap_loader(int fd)
        {
                off_t end = lseek(fd, 0, SEEK_END);
                if (end == (off_t)-1)
                        throw system_error(errno, system_category(),
                                           "finding file length");
                lim = end;

                base = mmap(nullptr, lim, PROT_READ, MAP_SHARED, fd, 0);
                if (base == MAP_FAILED)
                        throw system_error(errno, system_category(),
                                           "mmap'ing file");
                close(fd);
        }

        ~mmap_loader()
        {
                munmap(base, lim);
        }

        const void *load(off_t offset, size_t size)
        {
                if (offset + size > lim)
                        throw range_error("offset exceeds file size");
                return (const char*)base + offset;
        }
};

std::shared_ptr<loader>
create_mmap_loader(int fd)
{
        return make_shared<mmap_loader>(fd);
}

ELFPP_END_NAMESPACE
