#include <ustl/ustring.h>
#include "kprintf.h"
#include "SWEBDebugInfo.h"
#include "Stabs2DebugInfo.h"
#include "ArchCommon.h"
#include "ArchMemory.h"


struct FileHeader {
    uint16_t functions;
    uint8_t filename_len;
} __attribute__((packed));

struct FunctionHeader {
    uint64_t offset;
    uint16_t line_entries;
    uint8_t name_len;
} __attribute__((packed));

struct LineHeader {
    uint16_t offset;
    uint16_t number;
} __attribute__((packed));


SWEBDebugInfo::SWEBDebugInfo(char const *sweb_start, char const *sweb_end) : Stabs2DebugInfo(sweb_start, sweb_end, 0) {
  if (sweb_start != 0 && sweb_end != 0)
    initialiseSymbolTable();
}

SWEBDebugInfo::~SWEBDebugInfo() {
}


void SWEBDebugInfo::initialiseSymbolTable() {
    function_defs_.reserve(256);
    file_addrs_.reserve(256);

    char *data = (char *) stab_start_ + 8;

    char buffer[256];
    do {
        FileHeader *fh = (FileHeader *) data;
        data += sizeof(FileHeader);
        strncpy(buffer, data, fh->filename_len);
        buffer[fh->filename_len] = 0;
        data += fh->filename_len;
        ustl::string filename(buffer);

        for(int fn = 0; fn < fh->functions; fn++) {
            FunctionHeader* fnh = (FunctionHeader*)data;
            if(fn == 0) {
                file_addrs_[fnh->offset] = filename;
            }
            function_defs_[fnh->offset] = data;
            data += sizeof(FunctionHeader);
            data += fnh->name_len;
            data += fnh->line_entries * sizeof(LineHeader);
        }

    } while(data != (char*)stab_end_);

    debug(USERTRACE, "found %zd sweb debug functions\n", function_defs_.size());

}

void SWEBDebugInfo::getCallNameAndLine(pointer address, const char *&name, ssize_t &line) const {
    name = "UNKNOWN FUNCTION";
    line = 0;

    if (!this || function_defs_.size() == 0)
        return;

    FunctionHeader* fh = 0;
    for(auto f : function_defs_) {
      if (address >= f.first)
        fh = (FunctionHeader*)f.second;
    }
    if (fh == 0)
      return;

    name = ((char*)fh) + sizeof(FunctionHeader);

    LineHeader* lh = (LineHeader*)((char*)(fh + 1) + fh->name_len);
    bool found = false;
    for(int e = 0; e < fh->line_entries; e++) {
        if(address < fh->offset + lh->offset) {
            lh--;
            found = true;
            break;
        } else if(address == fh->offset + lh->offset) {
            found = true;
            break;
        }
        lh++;
    }

    line = found ? lh->number : -(int)(address - fh->offset);
}


void SWEBDebugInfo::printCallInformation(pointer address) const {
    const char *name;
    ssize_t line;
    getCallNameAndLine(address, name, line);
    if (line >= 0) {
        kprintfd("%10zx: %." CALL_FUNC_NAME_LIMIT_STR "s:%zu \n", address, name, line );
    }
    else {
        kprintfd("%10zx: %." CALL_FUNC_NAME_LIMIT_STR "s+%zx\n", address, name, -line);
    }
}
