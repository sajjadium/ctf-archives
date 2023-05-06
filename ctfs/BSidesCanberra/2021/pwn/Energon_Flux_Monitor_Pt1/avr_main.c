#define BAUD 38400

#include <avr/io.h>
#include <avr/eeprom.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/setbaud.h>

// =========== Idle ===========
// Sleeps until an interrupt is triggered.
void idle()
{
    sleep_enable();
    sleep_cpu();
    sleep_disable();
}

// =========== Watchdog ===========
void wdt_init()
{
    wdt_reset();
    wdt_enable(WDTO_30MS);
}

// =========== Bootloader Check ===========
// Bootloader address defined externally
extern void(*boot)(void);

// Bootload check
void chk_boot (void) __attribute__ ((naked)) __attribute__ ((section (".init3")));
void chk_boot (void)
{
    // Check for pin on startup
    DDRD = 0x00;
    if((PORTD & (1 << PIND3)))
    {
        // Jump to bootloader
        asm("rjmp boot");
    }
    
}

// =========== Timer 0 ===========
// Ticks timer
// When the timer overflows increment the tick count.
volatile uint16_t ticks;
ISR(TIMER0_OVF_vect)
{
    ticks++;
}

void init_timer0()
{
    ticks = 0;

    TCCR0A = (1 << WGM01);   // CTC - TOP = OCR0A
    TCCR0B = (1 << CS01);    // Clk/8
    OCR0A = 250;

    TIMSK |= (1 << TOIE0);

    //Interrupt should trigger every (250 / (F_CPU/8)) cycles.
    // At 8MHz this is 250us 
}

// Time constants for convenience
#define SEC 4000
#define QSEC 1000

// =========== UART IO ===========
// Serial buffer. Must be global.
struct buf_t {
    uint8_t data[32];
    volatile uint8_t * write_pos;
} buffer;

volatile uint8_t input_ready = 0;

#define clear_buffer() {buffer.write_pos = buffer.data; buffer.data[0] = 0;}


ISR(USART_RX_vect)
{
    // Get a character from the serial
    uint8_t b = UDR;

    *buffer.write_pos++ = b;
    if(buffer.write_pos >= (buffer.data + sizeof(buffer)))
        buffer.write_pos = buffer.data;

    if (b == '\n')
    {
        buffer.write_pos = 0;
        input_ready = 1;
    }
}

void init_uart()
{
    UCSRC |= (3 << UCSZ0); // 8 bits

    // Set baud
    UBRRH = UBRRH_VALUE;
    UBRRL = UBRRL_VALUE;
#if USE_2X
    UCSRA |= (1 << U2X);
#else
    UCSRA &= ~(1 << U2X);
#endif

    // Enable
    UCSRB |= (1 << RXEN) | (1 << TXEN) | (1 << RXCIE);

    // DDR for the TX/RX pins is overridden by the USART so we don't need to set it.
}


// =========== Print Functions ===========
// Send a character. Blocking.
void uart_putchar(uint8_t c)
{
        loop_until_bit_is_set(UCSRA, UDRE);
        UDR = c;
}

// SRAM print
void uart_print(uint8_t * str)
{
    while(*str != 0)
    {
        uart_putchar(*str);
        str++;
    }
}

// EEPROM print
void uart_print_E(const uint8_t * str)
{
    uint8_t val = eeprom_read_byte(str);
    while(val != 0)
    {
        uart_putchar(val);
        str++;
        val = eeprom_read_byte(str);
    }
}

uint8_t * itoa(uint16_t val)
{
    // No memory alloctor :(
    // Declare a static buffer for the output string.
    // It should be big enough for the largest possible value.
    static uint8_t output[5];
    
    // We have to start at the lowest digit and work upwards.
    uint8_t index = sizeof(output) - 1;

    // Start with the terminator.
    output[index--] = '\0';
    
    // Decimal division requires too much program memory.
    // Just do it in hexadecimal.
    do {
        uint8_t nibble = val & 0xf;
        uint8_t base = nibble < 0xa ? '0' : ('A' - 0xa);

        output[index--] = base + nibble;
        val >>= 4;
    } while(val);
    
    // Return a pointer to the last character that was written
    return &(output[++index]);
}

// =========== Energon Flux Sensor Comms ===========
// Store strings in EEPROM to save program memory.
const EEMEM uint8_t efd[] = "Density:\n";
const EEMEM uint8_t hex[] = "0x";
const EEMEM uint8_t units[] = " EF/m3\n";
const EEMEM uint8_t flag[] = "cybears{=========FLAG_GOES_HERE=========}";
const EEMEM uint8_t anim[] = "\\|/-";


uint16_t get_sample()
{
    // TODO - Read the actual value from the sensor.
    return 174;
}

uint16_t get_average()
{
    // Average across 2 seconds
    // Sample every ~1/4 second
    uint16_t avg = 0;
    uint8_t count = 8;

    // An animation to let the user know we are doing something.

    uart_putchar(' ');
    
    // Take the first sample as soon as practical.
    int next = ticks + 2;
    while (count)
    {
        wdt_reset();
        idle(); // The timer should wake us up when it ticks over

        if (ticks == next)
        {
            next = ticks + QSEC;

            // Divide by number of samples and add to average.
            avg += (get_sample() >> 3);
            count--;

            // Let the user know we are doing something.
            uart_putchar('\b');
            uart_putchar(eeprom_read_byte(&anim[count & 3]));
        }
    }
    
    uart_putchar('\n');
    return avg;
}


// =========================
// ====== Application ======
// =========================

// Put strings in EEPROM to save program space
const EEMEM uint8_t menu_str[] = (
    "\n-Menu-\n"
    "e)cho\n"
    "t)ime\n"
    "s)ample\n"
    "a)verage\n"
    "\n>");

const EEMEM uint8_t time_str[] = "Time: ";
const EEMEM uint8_t avg_str[] = "Avg: "; 
const EEMEM uint8_t err_str[] = "Err: ";


int main()
{
    wdt_init();

    // Idle sleep mode
    MCUSR &= ~((1 << SM1) | (1 << SM0));
    
    // Initialisation
    clear_buffer();
    init_uart();
    init_timer0();

    sei();

    // main loop
    while(1)
    {
        uart_print_E(menu_str);

        // Wait for a uart line
        while (!input_ready)
        {
            idle(); // UART interrupt should wake us from sleep.
            wdt_reset();
        }

        switch(buffer.data[0])
        {
            case 'e':
                uart_print(&buffer.data[1]);
                break;
            
            case 't':
                uart_print_E(time_str);
                uart_print_E(hex);
                uart_print(itoa(ticks));
                uart_putchar('\n');
                break;
            
            case 's':
                uart_print_E(efd);
                uart_print_E(hex);
                uart_print(itoa(get_sample()));
                uart_print_E(units);
                break;
            
            case 'a':
                uart_print_E(efd);
                uart_print_E(avg_str);
                uint16_t avg = get_average();
                uart_print_E(hex);
                uart_print(itoa(avg));
                uart_print_E(units);
                break;
            
            case '\n':
                break;
                
            default:
                uart_print_E(err_str);
                uart_putchar(buffer.data[0]);
                uart_putchar('\n');
                break;
        }
        
        clear_buffer()
        input_ready = 0;
    }
}
