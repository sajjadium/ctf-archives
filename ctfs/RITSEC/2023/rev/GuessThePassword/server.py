from encoding import Encoder
import socket, sys, time, threading


class Server:
    def __init__(self, PORT, DEBUG=True):
        self.HOST = ""
        self.PORT = PORT
        self.DEBUG = DEBUG
        self.accepting_connections = False
        self.encoder = Encoder("supersecret.json")
        self.connections = {}

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.soc.bind((self.HOST,self.PORT))
        except socket.error as err:
            print("Error binding to socket\n\t{0}\n\t{1}".format(err[0],err[1]))
            sys.exit(1)

        self.debug_print("Server set up")


    def debug_print(self, msg):
        if self.DEBUG:
            print(msg)


    def stop_accepting_connections(self):
        self.accepting_connections = False


    def user_is_rate_limited(self, client_ip):
        if not client_ip in self.connections:
            self.connections[client_ip] = time.time()
            return False
        
        elif time.time()-self.connections[client_ip] < 10:
            return True

        else:
            self.connections[client_ip] = time.time()
            return False


    def listen_for_connection(self):
        self.accepting_connections = True
        while self.accepting_connections:
            self.debug_print("Waiting for client")
            self.soc.listen()

            client_connection = self.soc.accept()

            client_thread = threading.Thread(target=self.chatter, args = (client_connection,))
            client_thread.start()      


    def chatter(self, connection_info):
        self.debug_print("Client connected")
        client_socket = connection_info[0]
        client_ip = connection_info[1][0]

        if self.user_is_rate_limited(client_ip):
            client_socket.send( "You are being rate limited".encode() )
            client_socket.close()
            return

        client_socket.send( "Enter the passcode to access the secret: \n".encode() )
        user_input = client_socket.recv(1024).decode() [:8]

        if len(user_input) == 8 and self.encoder.check_input(user_input):
            secret = self.encoder.flag_from_pwd(user_input)
            response = f"RS{ {secret} }\n"

        else:
            response = "That password isn't right!\n\tHint: The last 8 digits of your phone number\n"

        response += "\nClosing connection...\n"
        client_socket.send(response.encode())
        client_socket.close()

        self.debug_print("Client connection closed")


def main():
    serv = Server(1337)
    serv.listen_for_connection()


if __name__ == "__main__":
    main()
