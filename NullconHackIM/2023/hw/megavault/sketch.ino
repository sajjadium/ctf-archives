#include <LCD_I2C.h>

#define ARRSIZE(x) (sizeof(x)/sizeof((x)[0]))
#define BITAT(x) (1 << (x))

#define BTN_COUNT 18
#define FEEL_DELAY 5
#define BLINK_LED 17

enum { DISABLED, KEY, FUNC };

enum {
	FUNC_NONE,
	FUNC_BS,
	FUNC_ENTER,
	FUNC_LEFT,
	FUNC_RIGHT,
	FUNC_HOME,
	FUNC_DEL
};

enum {
	R1C1, R1C2, R1C3, R1C4,
	R2C1, R2C2, R2C3, R2C4,
	R3C1, R3C2, R3C3, R3C4,
	R4C1, R4C2, R4C3,
	  R5C12,    R5C3, R45C4
};

enum {
	NUMLOCK  = 1 << 0,
};

struct keycfg {
	uint8_t type;
	char c;
};

const char *bnames[BTN_COUNT] = {
	"R1C1", "R1C2", "R1C3", "R1C4",
	"R2C1", "R2C2", "R2C3", "R2C4",
	"R3C1", "R3C2", "R3C3", "R3C4",
	"R4C1", "R4C2", "R4C3",
	   "R5C12",     "R5C3", "R45C4"
};

const uint8_t pulsepins[] = { A2, A3, 9, A1, 8, A0 };
const uint8_t sensepins[] = { 6, 14, 4, 5, 7, 16 };
const uint8_t debugswitch = 10;

const uint8_t senselut[][6][2] = {
	{ {14, R2C1 }, {16, R3C1}, { 4, R4C1} },
	{ { 6, R1C2 }, {14, R2C2}, {16, R3C2}, {4, R4C2}, {5, R5C12} },
	{ { 6, R1C3 }, {14, R2C3}, {16, R3C3}, {4, R4C3}, {5, R5C3}, {7, R2C4} },
	{ {16, R1C4 } },
	{ { 6, R1C1 } },
	{ { 4, R45C4}, {14, R3C4} }
};

const uint8_t modkeys[] = { R1C1 };

const struct keycfg base_layer[BTN_COUNT] = {
	[R1C1]  = { DISABLED },
	[R1C2]  = { KEY, '/' },
	[R1C3]  = { KEY, '*' },
	[R1C4]  = { FUNC, FUNC_BS },
	[R2C1]  = { KEY, '7' },
	[R2C2]  = { KEY, '8' },
	[R2C3]  = { KEY, '9' },
	[R2C4]  = { KEY, '-' },
	[R3C1]  = { KEY, '4' },
	[R3C2]  = { KEY, '5' },
	[R3C3]  = { KEY, '6' },
	[R3C4]  = { KEY, '+' },
	[R4C1]  = { KEY, '1' },
	[R4C2]  = { KEY, '2' },
	[R4C3]  = { KEY, '3' },
	[R5C12] = { KEY, '0' },
	[R5C3]  = { KEY, '.' },
	[R45C4] = { FUNC, FUNC_ENTER }
};

const struct keycfg numlock_layer[BTN_COUNT] = {
	[R1C1]  = { DISABLED },
	[R1C2]  = { KEY, '/' },
	[R1C3]  = { KEY, '*' },
	[R1C4]  = { FUNC, FUNC_BS },
	[R2C1]  = { FUNC, FUNC_HOME },
	[R2C2]  = { DISABLED },
	[R2C3]  = { DISABLED },
	[R2C4]  = { KEY, '-' },
	[R3C1]  = { FUNC, FUNC_LEFT },
	[R3C2]  = { DISABLED },
	[R3C3]  = { FUNC, FUNC_RIGHT },
	[R3C4]  = { KEY, '+' },
	[R4C1]  = { DISABLED },
	[R4C2]  = { DISABLED },
	[R4C3]  = { DISABLED },
	[R5C12] = { DISABLED },
	[R5C3]  = { FUNC, FUNC_DEL },
	[R45C4] = { FUNC, FUNC_ENTER }
};

const struct keycfg *layers[1 << ARRSIZE(modkeys)] = {
	[0] = base_layer,
	[NUMLOCK] = numlock_layer
};

char pin[9] = { 0 };

char linebuf[256] = { 0 };

int16_t inputpos = 0;
char inputbuf[17] = { 0 };
char outputbuf[17] = { 0 };

int debugmode = 0;

int pbstates[BTN_COUNT] = { 0 };
int bstates[BTN_COUNT] = { 0 };

LCD_I2C lcd(0x27, 16, 2);

void
lcd_refresh(void)
{
	lcd.clear();
	lcd.noCursor();
	lcd.setCursor(0, 0);
	lcd.print(inputbuf);
	lcd.setCursor(0, 1);
	lcd.print(outputbuf);
	lcd.setCursor(inputpos, 0);
	lcd.cursor();
}

