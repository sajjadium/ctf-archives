Network
Easy
AUTHOR
Cosmin Gorea
MISSION
BRIEFING
A state-sponsored actor infiltrated a national satellite ground station and suppressed the telemetry of an unauthorized orbital adjustment. We recovered the modified CCSDS telemetry parser and the demodulated frame stream from the incident window.

Identify the anomaly in the parser's logic, then find the suppressed packet in the stream.

telem_parser.exe is a Windows binary. ground_station_rx.bin is the captured frame stream.

Flag format: CSCTF{<APID-in-hex>_<Timestamp-in-epoch>_<Payload-CRC16-in-hex>} Example: CSCTF{01A_1795300000_A1B2}
