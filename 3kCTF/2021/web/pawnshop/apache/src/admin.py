#!/usr/bin/python3
from funcs import *

form = cgi.FieldStorage() 
action = form.getvalue('action')

if action=='list':
	list_items()
elif action=='lookup':
	mail    = form.getvalue('mail')
	if(mail != None):
		verify_email(mail)
		api({'msg':lookupSeller(mail)})
	api({'msg':'error'})
elif action=='edit':
	api({'msg':'not implemented'})
else:
	api(False)

