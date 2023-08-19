#include "autotrace/autotrace.h"
#include <sys/mman.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void init() {
  autotrace_init();
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);
  alarm(30);
}

char* create_temp_image() {
    char temp_name[256] = "/tmp/image.XXXXXX";
    char *temp_buf, *fname;
    unsigned int file_size = 0;
    int temp_fd;

    // input file size
    printf("Image size (max: 4096): ");
    scanf("%u", &file_size);
    if (file_size >= 0x1000) {
      printf("image size too large!\n");
      return NULL;
    }
    temp_buf = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, 0, 0);
    if (temp_buf == (void *)-1) {
        perror("mmap error");
        return NULL;
    }
    if (read(STDIN_FILENO, temp_buf, 0x1000) != file_size) {
        printf("read error: File size not match\n");
        return NULL;
    }

    // make temp file
    if ((temp_fd = mkstemp(temp_name)) < 0) {
        perror("mktemp error");
        return NULL;
    }

    if (write(temp_fd, temp_buf, file_size) < 0) {
        perror("write error");
        return NULL;
    }
    close(temp_fd);

    if ((fname = strdup(temp_name)) == NULL) {
      perror("strdup error");
      return NULL;
    }

    return fname;
}

int do_convert() {
  at_bitmap * bitmap;
  at_splines_type * splines;
  at_bitmap_reader * reader;
  at_spline_writer * writer;
  at_fitting_opts_type * opts;

  char from_format[16];
  char to_format[16];
  char* fname;

  // get user input
  printf("Source image format: ");
  scanf("%15s", from_format);
  reader = at_input_get_handler_by_suffix(from_format);
  if (reader == NULL) {
    printf("input image format not support!\n");
    return 0;
  }

  printf("Vector image format: ");
  scanf("%15s", to_format);
  writer = at_output_get_handler_by_suffix(to_format);
  if (writer == NULL) {
    printf("output image format not support!\n");
    return 0;
  }

  fname = create_temp_image();
  if (fname == NULL) {
    printf("failed to create temp image!\n");
    return 0;
  }

  // parse image
  bitmap = at_bitmap_read(reader, fname, NULL, NULL, NULL);
  if (bitmap->bitmap == NULL) {
    printf("invalid or malformed image!\n");
    return 0;
  }
  unlink(fname);

  // conversion
  opts = at_fitting_opts_new();
  splines = at_splines_new(bitmap, opts, NULL, NULL);
  at_splines_write(writer, stdout, "", NULL, splines, NULL, NULL);

  // cleanup
  at_splines_free(splines);
  at_fitting_opts_free(opts);
  at_bitmap_free(bitmap);
  return 1;
}

int main(int argc, char * argv[]) {
  char buf[16];
  init();

  do {
    if (do_convert() == 0) {
      exit(-1);
    }
    printf("continue?\n");
    scanf("%15s", buf);
  } while (buf[0] == 'y' || buf[0] == 'Y');
  
  return 0;
}
