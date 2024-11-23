#include <util/delay.h>
void setup() {Serial.begin(9600);}
void loop() {
  char password[32];
  char input[32];
  int index;
  int userend=1;
  index=0;

  sprintf(password,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
  
  while(1==1){
    if(userend==1){Serial.print("Password: ");userend=0;index=0;}
    while (Serial.available() == 0) {_delay_ms(500);}
    if (Serial.available() > 0) {
      char inchar = Serial.read();
      if (inchar == '\n') {
        input[index] = '\0';
        userend=1;
        if (strcmp(input, password) == 0) {
          Serial.println("\nWelcome to the system");
          Serial.println("\nC0ncl4v3{68b329da9893e34099c7d8ad5cb9c940}");
          index = 0;
        } else {
          Serial.println("\nIncorrect password!!");
          index = 0;
        }
      } else {
        input[index] = inchar;
        index++;
      }}}}
