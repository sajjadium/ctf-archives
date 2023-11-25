#pragma once

#include "types.h"
#include "ustring.h"

class Dentry;
class VfsMount;
class Path;
class FileSystemInfo;

/**
 * @enum Type of the last component on LOOKUP_PARENT
 */
enum
{
  /**
   * The last component is a regular filename
   */
  LAST_NORM,

  /**
   * The last component is "."
   */
  LAST_DOT,

  /**
   * The last component is ".."
   */
  LAST_DOTDOT,
};

/**
 * @enum Error Codes for the path walk
 */
enum
{
  PW_SUCCESS = 0,
  /**
   * The path was not found
   */
  PW_ENOTFOUND,
  /**
   * The path to look up is invalid
   */
  PW_EINVALID
};

class PathWalker
{
  public:

    /**
     * Perform a file system lookup
     * @param pathname File pathname to be resolved
     * @param pwd Start directory of the file system walk
     * @param root Root directory for the file system walk
     * @param out Output parameter: Found file path
     * @param parent Optional output parameter: Parent directory
     * @return Returns 0 on success, != 0 on error
     */
    static int32 pathWalk(const char* pathname, const Path& pwd, const Path& root, Path& out, Path* parent = nullptr);

    static int32 pathWalk(const char* pathname, FileSystemInfo* fs_info, Path& out, Path* parent_dir = nullptr);

    static ustl::string pathPrefix(const ustl::string& path);
    static ustl::string lastPathSegment(const ustl::string& path, bool ignore_separator_at_end = false);

  private:
    static size_t getNextPartLen(const char* path);
    static int pathSegmentType(const char* segment);

    PathWalker();
    ~PathWalker();
};


