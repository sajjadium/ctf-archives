#include "elf++.hh"
#include "dwarf++.hh"

#include <fcntl.h>
#include <stdio.h>
#include <string>
#include <algorithm>
#include <cxxabi.h>
#include <map>
#include <stdint.h>

using namespace std;

/*
 * Debug File Format
 *
 * Name               Len (bytes)
 * -----------------------------------------
 * id                 8
 *
 * - For each source file that has symbol infos in the binary:
 *
 * functions          2
 * filename_len       1
 * filename           filename_len
 *
 * - For each function of the source file:
 *
 * offset             8
 * line_entries       2
 * functionname_len   1
 * functionname       functionname_len
 *
 * - For each line of the source file:
 *
 * line_offset        2
 * line_number        2
 *
 */

struct MatchPathSeparator {
    bool operator()(char ch) const { return ch == '\\' || ch == '/'; }
};

string basename(string const &pathname) {
    return string(
            find_if(pathname.rbegin(), pathname.rend(), MatchPathSeparator()).base(),
            pathname.end());
}

struct Function {
    uint64_t start, end;
    string name;

    Function(uint64_t s, uint64_t e, string n) : start(s), end(e), name(n) {}

    Function() : start(0), end(0), name("") {}
};

#define WRITE_FIX(x, type, offset) do {*(type*) debug = (x); debug += sizeof(type) - (offset);} while(0);
#define WRITE(x, type) WRITE_FIX(x, type, 0);
#define TELL(type) (type*)debug

struct FileHeader {
    uint16_t functions;
    uint8_t filename_len;
    char filename[255];
} __attribute__((packed));

struct FunctionHeader {
    uint64_t offset;
    uint16_t line_entries;
    uint8_t name_len;
    char name[255];
} __attribute__((packed));

struct LineHeader {
    uint16_t offset;
    uint16_t number;
} __attribute__((packed));


int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s elf-file dbg-file\n", argv[0]);
        return 2;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "%s: %s\n", argv[1], strerror(errno));
        return 0;
    }
    FILE *d = fopen(argv[2], "wb");
    if (!d) return 0;

    char *debug = (char *) malloc(1024 * 1024);
    char *debug_start = debug;

    memcpy(debug, "SWEBDBG1", 8);
    debug += 8;

    map <string, map<uint64_t, int>> line_info;

    try {
        elf::elf ef(elf::create_mmap_loader(fd));
        dwarf::dwarf dw(dwarf::elf::create_loader(ef));

        for (auto cu : dw.compilation_units()) {
            const dwarf::line_table &lt = cu.get_line_table();

            // count entries
            uint32_t lines = 0;
            for (auto &line : lt) {
                (void) line;
                lines++;
            }
            if (!lines || lt.begin() == lt.end() || (begin(lt)->file) == 0)
              continue;

            string file(basename(begin(lt)->file->path));

            // get lines
            for (auto &line : lt) {
                if (!line.end_sequence) {
                    line_info[file][line.address] = line.line;
                }
            }
        }

        // look for symbol table
        for (auto &sec : ef.sections()) {
            if (sec.get_hdr().type != elf::sht::symtab && sec.get_hdr().type != elf::sht::dynsym)
                continue;

            // extract and demangle functions
            map <uint64_t, Function> fncs;
            map<uint64_t, bool> fnc_written;
            for (auto sym : sec.as_symtab()) {
                auto &d = sym.get_data();
                if (d.type() != elf::stt::func) continue;

                int status;
                char *realname = abi::__cxa_demangle(sym.get_name().c_str(), 0, 0, &status);
                string name;

                if (status == -2) {
                    name = sym.get_name();
                    realname = NULL;
                } else {
                    name = string(realname);
                }

                fncs[(uint64_t) d.value] = Function((uint64_t) d.value,
                                                    (uint64_t) d.value + (int) d.size, string(name));
                fnc_written[(uint64_t) d.value] = false;
                free(realname);
            }

            // get line infos for functions
            for (auto &info : line_info) {
                // write fileheader
                FileHeader fh;
                fh.functions = 0;
                fh.filename_len = info.first.size() <= 255 ? info.first.size() : 255;
                strncpy(fh.filename, info.first.c_str(), 255);
                FileHeader *fh_orig = TELL(FileHeader);
                WRITE_FIX(fh, FileHeader, 255 - fh.filename_len);

                int functions = 0;
                for (auto &f : fncs) {
                    Function &func = f.second;

                    bool found = false;
                    map<int, int> offsets;
                    for (auto &it : info.second) {
                        if (func.start <= it.first && func.end > it.first) {
                            offsets[(int) (it.first - func.start)] = it.second;
                            found = true;
                        }
                    }

                    if (found) {
                        // write function name + offset + entries
                        functions++;
                        FunctionHeader fnh;
                        fnh.offset = func.start;
                        fnh.line_entries = (uint16_t) offsets.size();
                        fnh.name_len = func.name.size() <= 254 ? func.name.size() + 1 : 255;
                        strncpy(fnh.name, func.name.c_str(), 255);
                        fnh.name[fnh.name_len] = 0;
                        WRITE_FIX(fnh, FunctionHeader, 255 - fnh.name_len);

                        // write line infos
                        for (auto &it : offsets) {
                            LineHeader lh;
                            lh.offset = (uint16_t) it.first;
                            lh.number = (uint16_t) it.second;
                            WRITE(lh, LineHeader);
                        }

                        fnc_written[f.first] = true;
                    }
                }
                fh_orig->functions = functions;

            }

            // functions where we couldn't get a file name
            map <uint64_t, Function> unwritten;
            for (auto &f : fncs) {
                if (!fnc_written[f.first]) unwritten[f.first] = f.second;
            }

            // write zero fileheader
            FileHeader fh;
            fh.functions = unwritten.size();
            fh.filename_len = 0;
            WRITE_FIX(fh, FileHeader, 255);

            // write functions without line information
            for (auto &u : unwritten) {
                FunctionHeader fnh;
                fnh.offset = u.second.start;
                fnh.line_entries = 0;
                fnh.name_len = u.second.name.size() <= 254 ? u.second.name.size() + 1 : 255;
                strncpy(fnh.name, u.second.name.c_str(), 255);
                fnh.name[fnh.name_len] = 0;
                WRITE_FIX(fnh, FunctionHeader, 255 - fnh.name_len);
            }

            fncs.clear();
        }

        //printf("Got %d bytes of debug info\n", (int) (debug - debug_start));
        fwrite(debug_start, debug - debug_start, 1, d);

    } catch (...) {
      printf("No debug infos for '%s' available (binary too small).\n",argv[1]);
    }

    fclose(d);
    return 0;
}
