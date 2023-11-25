#include "PathWalker.h"
#include "Inode.h"
#include "Dentry.h"
#include "VfsMount.h"
#include "Superblock.h"
#include "assert.h"
#include "kstring.h"
#include "kprintf.h"
#include "FileSystemInfo.h"
#include "Path.h"
#ifndef EXE2MINIXFS
#include "Mutex.h"
#include "Thread.h"
#endif

#define CHAR_DOT '.'
#define NULL_CHAR '\0'
#define CHAR_ROOT '/'
#define SEPARATOR '/'



int32 PathWalker::pathWalk(const char* pathname, FileSystemInfo* fs_info, Path& out, Path* parent_dir)
{
  assert(fs_info);
  return pathWalk(pathname, fs_info->getPwd(), fs_info->getRoot(), out, parent_dir);
}

int32 PathWalker::pathWalk(const char* pathname, const Path& pwd, const Path& root, Path& out, Path* parent_dir)
{
  if ((pathname == 0) || (strlen(pathname) == 0))
  {
    debug(PATHWALKER, "pathWalk> ERROR: Invalid path name\n");
    return PW_EINVALID;
  }

  debug(PATHWALKER, "pathWalk> path: %s\n", pathname);

  if ((pwd.dentry_ == 0) || (pwd.mnt_ == 0) ||
      (root.dentry_ == 0) || (root.mnt_ == 0))
  {
      debug(PATHWALKER, "pathWalk> Error: Invalid pwd/root\n");
      return PW_EINVALID;
  }

  // Clear parent dir tracker
  if(parent_dir)
  {
    *parent_dir = Path();
  }

  // Start at ROOT if path starts with '/', else start with PWD
  out = (*pathname == CHAR_ROOT) ? root : pwd;
  debug(PATHWALKER, "PathWalk> Start dentry: %p, vfs_mount: %p\n", out.dentry_, out.mnt_);


  while (true)
  {
    while (*pathname == SEPARATOR)
      pathname++;

    if (!*pathname)
    {
      debug(PATHWALKER, "pathWalk> Reached end of path\n");
      break;
    }

    size_t segment_len = getNextPartLen(pathname);

    char segment[segment_len + 1];
    strncpy(segment, pathname, segment_len + 1);
    segment[segment_len] = 0;

    pathname += segment_len;

    while (*pathname == SEPARATOR)
        pathname++;


    debug(PATHWALKER, "pathWalk> segment: %s\n", segment);
    debug(PATHWALKER, "pathWalk> remaining: %s\n", pathname);

    switch(pathSegmentType(segment))
    {
    case LAST_DOT:
    {
        debug(PATHWALKER, "pathWalk> follow last dot\n");
        break;
    }
    case LAST_DOTDOT:
    {
        debug(PATHWALKER, "pathWalk> follow last dotdot\n");
        out = out.parent(&root);
        break;
    }
    case LAST_NORM:
    {
        debug(PATHWALKER, "pathWalk> follow last norm segment: %s\n", segment);

        Path child;
        if(out.child(segment, child) != PW_SUCCESS)
        {
            debug(PATHWALKER, "pathWalk> dentry %s not found\n", segment);
            if(!*pathname && parent_dir) // No further remaining segments -> parent directory exists
            {
                *parent_dir = out;
            }
            return PW_ENOTFOUND;
        }

        out = child;
        break;
    }
    default:
        assert(false);
    }
  }

  if(parent_dir)
  {
    *parent_dir = out.parent(&root);
  }
  return PW_SUCCESS;
}


int PathWalker::pathSegmentType(const char* segment)
{
    return (strcmp(segment, ".")  == 0) ? LAST_DOT    :
        (strcmp(segment, "..") == 0) ? LAST_DOTDOT :
        LAST_NORM;
}

size_t PathWalker::getNextPartLen(const char* path)
{
    const char* sep = strchr(path, SEPARATOR);
    return sep ? sep - path : strlen(path);
}


ustl::string PathWalker::pathPrefix(const ustl::string& path)
{
    ssize_t prefix_len = path.find_last_of("/");
    if(prefix_len == -1)
    {
        debug(PATHWALKER, "pathPrefix: %s -> %s\n", path.c_str(), "");
        return "";
    }

    ustl::string retval = path.substr(0, prefix_len);
    debug(PATHWALKER, "pathPrefix: %s -> %s\n", path.c_str(), retval.c_str());
    return retval;
}

ustl::string PathWalker::lastPathSegment(const ustl::string& path, bool ignore_separator_at_end)
{
    if(path.length() == 0)
        return path;

    if(!ignore_separator_at_end || path.back() != '/')
    {
        ssize_t prefix_len = path.find_last_of("/");
        ustl::string retval = path.substr(prefix_len+1, path.length() - prefix_len);
        debug(PATHWALKER, "lastPathSegment: %s -> %s\n", path.c_str(), retval.c_str());
        return retval;
    }
    else
    {
        ustl::string tmp_path = path.substr(0, path.find_last_not_of("/") + 1);
        ssize_t prefix_len = tmp_path.find_last_of("/");
        ustl::string retval = tmp_path.substr(prefix_len+1, tmp_path.length() - prefix_len);
        debug(PATHWALKER, "lastPathSegment: %s -> %s\n", path.c_str(), retval.c_str());
        return retval;
    }
}
