# Corvex Aerosystems — Field Re-Provisioning Note (RECOVERED)

Internal field-service note recovered from an engineering laptop. Applies to the
CX-series inspection UAV signing subsystem.

- Command and telemetry use **MAVLink 2 message signing**. The per-airframe
  session signing key is provisioned at the depot and is **not** carried on the
  link.
- Signing timestamps are **10 µs ticks from the airframe RTC**, counted since the
  unit's **commissioning epoch** (NOT the MAVLink 2015 epoch). Units ship with a
  per-unit RTC **rate tolerance** (offset *and* ppm drift differ per airframe);
  calibrate both from observed traffic before trusting any timestamp.
- Keys may be **re-provisioned in the field** with a `SETUP_SIGNING` message,
  authenticated by the unit's *provisioning key*:

  ```
  prov_key = HKDF-SHA256(
      ikm  = serial_ascii || commissioning_epoch,   # epoch = uint64, little-endian, seconds
      salt = session_nonce,                          # the unit announces it at connect
      info = "CX-PROV/v1",
      L    = 32)
  ```

- After re-provisioning, the unit stays in LOITER. Flight control follows the
  normal order: set mode GUIDED, arm, then command.
