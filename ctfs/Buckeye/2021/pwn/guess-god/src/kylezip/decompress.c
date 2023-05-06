#include <sys/mman.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

static int verify_file(char *in);
static uint64_t get_fsize(char *in);
static void do_decompress(char *out, char *in, size_t insize);

/* I got tired of C++ so I wrote this in C */
int decompress(const char *fname) {
  char resultName[100];

  strcpy(resultName, fname);
  strcat(resultName, ".unkyle");
  
  int infd = open(fname, O_RDONLY);
  int outfd = open(resultName, O_RDWR|O_CREAT, 0644);
  
  struct stat insb;
  
  if (infd == -1 || outfd == -1) {
    fprintf(stderr, "Failed to open infile or outfile\n");
    return -1;
  }

  if (fstat(infd, &insb) != 0) {
    fprintf(stderr, "Failed to stat infile\n");
    return -1;          
  }
    
  /* kyle wanted this mapped at his favorite address */ 
  void *from_mem = mmap((void*)0x42069000000, insb.st_size, PROT_READ, MAP_SHARED|MAP_FIXED, infd, 0);
  if (from_mem == MAP_FAILED || !verify_file(from_mem)) {
    fprintf(stderr, "mmap failed or didn't verify %p\n", from_mem);
    return -1;
  }

  size_t outsize = get_fsize(from_mem);
  ftruncate(outfd, outsize);
  void *to_mem = mmap((void*)0x13371337000, outsize, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_FIXED, outfd, 0);

  if (to_mem == MAP_FAILED) {
    fprintf(stderr, "mmap failed 2\n");
    return -1;
  }

  do_decompress(to_mem, from_mem, insb.st_size);
  
  return 0;
}

static int verify_file(char *in) {
    if (*(uint64_t*)in == 0x0123456789abcdef) return 1;
    return 0;
}

static uint64_t get_fsize(char *in) {
   return (*(uint64_t*)(in + 8));
}

static void do_decompress(char *out, char *in, size_t insize) {
    uint64_t cur = 16;
    while (cur < insize) {
        uint8_t cmd = in[cur];
        cur += 1;

        switch (cmd) {
            case 0:
                // NOP
                break;
            case 1: {
                // Write byte
                uint8_t b = in[cur++];
                *(out++) = b;
                break;
            }
            case 2: {
                // Seek
                uint64_t off = *(uint64_t*)(&in[cur]);
                cur += sizeof(off);
                out += off;
                break;
            }
            case 3: {
                // Copy some previously written bytes
                uint64_t off = *(uint64_t*)(&in[cur]);
                cur += sizeof(off);
                uint64_t count = *(uint64_t*)(&in[cur]);
                cur += sizeof(off);

                memcpy(out, out-off, count);
                out += count;
                break;
            }
            default:
                break;
        }
    }
}
