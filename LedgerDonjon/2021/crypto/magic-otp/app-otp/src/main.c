#include "os.h"
#include <stdbool.h>

#include "os_io_seproxyhal.h"
#include "string.h"

#include "ux.h"

#include "crypto.h"

unsigned int io_seproxyhal_touch_exit(const bagl_element_t *e);

unsigned char G_io_seproxyhal_spi_buffer[IO_SEPROXYHAL_BUFFER_SIZE_B];

#ifdef HAVE_UX_FLOW
#include "ux.h"
    ux_state_t G_ux;
    bolos_ux_params_t G_ux_params;
#else // HAVE_UX_FLOW
    ux_state_t ux;
#endif // HAVE_UX_FLOW

// display stepped screens
unsigned int ux_step;
unsigned int ux_step_count;


//////////////////////////////////////////////////////////////////////
#define xstr(s) str(s)
#define str(s) #s
UX_STEP_NOCB(
    ux_idle_flow_1_step, 
    bn, 
    {
      "OTP",
      xstr(MODE)
    });
UX_STEP_VALID(
    ux_idle_flow_2_step,
    pb,
    os_sched_exit(-1),
    {
      &C_icon_dashboard,
      "Quit",
    });
const ux_flow_step_t *        const ux_idle_flow [] = {
  &ux_idle_flow_1_step,
  &ux_idle_flow_2_step,
  FLOW_END_STEP,
};


unsigned int io_seproxyhal_touch_exit(const bagl_element_t *e) {
    // Go back to the dashboard
    os_sched_exit(0);
    return 0; // do not redraw the widget
}

void ui_idle(void) {
ux_step_count = 0;

#if defined(TARGET_BLUE)
    UX_DISPLAY(ui_idle_blue, NULL);
#elif defined(HAVE_UX_FLOW)
    // reserve a display stack slot if none yet
    if(G_ux.stack_count == 0) {
        ux_stack_push();
    }
    ux_flow_init(0, ux_idle_flow, NULL);
#elif defined(TARGET_NANOS)
    UX_DISPLAY(ui_idle_nanos, NULL);
#endif
}

unsigned int ui_idle_nanos_button(unsigned int button_mask,
                                  unsigned int button_mask_counter) {
    switch (button_mask) {
    case BUTTON_EVT_RELEASED | BUTTON_LEFT: // EXIT
        io_seproxyhal_touch_exit(NULL);
        break;
    }
    return 0;
}

unsigned int ui_address_nanos_button(unsigned int button_mask,
                                     unsigned int button_mask_counter) {
    switch (button_mask) {
    case BUTTON_EVT_RELEASED | BUTTON_LEFT: // CANCEL
        io_seproxyhal_touch_address_cancel(NULL);
        break;

    case BUTTON_EVT_RELEASED | BUTTON_RIGHT: { // OK
        io_seproxyhal_touch_address_ok(NULL);
        break;
    }
    }
    return 0;
}

unsigned short io_exchange_al(unsigned char channel, unsigned short tx_len) {
    switch (channel & ~(IO_FLAGS)) {
    case CHANNEL_KEYBOARD:
        break;

    // multiplexed io exchange over a SPI channel and TLV encapsulated protocol
    case CHANNEL_SPI:
        if (tx_len) {
            io_seproxyhal_spi_send(G_io_apdu_buffer, tx_len);

            if (channel & IO_RESET_AFTER_REPLIED) {
                reset();
            }
            return 0; // nothing received from the master so far (it's a tx
                      // transaction)
        } else {
            return io_seproxyhal_spi_recv(G_io_apdu_buffer,
                                          sizeof(G_io_apdu_buffer), 0);
        }

    default:
        THROW(INVALID_PARAMETER);
    }
    return 0;
}

void app_main(void) {
    unsigned int rx, tx;
    unsigned short sw;

    tx = 0;
    for (;;) {
        rx = 0;
        BEGIN_TRY {
            TRY {
                rx = io_exchange(CHANNEL_APDU, tx);
                if (rx == 0) {
                    THROW(0x6982);
                }
                tx = 0;
            }
            CATCH_OTHER(e) {
                switch (e & 0xF000) {
                case 0x6000:
                case 0x9000:
                    sw = e;
                    break;
                default:
                    sw = 0x6800 | (e & 0x7FF);
                    break;
                }
                G_io_apdu_buffer[0] = sw >> 8;
                G_io_apdu_buffer[1] = sw;
                tx = 2;
            }
            FINALLY {
            }
        }
        END_TRY;

        if (tx == 0) {
            tx = handle_apdu(G_io_apdu_buffer, rx);
        }
    }
}

