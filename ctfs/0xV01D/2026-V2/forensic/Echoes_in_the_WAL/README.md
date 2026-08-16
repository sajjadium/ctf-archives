Difficulty: Expert
Expected solve time: 2–4 hours

At 21:03 a field phone received a notification confirming an encrypted attachment was ready. Seconds later the attachment was replaced and a remote deletion policy ran. The current database says everything is gone, but the evidence collector captured the app files while it was active.

Recover the attachment that was valid at the exact notification time, then extract the flag.

Preserve the originals; some SQLite tools change directory state when opened.
The phone timezone is documented in the package.
No password guessing or brute force is required.
Every fact required to decrypt the attachment is inside the evidence set.
Flag format: 0xV01D{...}
