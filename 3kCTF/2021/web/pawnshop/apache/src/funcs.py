#!/usr/bin/python3
import cgi, cgitb ,json
from elasticsearch import Elasticsearch
from email.utils import parseaddr
import json
import re

es_client = Elasticsearch(['http://172.30.0.7:9200'])

def api(jsonv):
	print("Content-type: application/json\r\n\r\n")
	print(json.dumps(jsonv))	
	exit()

def verify_email(mail):
	parsedEmail = parseaddr(mail)[1]
	if parsedEmail == '' or parsedEmail != mail or not re.findall(r'.+@.+\..+',parsedEmail):
		api({'msg':'invalid email'})
	
def save_bid(tbid):
	save_file = open("/dev/null","w")
	save_file.write(tbid)
	save_file.close()

def list_items():
	body = {
            "query": {
	            "match_all": {}
	        }
	}
	res = es_client.search(index="pawnshop", body=body)
	printout={}
	if(len(res['hits']['hits'])>0):
		for i in res['hits']['hits']:
			printout[i['_id']]={'seller':i['_source']['seller'],'item':i['_source']['item'],"picture":i['_source']['picture']}
		api({"list":printout})
	api({"msg":"error"})

def lookupSeller(emailAddr):
	body = {
		'query': {
		        'query_string': {
		            'query': 'id:>0 AND seller:"'+emailAddr+'"',
		            "default_field":"seller"
		        }
		    }
	}
	res = es_client.search(index="pawnshop", body=body)
	if(len(res['hits']['hits'])>0):
		return emailAddr+' found'
	return 'not found'
