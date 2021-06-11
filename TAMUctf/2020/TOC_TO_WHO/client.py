import grpc
import argparse
import protobuf_pb2
import protobuf_pb2_grpc
import signal

class UserLogoutError(Exception):
    pass

def signal_handler(signum, frame):
    raise UserLogoutError('Logging user out')

class Client:
    def __init__(self,hname,p,uname):
        self.hostname = hname
        self.port = p
        self.username = uname
        self.stub = protobuf_pb2_grpc.EchoServiceStub(grpc.insecure_channel(hname+":"+p))
        self.password = ''

def encrypt(client, message):
    xored = []
    temp_pass = client.password
    for i in range(len(message)):
        xored_value = ord(message[i%len(message)]) ^ ord(temp_pass[i%len(temp_pass)])
        xored.append(chr(xored_value))
    return ''.join(xored)

def decrypt(client, message):
    return encrypt(client, message)

def login(client):
    response = input("You are about to login as user \"" + client.username + "\". Would you like to proceed? (y/n): ")
    if response[0] == 'n':
        client.username = input("Enter a new username: ")
    client.password = input("Enter a new password: ")
    reply = client.stub.Login(protobuf_pb2.Request(username=client.username,msg=client.password))
    print(reply.msg)

def logout(client):
    reply = client.stub.Logout(protobuf_pb2.ServiceUser(username=client.username))
    print('User',client.username,'logging off.')


def echoClient(hostname,port,username):
    client = Client(hostname, port, username)
    login(client)
    signal.signal(signal.SIGINT, signal_handler)
    try:
        print("Secure Echo Service starting up... Enter \"quit\" to exit.")
        while True:
            message = input("Message: ")
            if message == 'quit':
                logout(client)
                break
            reply = client.stub.SendEcho(protobuf_pb2.Request(username=client.username,msg=encrypt(client, message)))
            reply = client.stub.ReceiveEcho(protobuf_pb2.ServiceUser(username=client.username))
            print(decrypt(client, reply.msg))
    except UserLogoutError:
        logout(client)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some arguments")
    parser.add_argument('--host',default='localhost')
    parser.add_argument('-p','--port',default='3010')
    parser.add_argument('-u','--user',default='default')
    args = parser.parse_args()
    echoClient(args.host,args.port,args.user)
