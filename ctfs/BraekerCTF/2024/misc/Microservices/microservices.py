from scapy.all import *
load_layer("http")
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random


def dropTheFlag(flag):

    # Flag falls into bits
    pieces = bytes_to_long(flag.encode())
    pieces = bin(pieces)
    pieces = pieces[2:]
    pieces = [int(x) for x in pieces]

    # Bits get scattered about
    d = {}
    for i,x in enumerate(pieces):
        d[i]=x
    l = list(d.items())
    random.shuffle(l)
    pieces = dict(l)

    return pieces


# It was right here
flag = "brck{not_the_flag}"

# Oh dang I dropped the flag
pieces = dropTheFlag(flag)

# Let's pick it back up
pickMapping = {}
for i,v in enumerate(pieces):
    pickMapping[i] = (v, pieces[v])


# Neat TCP things
FIN = 0x01
SYN = 0x02
PSH = 0x08
ACK = 0x10

# Server IP for filter
serverIP = "server_ip"

# Totally valid HTTP response
body = b"HTTP/1.1 404 OK\r\nConnection: close\r\nContent-Type: text/html\r\n\r\nKeep guessing!"


def processWebRequest(payload, dport):
    
    # Secret and piece of flag
    secret, b = pickMapping[dport-1000]

    # Extract guess from request
    filterString = b'GET /guess?guess='
    guess = 0
    try:
        guess = payload[len(filterString)+2:payload.find(' ', len(filterString)+2)]
        guess = int(guess)
    except:
        guess = 0

    # Return based on guess
    body_ret = body + b' guess = ' + str(guess).encode() + b'\r\n'

    if guess > secret:
        return 1, body_ret
    elif guess == secret:
        return 2+b, body_ret
    else:
        return 0, body_ret


def packet_callback(pkt):

    # User packet
    ip = pkt[IP]
    tcp = pkt[TCP]
    payload = str(bytes(tcp.payload))

    # Init response packet
    ip_response = IP(src=ip.dst, dst=ip.src)

    # No response by default
    pkt_resp = False

    # ACK some SYNS
    if tcp.flags == SYN:

        syn_ack_tcp = TCP(sport=tcp.dport, dport=tcp.sport, flags="SA", ack=tcp.seq + 1, seq=1337)
        pkt_resp = ip_response / syn_ack_tcp
    
    # Respond to the PSH
    elif tcp.flags & PSH == PSH:

        if len(payload) > 10:
            ret, lbody = processWebRequest(payload, tcp.dport)
        
        # Reply OOB
        pkt_resp = (ip_response / 
                    TCP(sport=tcp.dport, dport=tcp.sport, flags="PAF", seq=1338, ack=tcp.seq+len(tcp.payload)) / 
                    Raw(lbody))
        send(pkt_resp)
        pkt_resp = (ip_response / 
                    TCP(sport=tcp.dport, dport=tcp.sport, flags="PAF", seq=7331+ret, ack=tcp.seq+len(tcp.payload)) / 
                    Raw(lbody))

    # ACK them FINs
    elif tcp.flags & FIN == FIN:
        pkt_resp = ip_response / TCP(sport=tcp.dport, dport=tcp.sport, flags="RA", seq=tcp.ack, ack=tcp.seq+len(tcp.payload))

    # Respond if applicable
    if pkt_resp:
        send(pkt_resp)


# Filter packets for required ports
def packet_filter(pkt):
    return (TCP in pkt and
            pkt[IP].dst == serverIP and
            pkt[TCP].dport >= 1000 and pkt[TCP].dport <= 1000+len(pickMapping)-1)


# Spin up hundreds of webservices just like in the cloud
sniff(filter="tcp", prn=packet_callback, lfilter=packet_filter)

