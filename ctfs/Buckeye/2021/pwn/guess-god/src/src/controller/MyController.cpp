#include "MyController.hpp"
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include "decompress.h"
#include <sys/types.h>
#include <sys/wait.h>

std::shared_ptr<oatpp::base::StrBuffer> MyController::get_file(int file_id, bool extract) {
  auto pair = std::make_pair(file_id, extract);
  
  lock.lock();
  if (fileCache.find(pair) != fileCache.end()) {
    lock.unlock();
    return fileCache[pair];
  }

  auto filename = fileMap[file_id].c_str();
  lock.unlock();

  std::ostringstream comp_fname;
  comp_fname << filename;
  if (extract) {
    // Want the un-kylezip-d version
    comp_fname << ".unkyle";
  }
  auto to_open = comp_fname.str();

  int fd = open(to_open.c_str(), O_RDONLY);
  if (fd == -1) {
      if (!extract) return NULL;

      /* Need to create decompressed version of file
       * Kyle gave me a buggy library so we are going to fork
       * in case we crash the web server will still stay up.
       */
      pid_t p = fork();
      if (p == 0) {
        decompress(filename);
        exit(0);
      } else {
        waitpid(p, NULL, 0);
      }


      fd = open(to_open.c_str(), O_RDONLY);
      if (fd == -1) {
        return NULL;
      }
  }

  struct stat sb;
  
  if (fstat(fd, &sb) != 0) {
      return NULL;
  }
  
  /* mmap the file in for performance, or something... idk kyle made me write this */
  
  void *mem = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (mem == NULL) return NULL;

  auto strbuf = oatpp::base::StrBuffer::createShared(mem, sb.st_size, false);
  
  lock.lock();
  fileCache[pair] = strbuf;
  lock.unlock();

  return strbuf;
}
