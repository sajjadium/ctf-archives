#!/usr/bin/env python3
import base64
import argparse
from PIL import Image
import math

def make_image(enc, outfile):
	enc = list(enc)
	dimension = int(math.sqrt(len(enc)*4))+1

	img = Image.new( 'RGB', (dimension,dimension), "black")
	pixels = img.load()

	colours = [
		(255, 0, 0),
		(0, 0, 255),
		(0, 128, 0),
		(255, 255, 0)
	]
	x,y = 0,0
	for i in enc:
		part = []
		part.append((ord(i)>>6)&3)
		part.append((ord(i)>>4)&3)
		part.append((ord(i)>>2)&3)
		part.append((ord(i)>>0)&3)
		for i in range(4):
			if(x==dimension):
				y+=1
				x=0
			pixels[x,y] = colours[part[i]]
			x +=1

	# img.show()
	img.save(outfile+".png")


def parse_file(filename):
	file = open(filename, "rb")
	enc = base64.b64encode(file.read()).decode()
	return enc

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', required=True, help="File to picturify")
	parser.add_argument('--out', default="output", help="Output file")

	args = parser.parse_args()
	filename = args.file
	outfile = args.out
	enc = parse_file(filename) 
	make_image(enc, outfile)
