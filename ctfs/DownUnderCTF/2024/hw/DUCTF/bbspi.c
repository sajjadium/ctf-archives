/* bbspi.h:

#include <stddef.h>
#include <stdint.h>

void bbspi_init(uint32_t cs, uint32_t sck, uint32_t mosi, uint32_t miso);

size_t bbspi_handle_rx(const uint8_t *rx_data, const size_t rx_count, uint8_t *tx_data);

*/

#include <stdbool.h>
#include <string.h>
#include "bbspi.h"
#include "hardware/gpio.h"
#include "hardware/irq.h"

static uint32_t bbspi_cs_pin = 0;
static uint32_t bbspi_sck_pin = 0;
static uint32_t bbspi_miso_pin = 0;
static uint32_t bbspi_mosi_pin = 0;

static bool bbspi_cs_asserted = false;

static uint8_t rx_data[32] = {0};
static uint8_t tx_data[32] = {0};

static size_t tx_i = 0;
static size_t rx_i = 0;

void bbspi_gpio_callback(uint16_t gpio, uint16_t events)
{
    if (gpio == bbspi_sck_pin)
    {
        if (bbspi_cs_asserted)
        {
            // data!!
            if (events & GPIO_IRQ_EDGE_FALL)
            {
                bool rx_bit = gpio_get(bbspi_mosi_pin);

                rx_data[rx_i / 8] |= (rx_bit << (7 - (rx_i % 8)));
                rx_i++;
            }
            else if (events & GPIO_IRQ_EDGE_RISE)
            {
                if (rx_i % 8 == 0)
                {
                    bbspi_handle_rx(&rx_data, rx_i / 8, &tx_data);
                }

                bool bit = !!(tx_data[tx_i / 8] & (1 << (7 - (tx_i % 8))));
                gpio_put(bbspi_miso_pin, bit);
                tx_i++;
            }
        }
    }
    else if (gpio == bbspi_cs_pin)
    {
        if (events & GPIO_IRQ_EDGE_FALL)
        {
            rx_i = 0;
            tx_i = 0;
            bbspi_cs_asserted = true;
            memset(rx_data, 0x00, sizeof(rx_data));
            memset(tx_data, 0x00, sizeof(tx_data));

            bool bit = !!(tx_data[tx_i / 8] & (1 << (7 - (tx_i % 8))));
            gpio_put(bbspi_miso_pin, bit);
            tx_i++;
        }
        else if (events & GPIO_IRQ_EDGE_RISE)
        {
            bbspi_cs_asserted = false;
            gpio_put(bbspi_miso_pin, false);
        }
    }
}

// Bitbanged SPI slave
void bbspi_init(uint32_t cs, uint32_t sck, uint32_t mosi, uint32_t miso)
{
    gpio_set_function(cs, GPIO_FUNC_SIO);
    gpio_set_function(sck, GPIO_FUNC_SIO);
    gpio_set_function(mosi, GPIO_FUNC_SIO);
    gpio_set_function(miso, GPIO_FUNC_SIO);

    gpio_set_inover(cs, GPIO_OVERRIDE_NORMAL);
    gpio_set_inover(sck, GPIO_OVERRIDE_NORMAL);
    gpio_set_inover(mosi, GPIO_OVERRIDE_NORMAL);
    gpio_set_inover(miso, GPIO_OVERRIDE_NORMAL);

    gpio_set_irqover(cs, GPIO_OVERRIDE_NORMAL);
    gpio_set_irqover(sck, GPIO_OVERRIDE_INVERT);
    gpio_set_irqover(mosi, GPIO_OVERRIDE_NORMAL);
    gpio_set_irqover(miso, GPIO_OVERRIDE_NORMAL);

    gpio_set_outover(cs, GPIO_OVERRIDE_NORMAL);
    gpio_set_outover(sck, GPIO_OVERRIDE_NORMAL);
    gpio_set_outover(mosi, GPIO_OVERRIDE_NORMAL);
    gpio_set_outover(miso, GPIO_OVERRIDE_NORMAL);

    gpio_set_dir(cs, GPIO_IN);
    gpio_set_dir(sck, GPIO_IN);
    gpio_set_dir(mosi, GPIO_IN);
    gpio_set_dir(miso, GPIO_OUT);
    gpio_set_pulls(miso, true, true);
    gpio_put(bbspi_miso_pin, false);

    gpio_set_irq_enabled(cs, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true);  // CS falls
    gpio_set_irq_enabled(sck, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true); // clock rises/falls

    gpio_set_irq_callback(bbspi_gpio_callback);

    irq_set_enabled(IO_IRQ_BANK0, true);

    bbspi_cs_pin = cs;
    bbspi_sck_pin = sck;
    bbspi_mosi_pin = mosi;
    bbspi_miso_pin = miso;
}