void io_seproxyhal_display(const bagl_element_t *element) {
    return io_seproxyhal_display_default((bagl_element_t *)element);
}

unsigned char io_event(unsigned char channel) {
    // nothing done with the event, throw an error on the transport layer if
    // needed

    // can't have more than one tag in the reply, not supported yet.
    switch (G_io_seproxyhal_spi_buffer[0]) {
    case SEPROXYHAL_TAG_FINGER_EVENT:
        UX_FINGER_EVENT(G_io_seproxyhal_spi_buffer);
        break;

    case SEPROXYHAL_TAG_BUTTON_PUSH_EVENT:
        UX_BUTTON_PUSH_EVENT(G_io_seproxyhal_spi_buffer);
        break;

#ifdef HAVE_BLE
    // Make automatically discoverable again when disconnected

    case SEPROXYHAL_TAG_BLE_CONNECTION_EVENT:
        if (G_io_seproxyhal_spi_buffer[3] == 0) {
            // TODO : cleaner reset sequence
            // first disable BLE before turning it off
            G_io_seproxyhal_spi_buffer[0] = SEPROXYHAL_TAG_BLE_RADIO_POWER;
            G_io_seproxyhal_spi_buffer[1] = 0;
            G_io_seproxyhal_spi_buffer[2] = 1;
            G_io_seproxyhal_spi_buffer[3] = 0;
            io_seproxyhal_spi_send(G_io_seproxyhal_spi_buffer, 4);
            // send BLE power on (default parameters)
            G_io_seproxyhal_spi_buffer[0] = SEPROXYHAL_TAG_BLE_RADIO_POWER;
            G_io_seproxyhal_spi_buffer[1] = 0;
            G_io_seproxyhal_spi_buffer[2] = 1;
            G_io_seproxyhal_spi_buffer[3] = 3; // ble on & advertise
            io_seproxyhal_spi_send(G_io_seproxyhal_spi_buffer, 5);
        }
        break;
#endif

    case SEPROXYHAL_TAG_DISPLAY_PROCESSED_EVENT:
        UX_DISPLAYED_EVENT({});
        break;

    case SEPROXYHAL_TAG_TICKER_EVENT:
        UX_TICKER_EVENT(G_io_seproxyhal_spi_buffer, {
            // don't redisplay if UX not allowed (pin locked in the common bolos
            // ux ?)
            if (ux_step_count && UX_ALLOWED) {
                // prepare next screen
                ux_step = (ux_step + 1) % ux_step_count;
                // redisplay screen
                UX_REDISPLAY();
            }
        });
        break;

    // unknown events are acknowledged
    default:
        UX_DEFAULT_EVENT();
        break;
    }

    // close the event if not done previously (by a display or whatever)
    if (!io_seproxyhal_spi_is_status_sent()) {
        io_seproxyhal_general_status();
    }
    // command has been processed, DO NOT reset the current APDU transport
    return 1;
}

void app_exit(void) {
    BEGIN_TRY_L(exit) {
        TRY_L(exit) {
            os_sched_exit(-1);
        }
        FINALLY_L(exit) {
        }
    }
    END_TRY_L(exit);
}

__attribute__((section(".boot"))) int main(void) {
    // exit critical section
    __asm volatile("cpsie i");

#ifdef MODE_SERVER
    init_server();
#endif

    for (;;) {
        UX_INIT();

        // ensure exception will work as planned
        os_boot();

        BEGIN_TRY {
            TRY {
                io_seproxyhal_init();

    #ifdef TARGET_NANOX
                // grab the current plane mode setting
                G_io_app.plane_mode = os_setting_get(OS_SETTING_PLANEMODE, NULL, 0);
    #endif // TARGET_NANOX

                USB_power(0);
                USB_power(1);

                ui_idle();

    #ifdef HAVE_BLE
                BLE_power(0, NULL);
                BLE_power(1, "Nano X");
    #endif // HAVE_BLE

                app_main();
            }
            CATCH(EXCEPTION_IO_RESET) {
                // reset IO and UX before continuing
                continue;
            }
            CATCH_ALL {
                break;
            }
            FINALLY {
            }
        }
        END_TRY;
    }

    app_exit();
    return 0;
}
