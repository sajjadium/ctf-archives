char * flag = "REDACTED";
String curr, first, second;
int in1=29, in2=27, in3=25, in4=23;
int out1=53, out2=51, out3=49, out4=47;
int i;

String get_output(String bits) {
    String output;
    digitalWrite(out1, ((bits[0] == '1')? HIGH : LOW));
    digitalWrite(out2, ((bits[1] == '1')? HIGH : LOW));
    digitalWrite(out3, ((bits[2] == '1')? HIGH : LOW));
    digitalWrite(out4, ((bits[3] == '1')? HIGH : LOW));
    delay(1000);
    output += String(digitalRead(in1));
    output += String(digitalRead(in2));
    output += String(digitalRead(in3));
    output += String(digitalRead(in4));
    return output;
}

//converts a given number into binary
String binary(int number) {
  String r;
  while(number!=0) {
    r = (number % 2 == 0 ? "0" : "1")+r; 
    number /= 2;
  }
  while ((int) r.length() < 8) {
    r = "0"+r;
  }
  return r;
}

void setup() {
  i = 0;
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  pinMode(out3, OUTPUT);
  pinMode(out4, OUTPUT);
  pinMode(in1, INPUT);
  pinMode(in2, INPUT);
  pinMode(in3, INPUT);
  pinMode(in4, INPUT);
  Serial.begin(9600);
}

void loop() {
  if (i < strlen(flag)) {
    curr = binary(flag[i]);
    first = curr.substring(0,4);
    second = curr.substring(4,8);
    Serial.print(get_output(first));
    Serial.println(get_output(second));
    delay(1000);
    i++;
  }
}