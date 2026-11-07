Reverse engineering
Hard
Reverse
AUTHOR
Chronos Security
MISSION
BRIEFING
An inert relay bench from Brenzava, which supplies relay hardware to the Operation Dawn coalition, was recovered after an unattributed supply-chain compromise. It exposes one stopped GDB Remote Serial Protocol (RSP) endpoint, and the extracted controller image and a historical bench capture came with it. The capture may record an old maintenance session, and nothing in it proves a recorded value is still valid on a live bench.

Work out how the controller activates its sealed diagnostic bank, recover the staged incident tasking and submit the code it contains. ghost-bank.zip holds firmware.bin, firmware-load.txt and capture.ndjson. Start your own bench from this page; it gives you a host and port for a raw TCP RSP connection (not HTTP), for example target remote <host>:<port> in gdb-multiarch. Work only against your own bench.

Flag format: CSCTF{...}
