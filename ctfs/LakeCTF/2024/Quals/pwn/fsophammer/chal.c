#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define N_ENTRIES 4
#define MAX_SZ 0x3000

const char banner[] = "\n\n"
"  _________.____       _____      _____            .____   ._.   ____.\n"
" /   _____/|    |     /  _  \\    /     \\           |   _|  | |  |_   |\n"
" \\_____  \\ |    |    /  /_\\  \\  /  \\ /  \\          |  |    |_|    |  |\n"
" /        \\|    |___/    |    \\/    Y    \\         |  |    |-|    |  |\n"
"/_______  /|_______ \\____|__  /\\____|__  /         |  |_   | |   _|  |\n"
"        \\/         \\/       \\/         \\/          |____|  |_|  |____|\n"
"    ______________ ______________                          ._.        \n"
"    \\__    ___/   |   \\_   _____/                          | |        \n"
"      |    | /    ~    \\    __)_                           |_|        \n"
"      |    | \\    Y    /        \\                          |-|        \n"
"      |____|  \\___|_  /_______  /                          | |        \n"
"                    \\/        \\/                           |_|        \n\n";
char* entries [N_ENTRIES];
int slammed = 0;

void init_setup(void) __attribute__ ((constructor));
void alloc();
void free();
void slam();

void init_setup() {
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);
}

int get_num(const char* prompt, size_t* num, size_t bound) {
  printf("%s> ", prompt);
  int scanned = scanf("%zu",num);
  getchar();
  if((scanned != 1) || (bound && *num >= bound)) {
    puts("[-] getnum");
    return -1;
  }
  return 0;
}

void get_str(char* buf, size_t cap) {
  char c;
  printf("content> ");
  // I'm so nice that you won't have to deal with null bytes
  for (int i = 0 ; i < cap ; ++i) {
    int scanned = scanf("%c",&c);
    if (scanned !=1 || c=='\n') {
      return;
    }
    buf[i] = c;
  }
}

void alloc() {
  size_t idx;
  size_t sz;
  if(get_num("index",&idx,N_ENTRIES)) {
    return;
  }
  if(get_num("size",&sz,MAX_SZ)) {
    return;
  }
  entries[idx] = malloc(sz);
  get_str(entries[idx],sz);
  printf("alloc at index: %zu\n", idx);
}

void free_() {
  size_t idx;
  if(get_num("index",&idx,N_ENTRIES)) {
    return;
  }
  if(!entries[idx]) {
    return;
  }
  free(entries[idx]);
  entries[idx] = NULL;
}


void slam() {
  size_t idx;
  size_t pos;
  puts("is this rowhammer? is this a cosmic ray?");
  puts("whatever, that's all you'll get!");
  if (get_num("index",&idx,sizeof(*stdin))) {
    return;
  }

  if (idx < 64) {
    puts("[-] invalid index");
    return;
  }

  if (get_num("pos",&pos,8)) {
    return;
  }
  unsigned char byte = ((char*)stdin)[idx];
  unsigned char mask = ((1<<8)-1) & ~(1<<pos);
  byte = (byte & mask) | (~byte & (~mask));
  ((char*)stdin)[idx] = byte;
}

void menu() {
  puts("1. alloc\n2. free\n3. slam");
  size_t cmd;

  if (get_num("cmd",&cmd, 0)) {
    return;
  }

  switch(cmd) {
    case 1:
      alloc();
      break;
    case 2:
      free_();
      break;
    case 3:
      if (!slammed) {
        slam();
        slammed = 1;
      } else {
        puts("[-] slammed already");
      }
      break;
    default:
      puts("[-] invalid cmd");
      break;
  }
}

int main() {
  puts(banner);
  while(1) {
    menu();
  }
  return 0;
}
