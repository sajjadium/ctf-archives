Forensics
Hard
AUTHOR
Dragoș Bacitea
MISSION
BRIEFING
Reconnaissance drone Valkyrie-9 drifted off its approved waypoint while the command server recorded the mission as nominal. Reconcile the recovered client and backend logic with the flight record, telemetry, and radio intercept to show how the diversion avoided the alarm.

This is a constructed offline forensic case.

Attachments: drone_control.decompiled, command_backend.decompiled, flight_log.bin, mission_manifest.json, radio_intercept.log, telemetry_logs.json

Flag format: CSCTF{16_lowercase_hex}

Flag construction: SHA-256 the concatenated text <APPROVED_LAT_4DP><APPROVED_LON_4DP><LAT_OFFSET_6DP><LON_OFFSET_6DP><DISTANCE_1DP> with no separators, then use the first 16 lowercase hex characters. The flight-log tag verifies the last 8 characters of the same digest; it is not an input.

Flag derivation (serialization spec): the flag is sha256(f"{approved_lat:.4f}{approved_lon:.4f}{delta_lat:.6f}{delta_lon:.6f}{displacement_m:.1f}")[:16], lowercase hex.

Serialization details:

approved_lat / approved_lon = the manifest-approved coordinates, 4 decimal places each.
delta_lat / delta_lon = the per-axis delta between approved and diverted coordinates, 6 decimal places each (in degrees).
displacement_m = computed great-circle distance in meters between approved and diverted points, 1 decimal place.
Fields concatenated with no separator. The TAG: value in flight_log.bin matches the last 8 hex of the same sha256 — it is a verification check, not part of the flag.
