#pragma once

#include "ustring.h"
#include "umap.h"
#include "Stabs2DebugInfo.h"


// The limit for function names, after that, they will get capped
#define CALL_FUNC_NAME_LIMIT 256
#define CALL_FUNC_NAME_LIMIT_STR macroToString(CALL_FUNC_NAME_LIMIT)

class SWEBDebugInfo : public Stabs2DebugInfo {
public:

    SWEBDebugInfo(char const *sweb_begin, char const *sweb_end);

    virtual ~SWEBDebugInfo();

    virtual void getCallNameAndLine(pointer address, const char *&mangled_name, ssize_t &line) const;

    virtual void printCallInformation(pointer address) const;

private:
    ustl::map<size_t, ustl::string> file_addrs_;
    ustl::map<size_t, const char*> function_defs_;

    virtual void initialiseSymbolTable();

};
