#pragma once

#include "types.h"
#include "ustring.h"
#include "Path.h"

class Dentry;
class VfsMount;

class FileSystemInfo
{
  protected:
    /**
     * File system root
     */
    Path root_;

    /**
     * Current working directory
     */
    Path pwd_;


  public:
    FileSystemInfo();
    ~FileSystemInfo();
    FileSystemInfo(const FileSystemInfo& fsi);

    /**
     * set the ROOT-info to the class
     * @param root the root path to set
     */
    void setRoot(const Path& path)
    {
      root_ = path;
    }

    /**
     * set the PWD-info to the class (PWD: print working directory)
     * @param path the current path to set
     */
    void setPwd(const Path& path)
    {
      pwd_ = path;
    }

    /**
     * get the ROOT-info (ROOT-directory) from the class
     * @return the root path
     */
    Path& getRoot()
    {
      return root_;
    }

    /**
     * get the PWD-info (PWD-directory) from the class
     * @return the path of the current directory
     */
    Path& getPwd()
    {
      return pwd_;
    }
};

extern FileSystemInfo* default_working_dir;
// you use a different getcwd() method depending on where your cpp is being compiled
//   (it can come either from Thread.cpp or from exe2minixfs.cpp)
FileSystemInfo* getcwd();

