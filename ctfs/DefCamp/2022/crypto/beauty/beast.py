
from beast_tls import *

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 4444))
secret = all_requests("flag: CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}")
found = ''.join(secret)
print "\n" + found
connection.close()