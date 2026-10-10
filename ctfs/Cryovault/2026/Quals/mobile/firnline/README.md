AJ

Field technicians on the SHARD-24 traverse log ice-core custody in FIRNLINE, the Android app attached here. Open a station link at the address below and set it as the Station URL in the app's Settings; the custodian's release entry on your station is sealed. Thaw the vault.


# FIRNLINE field client 3.2.0

Field technicians on the SHARD-24 traverse log ice-core custody with FIRNLINE. The app
keeps working offline and syncs with the station whenever it can reach it.

## Setup

1. Install `firnline.apk` on an Android 6.0 or later phone or emulator (arm64-v8a or
   x86_64), for example `adb install firnline.apk`.
2. Open the station address from the challenge page in a browser and press **Open a
   station link**. Open **Settings** in the app and set the **Station URL** to the link it
   shows (`https://.../s/<link>/`).
3. Tap **Sync**. The first sync enrolls the device with the station.

Your link is your station alone: keep it within your team. Point the app, or anything you
write, at it. Scripts can open a link with `POST /session` and `Accept: application/json`.
A link closes after about three hours without traffic; a new link opens a new station.

The station keeps a limited number of devices and forgets the one that has been quiet
longest. A forgotten device gets `403 unknown device`; enrolling again with the same
install id brings it back. The app does this by itself.

## Build

| | |
|---|---|
| package | `org.isfcr.firnline` 3.2.0 (320) |
| APK sha256 | `624fc914497079003f8599a50191a40b89dd17b74c914e84b96f2d0d9f1cdd86` |
| signer certificate sha256 | `8242dcb85e2b59641d59887fef7ef79c839a45d6ae3eff04344bf0274dff9f4d` |
| size | 41498 bytes |
