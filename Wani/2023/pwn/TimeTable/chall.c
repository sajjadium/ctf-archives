#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

comma timetable[5][5];

void print_mandatory_subject();
void print_elective_subject();
void register_mandatory_class();
void register_elective_class();
void print_class_detail();
void write_memo();
void print_menu();
student register_student();

student user;
int main() {
  init();
  user = register_student();
  int i;
  while (1) {
    print_table(timetable);
    print_menu();
    scanf("%d", &i);
    switch (i) {
    case 1:
      register_mandatory_class();
      break;
    case 2:
      register_elective_class();
      break;
    case 3:
      print_class_detail();
      break;
    case 4:
      write_memo();
      break;
    case 5:
      exit(0);
      break;
    default:
      printf("invalid input\n");
    }
  }
}

void print_mandatory_subject(mandatory_subject *mandatory_subjects) {
  printf("Class Name : %s\n", mandatory_subjects->name);
  printf("Class Time : %s\n", time_to_str(mandatory_subjects->time));
  printf("Class Target : %s > ", mandatory_subjects->target[0]);
  printf("%s > ", mandatory_subjects->target[1]);
  printf("%s > ", mandatory_subjects->target[2]);
  printf("%s \n", mandatory_subjects->target[3]);
  printf("Professor : %s\n", mandatory_subjects->professor);
  printf("Short Memo : %s\n", mandatory_subjects->memo);
}

void print_elective_subject(elective_subject *elective_subjects) {
  printf("Class Name : %s\n", elective_subjects->name);
  printf("Class Time : %s\n", time_to_str(elective_subjects->time));
  printf("Professor : %s\n", elective_subjects->professor);
  printf("Short Memo : %s\n", elective_subjects->memo);
}

void register_mandatory_class() {
  int i;
  mandatory_subject choice;
  print_table(timetable);
  printf("-----Mandatory Class List-----\n");
  print_mandatory_list();
  printf(">");
  scanf("%d", &i);
  choice = mandatory_list[i];

  printf("%d\n", choice.time[0]);
  timetable[choice.time[0]][choice.time[1]].name = choice.name;
  timetable[choice.time[0]][choice.time[1]].type = MANDATORY_CLASS_CODE;
  timetable[choice.time[0]][choice.time[1]].detail = &mandatory_list[i];
}

void register_elective_class() {
  int i;
  elective_subject choice;
  print_table(timetable);
  printf("-----Elective Class List-----\n");
  print_elective_list();
  printf(">");
  scanf("%d", &i);
  choice = elective_list[i];
  if (choice.IsAvailable(&user) == 1) {
    timetable[choice.time[0]][choice.time[1]].name = choice.name;
    // The type of timetable is 0 by default since it is a global value.
    timetable[choice.time[0]][choice.time[1]].detail = &elective_list[i];
  } else {
    printf("You can't register this class\n");
  }
}

void print_class_detail() {
  comma *choice = choose_time(timetable);
  if (choice->type == MANDATORY_CLASS_CODE) {
    print_mandatory_subject(choice->detail);
  } else if (choice->type == ELECTIVE_CLASS_CODE) {
    print_elective_subject(choice->detail);
  }
}

void write_memo() {
  comma *choice = choose_time(timetable);
  printf("WRITE MEMO FOR THE CLASS\n");

  if (choice->type == MANDATORY_CLASS_CODE) {
    read(0, ((mandatory_subject *)choice->detail)->memo, 30);
  } else if (choice->type == ELECTIVE_CLASS_CODE) {
    read(0, ((elective_subject *)choice->detail)->memo, 30);
  }
}

void print_menu() {
  printf("1. Register Mandatory Class\n");
  printf("2. Register Elective Class\n");
  printf("3. See Class Detail\n");
  printf("4. Write Memo\n");
  printf("5. Exit\n");
  printf(">");
}

student register_student() {
  student new_student;
  printf("WELCOME TO THE TIME TABLE PROGRAM\n");
  printf("Enter your name : ");
  read(0, new_student.name, 9);
  printf("Enter your student id : ");
  scanf("%d", &new_student.studentNumber);
  printf("Enter your major : ");
  scanf("%d", &new_student.EnglishScore);
  return new_student;
}
