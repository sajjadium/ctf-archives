#include "FileSystemInfo.h"
#include "Dentry.h"
#include "kstring.h"
#include "assert.h"

FileSystemInfo::FileSystemInfo() :
    root_(), pwd_()
{
}

FileSystemInfo::FileSystemInfo(const FileSystemInfo& fsi) :
    root_(fsi.root_),pwd_(fsi.pwd_)
{
}

FileSystemInfo::~FileSystemInfo()
{
}
