#ifndef SHELLCODEVERIFIER_H_
#define SHELLCODEVERIFIER_H_

#include <stdbool.h>

#define MAX_FILE_SIZE (1ul * 1024 * 1024)

#define SANDBOX_DIR "sandbox"
#define COMPILER_NAME "compiler"
#define SOURCE_NAME "source_file"
#define OUTPUT_NAME "prog"

bool verify_buffer(const unsigned char* buf, size_t size);
unsigned long call_shellcode(void* buf);

#endif // SHELLCODEVERIFIER_H_
