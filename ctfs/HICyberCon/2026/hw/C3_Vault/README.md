by Hidden Investigations
hardware
A retired ESP32-C3 gateway still has access to a remote vault. The recovery lab preserved its SPI flash and eFuse read-register window. Recover its enrollment credentials and convince the live service that you are the gateway.

The gateway runs a custom enrollment application built with ESP-IDF. The supplied artifacts are a reproducible lab acquisition; see recovery.txt for their exact format. The endpoint is a host-side authentication verifier, not an emulated shell.

No brute force or physical board is required. The event flag exists only on the live instance, not in the downloadable evidence.
