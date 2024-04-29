While listening to my favourite radio station, the wonderful music has been interrupted by this weird radio signal. We only know that the embedded message is generated using this driver:

def generate_packet(sequence_no, data):
    packet = b'\x13\x37' + b'\xbe\xef' # SRC and DST
    packet += sequence_no.to_bytes(1, 'big') # sequence number
    packet += len(data).to_bytes(1, 'big') + data.encode() # len + data
    packet += zlib.crc32(packet).to_bytes(4, 'big') # crc
    return b'\xaa\xaa' + packet
