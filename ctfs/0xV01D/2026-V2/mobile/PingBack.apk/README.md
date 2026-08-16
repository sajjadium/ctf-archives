A network monitoring app ships with an exported BroadcastReceiver that was meant for internal device diagnostics. The receiver listens for a custom action, validates an auth token and a sequence number, then decrypts and logs an internal unlock signal.

The developers never removed it from the release build. The receiver is listening. Send the right Intent and check the logs.
