Crypto
Medium
AUTHOR
Michalina Moszyńska
MISSION
BRIEFING
The SABRELINK field authentication unit on an Ash Army proxy brigade's fires-control net, facing coalition lines in the Operation Dawn theatre, tags every dispatch with AES-128-GCM. A firmware fault made it reuse one message nonce across a run of dispatches.

We intercepted three authenticated dispatches under that nonce plus one sealed master order, whose text is sealed with AES-128-CTR under the link's per-nonce authentication value. Recover the master order. Handout: watchword.zip, 1,207 bytes, SHA-256 1e081c278b16e265391a8c6cf68cf2787ff2e54aae574b6c2d1cf0cada02647e. Submit the recovered master-order text.

Flag format: CSCTF{...}
