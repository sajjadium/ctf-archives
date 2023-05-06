#define LED_PORT_DDR        DDRC
#define LED_PORT_OUTPUT     PORTC
#define LED1_BIT            0
#define LED2_BIT            1

#include <stdlib.h>
#include <string.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include "usbdrv.h"
#include <avr/pgmspace.h>   /* required by usbdrv.h */
#include "requests.h"       /* The custom request numbers we use */

struct __attribute__((__packed__)) entry{
    uchar * content;
    uchar length;
};

volatile const static char flag[] = "flag: hxp{censored........................}";
#define SIZE 16u
static uchar currentRequest, currentIndex, currentPosition, bytesRemaining;
static struct entry store[SIZE];


usbMsgLen_t usbFunctionSetup(uchar data[8])
{
    usbRequest_t *rq = (void *)data;

    if(rq->bRequest == CUSTOM_RQ_GET_STATUS && rq->wIndex.word < SIZE && store[rq->wIndex.word].length > 0){
        currentRequest = rq->bRequest;
        currentPosition = 0;

        bytesRemaining = store[rq->wIndex.word].length;
        if(bytesRemaining > rq->wLength.word)          // if the host requests less than we have
            bytesRemaining = rq->wLength.word;         // return only the amount requested
        currentIndex = rq->wIndex.word;

        return USB_NO_MSG;                          // tell driver to use usbFunctionRead()
    }else if(rq->bRequest == CUSTOM_RQ_SET_STATUS && rq->wIndex.word < SIZE){
        currentRequest = rq->bRequest;
        currentPosition = 0;                // initialize position index

        bytesRemaining = rq->wLength.word;  // store the amount of data requested
        currentIndex = rq->wIndex.word; 
        store[currentIndex].length = bytesRemaining;
        store[currentIndex].content = realloc(store[currentIndex].content, bytesRemaining);

        return USB_NO_MSG;        // tell driver to use usbFunctionWrite()
    }
    return 0;   /* default for not implemented requests: return no data back to host */
}

uchar usbFunctionRead(uchar *data, uchar len)
{
    uchar i;
    if(len > bytesRemaining)                // len is max chunk size
        len = bytesRemaining;               // send an incomplete chunk
    bytesRemaining -= len;

    for(i = 0; i < len; i++) {
        if(currentRequest == CUSTOM_RQ_GET_STATUS){
            data[i] = store[currentIndex].content[currentPosition++];
        }
    }
    return len;                             // return real chunk size
}

uchar usbFunctionWrite(uchar *data, uchar len)
{
    uchar i;
    if(len > bytesRemaining)                // if this is the last incomplete chunk
        len = bytesRemaining;               // limit to the amount we can store
    bytesRemaining -= len;
    for(i = 0; i < len; i++) {
        store[currentIndex].content[currentPosition++] = data[i];
    }

    return bytesRemaining == 0;             // return 1 if we have all data
}

void blink()
{
    DDRC=0xFF;
    for(;;){
        wdt_reset();
        _delay_ms(50);
        LED_PORT_OUTPUT |= _BV(LED2_BIT);
        _delay_ms(50);
        LED_PORT_OUTPUT &= ~_BV(LED2_BIT);
    }
}

int __attribute__((noreturn)) main(void)
{
    uchar i;
    uint16_t j;

    wdt_enable(WDTO_250MS);
    /* RESET status: all port bits are inputs without pull-up.
     * That's the way we need D+ and D-. Therefore we don't need any
     * additional hardware initialization.
     */

    LED_PORT_DDR |= _BV(LED1_BIT) | _BV(LED2_BIT);   /* make the LED bits outputs */
    LED_PORT_OUTPUT = 0x0;

    usbInit();
    usbDeviceDisconnect();  /* enforce re-enumeration, do this while interrupts are disabled! */
    i = 0;
    while(--i){             /* fake USB disconnect for > 250 ms */
        wdt_reset();
        _delay_ms(1);
    }
    usbDeviceConnect();

    sei();
    j = 0;
    for(;;j--){                /* main event loop */
        wdt_reset();
        usbPoll();

        if(j % 0x2000 == i)
            LED_PORT_OUTPUT ^= _BV(LED1_BIT);
    }
}

