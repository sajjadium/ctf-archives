from struct import unpack

png = open('flag.png', 'rb').read()

new = [b'\x89PNG\r\n\x1a\n']
i = 8
while i < len(png):
	size = png[i:i+4]
	chunk = size[::-1]
	chunk = png[i+4:i+8] + chunk
	chunk = png[i+8:i+8+unpack('>I', size)[0]] + chunk
	new.append(chunk)
	new = new[::-1]
	i = i + 8 + unpack('>I', size)[0] + 4

open('scrambled.png', 'wb').write(b''.join(new))
