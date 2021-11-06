#include <stdio.h>
#include <unistd.h>

int main() {
  char feedback[0x40];
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(180);
  puts("Enter your feedback: ");
  scanf("%s", feedback);
  puts("Thank you!");
  return 0;
}
