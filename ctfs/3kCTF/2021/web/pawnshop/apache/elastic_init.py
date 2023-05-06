from elasticsearch import Elasticsearch
import random
import string

def id_generator(size=6, chars=string.ascii_lowercase+ string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

es_client = Elasticsearch(['http://172.30.0.7:9200'])

FLAG = '3k{*REDACTED*}'

entries=[]

entries.append({"id":1,"picture":"axe.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"Memory leak Axe","value":id_generator(10)})
entries.append({"id":2,"picture":"drill.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"SUID drill","value":id_generator(10)})
entries.append({"id":3,"picture":"rifle.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"ROP rifle","value":id_generator(10)})
entries.append({"id":4,"picture":"bullets.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"Syscall bullets","value":id_generator(10)})
entries.append({"id":5,"picture":"flag.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"Flag","value":FLAG})
entries.append({"id":6,"picture":"hammer.png","seller":id_generator()+"@pawnshop.2021.3k.ctf.to","item":"0day hammer","value":id_generator(10)})

body = []
for entry in entries:
    body.append({'index': {'_id': entry['id']}})
    body.append(entry)

response = es_client.bulk(index='pawnshop',  body=body)

print(response)