by Hidden Investigations
hardware
A farm gateway was retired during a vault-key rotation. Its flash still holds a sealed record, and the recovery lab preserved a short broker session. Recover the record the gateway could authenticate.

The gateway uses official ESP32 Tasmota firmware with a custom Berry agent. The attachment is a reproducible laboratory fixture; recovery.txt inside the archive describes its acquisition assumptions and the matching tooling. Analyze both the flash image and the MQTT traffic.

This challenge is entirely offline. No physical board, running broker, emulator, brute force, or connection to the captured IP addresses is required.
