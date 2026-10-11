Zaza

The GHOST-13 line controller kept a remote manufacturing cell alive through a brief power failure. When it restarted, its maintenance gateway received two diagnostic writes that should never have looked alike. The hardware is gone, but the plant retained a firmware image, its IEC-style program/configuration dump, Modbus/TCP capture, buzzer recording, OTA update, serial log, and a damaged service manual excerpt.

Reconstruct the active configuration and the reboot sequence. Recover the diagnostic secret sealed in the maintenance update.

This is a fictional, fully offline investigation. No PLC, network service, or outside account is needed.

Files: plc_firmware.bin, plc_program.bin, plc_traffic.pcap, alarm_buzzer.wav, maintenance_update.ota, uart_log.txt, field_service_excerpt.txt

Flag format: isfcr{[a-z0-9_]+}
