Network
Hard
Networking
AUTHOR
Dragoș Bacitea
MISSION
BRIEFING
A telecom operator is seeing fraudulent roaming activity and disputed billing events. Investigators recovered SS7 signalling, Diameter sessions, and the related billing export.

Reconstruct the intrusion chain from those records and recover its marker. This is a constructed, offline protocol-forensics case.

Attachments: ss7_capture.pcap, diameter_capture.pcap, billing_events.json

Flag format: CSCTF{8_lowercase_hex}

Flag construction: SHA-256 the literal text <IMSI>:<SESSION_ID>:<FIRST_ANOMALOUS_BILLING_TIMESTAMP>, then use the first 8 lowercase hex characters. Use the values exactly as written in the evidence and literal : separators.

Flag derivation (serialization spec): the flag is sha256("<imsi>:<full_diameter_session_id>:<unix_timestamp>")[:8], lowercase hex.

Serialization details:

imsi = the anomalous IMSI as decimal (e.g. 226012014000001).
full_diameter_session_id = the entire Session-Id including dots and semicolons (e.g. host.example.com;seconds;id), not just the GT fragment.
unix_timestamp = unix seconds (integer) of the first anomalous billing event, not ISO.
Fields joined as strings with : between them. No hosts, no GTs, no event ids.
