by bekkaze
Binary Exploitation
The Commons makes your human half prove it at a public kiosk: play the terminal's little platformer, and it signs off that a person was here. The game is the whole authentication. Teach the cabinet to sign for a session that never happened.

The service is headless: it replays a recorded input stream, so play and record locally first, then submit the recording here. Run the handout as cabinet play to play (a/d move, w jump, j stomp, hold l for fine movement, q to quit and save) -- it writes an input recording. Feed that file to this endpoint in the cabinet replay format: a u32 big-endian frame count, then that many per-frame input bytes.
