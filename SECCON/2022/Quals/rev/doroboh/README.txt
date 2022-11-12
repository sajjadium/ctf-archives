The following diagram discribes what each file is.
Do not run araiguma.exe unless you fully understand the logic.

+-- Victim Machine --+       +-- Attacker Machine --+
| +--------------+   |       |   +-------------+    |
| | araiguma.exe |<------------->| kitsune.exe |    |
| +--------------+   |   ^   |   +-------------+    |
|        ^           |   |   |                      |
+--------|-----------+   |   +----------------------+
         |               |
  Memory |               | Packet
   Dump  |               | Capture
         |               |
  [ araiguma.DMP ] [ network.pcapng ]
