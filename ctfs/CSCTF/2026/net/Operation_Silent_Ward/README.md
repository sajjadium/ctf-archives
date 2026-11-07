Network
Hard
Networking
AUTHOR
Dragoș Bacitea
MISSION
BRIEFING
A compromised medical-imaging device leaked patient data across a hospital network. The DICOM capture, device configuration, access ledger, SNMP alerts, and recovered exfiltration stream must be treated as corroborating evidence rather than independent answers.

Reconstruct the intrusion and recover its marker from the supplied offline evidence.

Attachments: hospital_network.pcap, dicom_device.xml, patient_records.csv, snmp_trap.log, exfil_stream.bin

Flag format: CSCTF{8_lowercase_hex}

Flag derivation (serialization spec): the flag is sha256("<dicom_serial>:<snmp_iso_timestamp>:<leak_count>:<anomaly_count>:<manifest_seed>")[:8], lowercase hex.

Serialization details:

dicom_serial = the device serial string from dicom_device.xml.
snmp_iso_timestamp = the exact ISO 8601 timestamp from the anomalous event in snmp_trap.log, with T and trailing Z.
leak_count = number of leaked patient records as decimal integer.
anomaly_count = number of anomalous C-STORE operations in the pcap as decimal integer.
manifest_seed = the calibration seed that must agree between dicom_device.xml and snmp_trap.log, as decimal.
Fields joined as strings with : between them. No binary packing. No other fields.
