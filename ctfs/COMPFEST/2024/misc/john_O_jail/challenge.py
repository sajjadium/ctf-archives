import inspect as [REDACTED]


blocked1 = ['eval', 'exec', 'execfile', 'compile', 'open',
    'file', 'input', 'import', 'getattr', 'setattr', 'delattr','attr', 'var', 'help',
    'dir', 'bytearray', 'bytes', 'memoryview', '__import__',  'os', 'sys', 'subprocess', 'shutil', 'socket', 'threading',
    'multiprocessing', 'ctypes', 'marshal', 'pickle', 'class', 'cPickle',
    'atexit', 'signal', 'resource', 'inspect', 'tempfile', 'decode', '__dict__', 'co', '__class__', '__bases__', '__mro__', '__subclasses__', '__code__', '__closure__', '__func__', '__self__',
    '__module__', '__defaults__', '__annotations__', '()', '[', '{', ']', '}', '0', '1', '2', '3', '4', '5', '6', 
    '7', '8', '9', 'True', 'False', '=', 'dict', 'update', 'pop', 'remove', 'set', 'breakpoint', ' ']

blocked2 = [';', '..', '&&', '|', '`', '$', '>', '<', '(', ')', '[', ']', '{', '}', '!', '#', '&', '*', '\\', '\n', '\r', '\x00',
    '%', '"', "'", 'wget', 'curl', 'rm', 'chmod', 'chown', 'perl', 'php', 'bash', 'sh', 'nc', 'netcat', 'ncat', 'echo',
    'touch', 'cat', 'cd', 'mv', 'cp', 'ftp', 'scp', 'ssh', 'telnet', 'perl', 'ruby', 'pip', 'apt-get', 'yum',
    'brew', 'kill', 'killall', 'nohup', 'service', 'systemctl', 'shutdown', 'reboot', 'poweroff', 'mkfs', 'fdisk', 'dd',
    'iptables', 'ufw', 'route', 'ifconfig', 'ip', 'passwd', 'useradd', 'userdel', 'groupadd', 'groupdel', 'usermod',
    'groupmod', 'sudo', 'su', 'cron', 'crontab', 'vi', 'nano', 'pwd', 'e', '?', 'awk', 'tac', 'tail', 'xxd', 'hd', 'diff', 'od', 'cut',
    'uniq', 'strings', 'fold', 'sort']

def secret_function(password):
    if password == [REDACTED]':
        print('John escaped from his cell! \nNow try helping him escaping the jail.')
        stage2()
    else:
        print('Nope! Try again.')

def stage1():
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["exit"]:
            break
        if check1(user_input) == False:
            break
        try:
            print(eval(user_input))
        except Exception as e:
            print("The police noticed your attempt. Try again.")
            return

def stage2():
    while True:
        user_input2 = input(">> ")
        if user_input2.lower() in ["exit"]:
            break
        if check2(user_input2) == False:
            break
        try:
            print(__import__('os').system(user_input2))
        except Exception as e:
            print("Bad attempt at escaping jail. Try again.")
            return
        
def check1(payload):
    if not payload.isascii(): return False
    for i in blocked1:
        if i in payload:
            print('Nice try, the police have found you and put you back in your cell.')
            return False
    return True

def check2(payload):
    if not payload.isascii(): return False
    words = payload.split()
    if len(words) < 2: return False
    for i in blocked2:
        if i in payload:
            print('You climbed the wrong wall. Try again.')
            return False
    return True

if __name__ == '__main__':
    print("John has been detained in prison for the second time.")
    print("Help him escape!")
    while True:
        print('''
What will you do?
    1. Write a payload
    2. Input jail cell password
    3. Exit
              ''')
        chosen = input("> ")
        if chosen == '1':
            print("Type 'exit' to quit.")
            stage1()
        elif chosen == '2':
            password = input("Enter your password: ")
            secret_function(password)
        elif chosen == '3':
            break
        else:
            print('Command not found!')
            break
    print('Bye.')
