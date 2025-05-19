#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_AlphaNum4 alpha4 = Adafruit_AlphaNum4();

String flag = "byuctf{REDACTED}";

void setup() {
  Serial.begin(9600);
  alpha4.begin(0x70);
  alpha4.writeDigitRaw(0, 0x0);
  alpha4.writeDigitRaw(1, 0x0);
  alpha4.writeDigitRaw(2, 0x0);
  alpha4.writeDigitRaw(3, 0x0);
  alpha4.writeDisplay();
}

void loop() {
  delay(1000);
  for (uint8_t i = 0; i < (flag.length() - 3); i++) {
    alpha4.writeDigitAscii(0, flag[i]);
    alpha4.writeDigitAscii(1, flag[i+1]);
    alpha4.writeDigitAscii(2, flag[i+2]);
    alpha4.writeDigitAscii(3, flag[i+3]);
    alpha4.writeDisplay();
    delay(500);
  }
}
