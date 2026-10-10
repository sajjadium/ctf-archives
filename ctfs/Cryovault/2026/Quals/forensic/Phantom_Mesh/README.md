SR

A smart lighting mesh at an office has a device on it that nobody added, and it sends a short diagnostics report at the same time every day. You get an over the air radio capture, the raw signal straight off the coordinator antenna, and the vendor's notes on their protocol. Nobody has the network key. Recover the report and read the flag out of it.

You are given mesh.pcap, the raw I/Q trace and nonces under traces/, and the vendor protocol notes under docs/. The flag is in isfcr{...} format, with printable ASCII and no spaces inside the braces.
