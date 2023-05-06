from pwn import *
context.log_level = 'debug' #will print all input and output for debugging purposes
conn = remote("server",port) #enter the address and the port here as strings. For example nc 0.0.0.0 5000 turns into remote('0.0.0.0', 5000)
def get_input(): #function to get one line from the netcat
    input = conn.recvline().strip().decode()
    return input
def parse(polynomial):
    '''
    TODO: Parse polynomial
    For example, parse("x^3 + 2x^2 - x + 1") should return [1,2,-1,1]
    '''
for _ in range(4): get_input() #ignore challenge flavortext
for i in range(100):
    type = get_input()
    coeffs = parse(get_input())
    print(coeffs)
    ans = -1
    if 'sum of the roots' in type:
        ans = -1
        #TODO: Find answer
    elif 'sum of the reciprocals of the roots' in type:
        ans = -1
        #TODO: Find answer
    elif 'sum of the squares of the roots' in type:
        ans = -1
        #TODO: Find answer
    conn.sendline(str(ans)) #send answer to server
    get_input()
conn.interactive() #should print flag if you got everything right