void
call_func(char c)
{
	switch (c) {
	case FUNC_BS:
		input_del();
		break;
	case FUNC_ENTER:
		input_enter();
		break;
	case FUNC_LEFT:
		inputpos--;
		lcd_refresh();
		break;
	case FUNC_RIGHT:
		inputpos++;
		lcd_refresh();
		break;
	case FUNC_HOME:
		inputpos = 0;
		lcd_refresh();
		break;
	case FUNC_DEL:
		inputbuf[inputpos] = 0;
		lcd_refresh();
	}
}

void
input_put(char c)
{
	if (inputpos >= 15)
		return;
	Serial.println("PUT");

	inputbuf[inputpos] = c;
	inputpos++;
	lcd_refresh();
}

void
input_del(void)
{
	int i;

	if (!inputpos)
		return;

	for (i = inputpos; i < sizeof(inputbuf); i++)
		inputbuf[i-1] = inputbuf[i];
	inputpos--;
	lcd_refresh();
}

void
input_enter(void)
{
	if (!strncmp(inputbuf, pin, sizeof(inputbuf))) {
		comm_open();
	} else {
		snprintf(outputbuf, sizeof(outputbuf), "wrong!");
	}
	lcd_refresh();
	memset(outputbuf, 0, sizeof(outputbuf));
}

void
blink(uint32_t ms)
{
	digitalWrite(BLINK_LED, LOW);
	delay(ms);
	digitalWrite(BLINK_LED, HIGH);
	delay(ms);
}

void
comm_init(void)
{
	size_t len;

	while (!Serial.available());

	while (1) {
		memset(linebuf, 0, sizeof(linebuf));
		len = Serial.readBytesUntil('\r', linebuf, sizeof(linebuf));
		if (!len) continue;
		if (debugmode) {
			Serial.print("<");
			Serial.println(linebuf);
		}
		if (!strncmp(linebuf, "!INIT", len))
			break;
	}

	Serial.println("!OK");

	blink(1000);
}

void
comm_open(void)
{
	size_t len;

	blink(1000);

	Serial.println("!FLAG");
	memset(linebuf, 0, sizeof(linebuf));
	len = Serial.readBytesUntil('\r', linebuf, sizeof(linebuf));
	if (debugmode) {
		Serial.print("<");
		Serial.println(linebuf);
	}

	if (!strncmp(linebuf, "!OK", len)) {
		len = Serial.readBytesUntil('\r', linebuf, sizeof(linebuf));
		strncpy(outputbuf, linebuf, sizeof(outputbuf));
	} else {
		snprintf(outputbuf, sizeof(outputbuf), "error..");
	}
}

void
getstates(void)
{
	int i, k;

	memcpy(pbstates, bstates, sizeof(bstates));
	memset(bstates, 0, sizeof(bstates));

	for (i = 0; i < ARRSIZE(pulsepins); i++) {
		for (k = 0; k < ARRSIZE(pulsepins); k++) {
			pinMode(pulsepins[k], k == i ? OUTPUT: INPUT);
			digitalWrite(pulsepins[k], LOW);
		}
		delay(FEEL_DELAY);

		for (k = 0; k < 6 && senselut[i][k][0]; k++) {
			if (digitalRead(senselut[i][k][0]) == LOW)
				bstates[senselut[i][k][1]] = true;
		}
	}
}

void
setup(void)
{
	int i;

	snprintf(pin, 9, "13371337");

	for (i = 0; i < ARRSIZE(sensepins); i++) {
		pinMode(sensepins[i], INPUT);
		digitalWrite(sensepins[i], HIGH);
	}

	pinMode(debugswitch, INPUT);
	digitalWrite(debugswitch, HIGH);
	delay(10);
	debugmode = (digitalRead(debugswitch) == LOW);

	lcd.begin();
	lcd_refresh();

	lcd.noBacklight();

	Serial.begin(9600);
	Serial.setTimeout(2000);
	comm_init();

	lcd.backlight();
}

void
loop(void)
{
	int i, k, layer;
	bool hit;

	getstates();

	layer = 0;
	for (i = 0; i < ARRSIZE(modkeys); i++)
		layer |= bstates[modkeys[i]] * (1 << i);

	hit = false;
	for (i = 0; i < BTN_COUNT; i++) {
		if (bstates[i] && !pbstates[i]) {
			hit = true;
			if (debugmode) {
				Serial.print("PRESS: ");
				Serial.println(bnames[i]);
			}
			if (layers[layer]) {
				if (layers[layer][i].type == KEY) {
					input_put(layers[layer][i].c);
				} else if (layers[layer][i].type == FUNC) {
					call_func(layers[layer][i].c);
				}
			}
		} else if (!bstates[i] && pbstates[i]) {
			if (debugmode) {
				Serial.print("RELEASE: ");
				Serial.println(bnames[i]);
			}
		}
	}

	if (debugmode && hit) {
		Serial.print("POS ");
		Serial.println(inputpos);
	}
}
