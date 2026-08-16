Difficulty: Expert
Expected solve time: 2–4 hours

A mysterious inline device failed just after midnight. Two synchronized capture points surrounded it and were merged into one PCAPNG. Logs say the device modified one binary upload without changing TCP sequence space while other uploads continued in the background.

Identify the changed flow, recover the evidence that exists on neither side alone, and extract the flag.

Keep PCAPNG interface identity. A duplicated packet is not necessarily an identical copy. No brute force or external service is required.

Flag format: 0xV01D{...}
