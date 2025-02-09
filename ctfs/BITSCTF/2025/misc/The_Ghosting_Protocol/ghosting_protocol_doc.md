# Ghosting Protocol Documentation

## Overview
Just like that person who left your texts on 'seen' for days, the Ghosting Protocol is a custom peer-to-peer messaging protocol that acknowledges received messages with nothing but a cold, emotionless "seen" response. No explanations, no closure, just the void staring back at you. 

## Packet Structure
Each Ghosting Packet consists of the following fields, like the desperate attempts to reach out before the inevitable silence:

| Field           | Size  | Description                                    |
|---------------|------|------------------------------------------------|
| Version       | 1B   | Protocol version (default: 1)                  |
| Type          | 1B   | Packet type (DATA, SEEN, ERROR)                |
| Flags         | 1B   | Control flags (DEV, SYN, ACK, ERROR, FIN, PSH) |
| RSV           | 4B   | Reserved field (default: `xxxx`)               |
| Payload Length | 1B   | Length of the payload (0-255 bytes)            |
| Payload       | Variable | Optional message data                        |

## Packet Types

Because sometimes, the only thing you get back is silence.

| Type  | Value | Description                                      |
|-------|-------|--------------------------------------------------|
| DATA  | 0x01  | Contains actual message data—your heartfelt text.|
| SEEN  | 0x02  | The equivalent of "k." It hurts.                 |
| ERROR | 0x03  | Signals that something went wrong. Like your relationship.|

## Flags
Flags control packet behavior, much like the mixed signals you keep receiving.

| Flag  | Value    | Description                         |
|------|---------|---------------------------------|
| DEV  | 0b10000000 | Developer access flag—because some get special treatment.|
| SYN  | 0b01000000 | Synchronization request to establish connection. No proper handshake, no talk. |
| ACK  | 0b00100000 | Acknowledgment—"Yeah, I got it, whatever."|
| ERROR| 0b00010000 | Signals a mistake, like trusting them.|
| FIN  | 0b00001000 | Indicates termination, as sudden as that last message.|
| PSH  | 0b00000100 | Urges immediate delivery. Too bad they won’t reply.|

## Connection Establishment (Handshake First, Always)
Before you can start sending messages (and getting ignored), you must establish a connection properly. The client must initiate with a **SYN** packet. The server, if willing to acknowledge your existence, will respond with **ACK**. Only after this tragic formality is complete can real communication begin.

Failure to follow this sequence? Well, expect radio silence. Again.

### Handshake Example:
1. **Client:** Sends a packet with `SYN` flag set.
2. **Server:** Replies with `ACK` if it's open to a connection.
3. **Client:** Finally sends actual data (DATA packet).
4. **Server:** Replies with a SEEN packet, leaving you questioning your life choices.

## Implementation

### GhostingPacket Class
The `GhostingPacket` class lets you experience what it's like to be ignored programmatically. 

#### Constructor
```python
GhostingPacket(version=1, packet_type=PacketType.DATA, flags=0, rsv=b'xxxx', payload=b'')
```
- **version**: Protocol version (default: 1)
- **packet_type**: Type of packet (DATA, SEEN, ERROR)
- **flags**: Bitwise flags for control information
- **rsv**: Reserved 4-byte field (default: `xxxx`)
- **payload**: Variable-length message data

#### Methods
- **`pack()`**: Serializes the packet into bytes, like you packing up your dignity.
- **`unpack(data)`**: Deserializes bytes into a `GhostingPacket` object, if only you could unpack the truth.
- **`validate()`**: Ensures compliance with protocol constraints. Unlike people.
- **`__str__()`**: Returns a string representation for debugging your heartbreak.

### Example Usage

#### Sending a Message (Foolishly Hoping for a Reply)
```python
packet = GhostingPacket(packet_type=PacketType.DATA, flags=Flags.DEV, payload=b'Hello?')
packed_data = packet.pack()
print(packed_data)
```

#### Receiving a Response (Or Lack Thereof)
```python
received_packet = GhostingPacket.unpack(packed_data)
print(received_packet)
```

## Error Handling
Because mistakes were made.
- Invalid packet types result in a `ValueError`, just like choosing to text first.
- Payload exceeding 255 bytes throws an exception—much like an overlong paragraph that gets ignored.
- Incorrect `rsv` field length is rejected. Just like you.

## Future Extensions
- Support for encrypted payloads (because some things should remain unsaid).
- Additional handshake mechanisms (but let's be honest, they're not reaching out).
- More sophisticated error handling (like handling rejection with grace).
- To limit the powers of dev and make sure that reserved things stayed reserved.
---
**Author:** A Heartbroken Developer 😔  
**Version:** 1.0  
**Last Updated:** February 2025  

