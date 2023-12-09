void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void blinking(){
  digitalWrite(LED_BUILTIN, HIGH);   
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(300);                       // wait for a second  
}
void lit(){
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(2000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(300);                       // wait for a second  
}

void wait(){
  digitalWrite(LED_BUILTIN, LOW);
  delay(1200); 
}
// the loop function runs over and over again forever
void loop() {
  blinking();
  wait();

  lit();
  blinking();
  wait();
  
  blinking();
  lit();
  lit();
  lit();
  wait();

  lit();
  lit();
  lit();
  lit();
  lit();
  wait();

  lit();
  blinking();
  lit();
  lit();
  wait();

  blinking();
  blinking();
  blinking();
  blinking();
  wait();

  blinking();
  lit();
  wait();

  blinking();
  lit();
  blinking();
  wait();

  lit();
  blinking();
  blinking();
  wait();

  blinking();
  lit();
  lit();
  wait();

  blinking();
  lit();
  wait();

  blinking();
  lit();
  blinking();
  wait();

  blinking();
  wait();

  lit();
  blinking();
  lit();
  blinking();
  lit();
  lit();
  wait();

  delay(3000);
}
