#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  char buf[4];
  setvbuf(stdout, NULL, _IONBF, 0);
  printf("Välkommen till datumtjänsten för alla!\n");
  printf("Ange ett alternativ:\n"
         "1) ISO-8601\n"
         "2) Jänkar-format\n"
         "3) Författarens påhitt\n"
         "4) Lämna\n");
  scanf("%s", buf);

  int option = atoi(buf);

  switch (option) {
  case 1:
    system("date -I");
    break;
  case 2:
    system("date +%D");
    break;
  case 3:
    system("date +'Dag %j/360, Vecka %V'");
    break;
  case 4:
    return 0;
  default:
    printf("Ogiltig indata!\n");
  }
}
