// Compile with `gcc -static -fno-tree-loop-distribute-patterns -nostdlib -O3 -o example example.c sdk.c`

#include <stddef.h>
#include <stdint.h>

void write_all(char *buf, size_t count);
size_t read(char *buf, size_t count);
void *mmap(void *addr, size_t length, int prot, int flags, int fd, size_t offset);
void *malloc(size_t count);
void print(char *buf);

int main();

#define PROT_READ	0x1		/* Page can be read.  */
#define PROT_WRITE	0x2		/* Page can be written.  */
#define PROT_EXEC	0x4		/* Page can be executed.  */
/* Sharing types (must choose one and only one of these).  */
#define MAP_SHARED	0x01		/* Share changes.  */
#define MAP_PRIVATE	0x02		/* Changes are private.  */
#define MAP_SHARED_VALIDATE	0x03	/* Share changes and validate extension flags.  */
#define MAP_DROPPABLE	0x08		/* Zero memory under memory pressure.  */
#define MAP_TYPE	0x0f		/* Mask for type of mapping.  */
#define MAP_FIXED	0x10		/* Interpret addr exactly.  */

#define MAP_FILE	0
#define MAP_ANONYMOUS	0x20		/* Don't use a file.  */
