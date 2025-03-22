import struct

def compress_bmp(input_file, output_file):
    with open(input_file, "rb") as f:
        header = f.read(54)  # BMP header (first 54 bytes)
        pixel_data = f.read()

    compressed_data = bytearray()
    prev_byte = None
    count = 0

    for byte in pixel_data:
        transformed_byte = byte ^ 0xAA  # XOR with 0xAA for obfuscation
        
        if transformed_byte == prev_byte and count < 255:
            count += 1
        else:
            if prev_byte is not None:
                compressed_data.append(prev_byte)
                compressed_data.append(count)
            prev_byte = transformed_byte
            count = 1

    # Append the last byte
    if prev_byte is not None:
        compressed_data.append(prev_byte)
        compressed_data.append(count)

    with open(output_file, "wb") as f:
        f.write(header)  # Write BMP header
        f.write(compressed_data)  # Write compressed pixel data

    print(f"Compression complete. Original size: {len(pixel_data)} bytes, Compressed size: {len(compressed_data)} bytes")

if __name__ == "__main__":
    compress_bmp("flag.bmp", "compressed_data")

