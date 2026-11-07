Reverse engineering
Medium
Rev
AUTHOR
Dan-Andrei Grigorescu
MISSION
BRIEFING
A TL-9 Vireo reconnaissance UAV of the Aurelian Air Surveillance Corps drifted ~380 m off its approved waypoint mid-sortie. The command server's signed audit trail says the flight was nominal — every waypoint within tolerance, hash-chain intact. A state actor tracked as Sable Drift is believed to have injected a single crafted command.

You are the attribution analyst. You have the uplink capture, the drone's flight-control software, and the signed audit trail. Prove the waypoint the drone actually flew — and why the server never saw it.

Endpoint: GET /schema for the submission format; submit to POST /submit. Artifacts are served at /files/.

Flag format: CSCTF{...}
