#!/usr/bin/env python3
import tempfile
import pathlib
import os

os.chdir(pathlib.Path(__file__).parent.resolve())

with tempfile.NamedTemporaryFile() as tmp:
	print('Send the file: (ended with "\\n-- EOF --\\n"):')
	s = input()
	while(s != '-- EOF --'):
		tmp.write((s+'\n').encode())
		s = input()
	tmp.flush()
	os.close(0)
	os.system('./jerry ' + tmp.name)


