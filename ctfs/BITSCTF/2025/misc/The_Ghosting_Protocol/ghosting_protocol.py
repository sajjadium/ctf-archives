import struct
from enum import IntEnum

class PacketType(IntEnum):
    DATA = 0x01
    SEEN = 0x02
    ERROR = 0x03

class Flags:
    DEV = 0b10000000
    SYN = 0b01000000
    ACK = 0b00100000
    ERROR = 0b00010000
    FIN = 0b00001000
    PSH = 0b00000100
    

class GhostingPacket:
    """
    Packet structure:
    - version (1 byte)
    - type (1 byte)
    - flags (1 byte)
    - rsv (4 bytes string)
    - payload_length (1 byte)
    - payload (variable length)
    """
    def __init__(self, version=1, packet_type=PacketType.DATA, flags=0, rsv=b'xxxx',payload_length = 0, payload=b''):
        if not isinstance(rsv, bytes) or len(rsv) != 4:
            raise ValueError("RSV must be exactly 4 bytes")
        
        self.version = version
        self.packet_type = packet_type
        self.flags = flags
        self.rsv = rsv
        self.payload = payload
        self.payload_length = len(payload)

    def pack(self):
        """Pack the packet into bytes"""
        if len(self.payload) > 255:
            raise ValueError("Payload too large (max 255 bytes)")
            
        header = struct.pack('!BBB4sB', 
            self.version,
            int(self.packet_type),  
            self.flags,
            self.rsv,
            self.payload_length
        )
        return header + self.payload

    @classmethod
    def unpack(cls, data):
        """Unpack bytes into a packet"""
        if len(data) < 8:
            raise ValueError("Packet too short (minimum 8 bytes)")
            
        
        version, packet_type, flags, rsv, payload_length = struct.unpack('!BBB4sB', data[:8])
        
        if len(data) < 8 + payload_length:
            raise ValueError(f"Packet payload incomplete. Expected {payload_length} bytes")
            
        payload = data[8:8+payload_length]
        
        try:
            packet_type = PacketType(packet_type)
        except ValueError:
            raise ValueError(f"Invalid packet type: {packet_type}")
            
        return cls(version, packet_type, flags, rsv,payload_length, payload)

    def __str__(self):
        """String representation for debugging"""
        flags_str = []
        if self.flags & Flags.DEV: flags_str.append("DEV")
        if self.flags & Flags.SYN: flags_str.append("SYN")
        if self.flags & Flags.ACK: flags_str.append("ACK")
        if self.flags & Flags.ERROR: flags_str.append("ERROR")
        if self.flags & Flags.FIN: flags_str.append("FIN")
        
        return (f"GhostingPacket(version={self.version}, "
                f"type={self.packet_type.name}, "
                f"flags=[{' | '.join(flags_str)}], "
                f"rsv={self.rsv}, "
                f"payload_length={self.payload_length}, "
                f"payload={self.payload})")

    def validate(self):
        
        if self.version != 1:
            raise ValueError("Unsupported version")
            
        if not isinstance(self.packet_type, PacketType):
            raise ValueError("Invalid packet type")
            
        if len(self.rsv) != 4:
            raise ValueError("RSV must be exactly 4 bytes")
            
        if len(self.payload) > 255:
            raise ValueError("Payload too large")