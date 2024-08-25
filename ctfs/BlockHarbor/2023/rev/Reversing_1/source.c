#define MAX_SIZE 32

const uint32_t a = 1103515245;
const uint32_t c = 12345;
const uint32_t m = 2147483647;
uint32_t seed = 1337;

unsigned char user_input[MAX_SIZE];
const uint32_t STATE[4] = {0x1e48add6, 0xaaa7550c, 0x18df53bf, 0xe6af1116};

uint32_t start[] = {0x0, 0x0, 0x0, 0x0};

uint32_t gen_random(void) {
  seed = (uint32_t)(((uint32_t)a * (uint32_t)seed + (uint32_t)c) % m);
  return (uint32_t)seed;
}

void setup() {
  Serial.begin(115200);
  Serial.println("==================================================");
  Serial.println("=               SECURE LOCK - v0.5               =");
  Serial.println("==================================================");
}

int check_pass(uint32_t start[]) {
    Serial.println("checking\n");
    uint32_t temp = 0;
    for (int i = 0; i < 4; ++i) {
      temp = start[i];
      temp *= (uint32_t)0xcafebeef;
      temp += (uint32_t)gen_random();
      temp *= (uint32_t)0xfacefeed;
      temp ^= (uint32_t)gen_random();

      if ((uint32_t)temp != (uint32_t)STATE[i]) {
        return 0;
      }
    }
    return 1;
}

void loop() {
  
  memset(user_input,0,MAX_SIZE);
  memset(start, 0, 16);

  Serial.println("Enter your password: ");

  while (Serial.available() == 0) {
    delay(100);
  }

  Serial.readBytes(user_input, MAX_SIZE);
  
  Serial.println();
  for (int i = 0; i < 4; i++) {
    
    start[i] |= ((uint32_t)user_input[(i * 4)]   << 24);
    start[i] |= ((uint32_t)user_input[(i * 4)+1] << 16);
    start[i] |= ((uint32_t)user_input[(i * 4)+2] << 8);
    start[i] |= ((uint32_t)user_input[(i * 4)+3] << 0);

    Serial.println(start[i],HEX);
  }

  if (check_pass(start) == 1) {
    Serial.print("Thats it!\r\nSubmit in the format FLAG{");
    for (int i = 0; i < 4; i++) {
          Serial.print(start[i],HEX);
    }
    Serial.println("}");
    while (true) { delay(1000); }
  }

  // Failed, just spin
  Serial.println("Incorrect password!");
  while (true) {delay(1000); }
}

