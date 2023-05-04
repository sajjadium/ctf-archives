#include "const.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>

// Convert input to int[2] e.g. "Mon 3" -> {0, 3}
int *str_to_time(char *input) {
  int *time = malloc(sizeof(int) * 2);
  char *token = strtok(input, " ");
  int i = 0;
  while (token != NULL) {
    if (i == 0) {
      printf("%s\n", token);
      if (!strcmp(token, "MON")) {
        time[1] = 0;
      } else if (!strcmp(token, "TUE")) {
        time[1] = 1;
      } else if (!strcmp(token, "WED")) {
        time[1] = 2;
      } else if (!strcmp(token, "THU")) {
        time[1] = 3;
      } else if (!strcmp(token, "FRI")) {
        time[1] = 4;
      } else {
        printf("Wrong input\n");
      }
    } else if (i == 1) {
      time[0] = atoi(token) - 1;
      printf("%d\n", time[0]);
      if (time[0] < 0 || time[0] > 4) {
        printf("Wrong input\n");
      }
    }
    token = strtok(NULL, " ");
    i++;
  }
  return time;
}

char *time_to_str(int time[2]) {
  char *str = malloc(sizeof(char) * 10);
  if (time[1] == 0) {
    sprintf(str, "MON");
  } else if (time[1] == 1) {
    sprintf(str, "TUE");
  } else if (time[1] == 2) {
    sprintf(str, "WED");
  } else if (time[1] == 3) {
    sprintf(str, "THU");
  } else if (time[1] == 4) {
    sprintf(str, "FRI");
  }
  sprintf(str, "%s %d", str, time[0] + 1);
  return str;
}

void init() {
  alarm(180);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

// print table with type comma
void print_table(comma table[5][5]) {
  int i, j;
  printf("\n");
  printf(" \tMON\t\tTUE\t\tWED\t\tTHU\t\tFRI\n");
  for (i = 0; i < 5; i++) {
    printf("%d\t", i + 1);
    for (j = 0; j < 5; j++) {
      printf("%-16s", table[i][j].name);
    }
    printf("\n");
  }
  printf("\n");
}

void print_mandatory_list() {
  int i;
  for (i = 0; i < 3; i++) {
    printf("%d : %s - %s - %s \n", i, mandatory_list[i].name,
           mandatory_list[i].professor, time_to_str(mandatory_list[i].time));
  }
}

void print_elective_list() {
  int i;
  for (i = 0; i < 2; i++) {
    printf("%d : %s - %s\n", i, elective_list[i].name,
           elective_list[i].professor);
  }
}

comma *choose_time(comma timetable[5][5]) {
  char input[7];
  int *time;
  print_table(timetable);
  printf("Please choose the class.\n");
  printf("ex) FRI 3\n");
  printf(">");
  read(0, input, 6);
  time = str_to_time(input);
  if (timetable[time[0]][time[1]].name == NULL) {
    printf("No class\n");
    exit(1);
  }
  return &timetable[time[0]][time[1]];
}
