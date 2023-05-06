#!/usr/bin/python3
from funcs import *

form = cgi.FieldStorage() 
action = form.getvalue('action')

if action=='list':
	list_items()
elif action=='bid':
	mail    = form.getvalue('mail')
	item_id = form.getvalue('item_id')
	amount  = form.getvalue('amount')
	if(mail != None and item_id != None and amount != None):
		verify_email(mail)
		save_bid(mail+"|"+item_id+"|"+amount+"\n\n")
		api({'msg':'bid saved, we will contact winners when auction ends'})
	api({'msg':'error'})
else:
	api(False)